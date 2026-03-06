"""
Trigram decomposition of the King Wen sequence.

Decomposes all 64 hexagrams into lower/upper/nuclear trigrams,
maps the KW path through trigram-pair space, and characterizes
the relationship between the trigram split and the mirror-pair split.

Outputs structured data for all 6 tasks in Round 1.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN

# ── Constants ────────────────────────────────────────────────────────────────

TRIGRAM_MAP = {
    "111": ("Qian",    "☰", "Heaven",  "Father"),
    "000": ("Kun",     "☷", "Earth",   "Mother"),
    "100": ("Zhen",    "☳", "Thunder", "Eldest Son"),
    "010": ("Kan",     "☵", "Water",   "Middle Son"),
    "001": ("Gen",     "☶", "Mountain","Youngest Son"),
    "011": ("Xun",     "☴", "Wind",    "Eldest Daughter"),
    "101": ("Li",      "☲", "Fire",    "Middle Daughter"),
    "110": ("Dui",     "☱", "Lake",    "Youngest Daughter"),
}

# Mirror-pair generators: which bits they flip (0-indexed)
GENERATORS = {
    "id":  [],
    "O":   [0, 5],      # L1, L6
    "M":   [1, 4],      # L2, L5
    "I":   [2, 3],      # L3, L4
    "OM":  [0, 1, 4, 5], # L1, L2, L5, L6
    "OI":  [0, 2, 3, 5], # L1, L3, L4, L6
    "MI":  [1, 2, 3, 4], # L2, L3, L4, L5
    "OMI": [0, 1, 2, 3, 4, 5],  # all
}

# Generator signatures (which mirror pairs are asymmetric)
GEN_SIGNATURES = {
    "id":  (0, 0, 0),
    "O":   (1, 0, 0),
    "M":   (0, 1, 0),
    "I":   (0, 0, 1),
    "OM":  (1, 1, 0),
    "OI":  (1, 0, 1),
    "MI":  (0, 1, 1),
    "OMI": (1, 1, 1),
}

# Reverse lookup: signature → generator name
SIG_TO_GEN = {v: k for k, v in GEN_SIGNATURES.items()}


# ── Utility functions ────────────────────────────────────────────────────────

def bits(hex_idx):
    """Return 6-bit list for hexagram at 0-based index."""
    return [int(b) for b in KING_WEN[hex_idx][2]]

def lower_tri(h):
    """Lower trigram bits (L1,L2,L3) as string."""
    if isinstance(h, str):
        return h[:3]
    return ''.join(str(b) for b in h[:3])

def upper_tri(h):
    """Upper trigram bits (L4,L5,L6) as string."""
    if isinstance(h, str):
        return h[3:]
    return ''.join(str(b) for b in h[3:])

def nuclear_lower(h):
    """Nuclear lower trigram (L2,L3,L4) as string."""
    if isinstance(h, str):
        return h[1:4]
    return ''.join(str(b) for b in h[1:4])

def nuclear_upper(h):
    """Nuclear upper trigram (L3,L4,L5) as string."""
    if isinstance(h, str):
        return h[2:5]
    return ''.join(str(b) for b in h[2:5])

def tri_name(s):
    """Trigram name from binary string."""
    return TRIGRAM_MAP.get(s, ("?",))[0]

def tri_symbol(s):
    """Trigram symbol from binary string."""
    return TRIGRAM_MAP.get(s, ("?", "?"))[1]

def tri_image(s):
    """Trigram image from binary string."""
    return TRIGRAM_MAP.get(s, ("?", "?", "?"))[2]

def xor_sig(h):
    """XOR signature (orbit) of hexagram bits."""
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def reverse_bits(h):
    """Reverse a 6-bit list."""
    return list(reversed(h))

def complement_bits(h):
    """Complement a 6-bit list."""
    return [1 - b for b in h]

def yang_count(s):
    """Count yang (1) bits in a trigram string."""
    return sum(int(c) for c in s)


# ── Build full decomposition ─────────────────────────────────────────────────

def build_decomposition():
    """Build complete trigram decomposition for all 64 hexagrams."""
    hexagrams = []
    for idx in range(64):
        num, name, binary = KING_WEN[idx]
        h = bits(idx)
        lt = lower_tri(binary)
        ut = upper_tri(binary)
        nl = nuclear_lower(binary)
        nu = nuclear_upper(binary)
        sig = xor_sig(h)
        gen = SIG_TO_GEN.get(sig, "?")
        
        hexagrams.append({
            'idx': idx,
            'num': num,
            'name': name,
            'binary': binary,
            'bits': h,
            'lower': lt,
            'upper': ut,
            'nuc_lower': nl,
            'nuc_upper': nu,
            'lower_name': tri_name(lt),
            'upper_name': tri_name(ut),
            'nuc_lower_name': tri_name(nl),
            'nuc_upper_name': tri_name(nu),
            'orbit_sig': sig,
            'generator': gen,
        })
    return hexagrams


def build_pairs(hexagrams):
    """Build 32 KW pairs."""
    pairs = []
    for k in range(32):
        a = hexagrams[2*k]
        b = hexagrams[2*k + 1]
        
        # Determine pair type
        h_a = a['bits']
        h_b = b['bits']
        is_inv = (h_b == reverse_bits(h_a))
        is_comp = (not is_inv) and (h_b == complement_bits(h_a))
        
        # XOR mask
        xor = tuple(h_a[i] ^ h_b[i] for i in range(6))
        sig = (xor[0] & xor[5], xor[1] & xor[4], xor[2] & xor[3])
        # Actually the pair mask determines which generator connects them
        # The mask is the XOR pattern
        pair_sig = xor_sig(h_a)  # orbit signature
        pair_gen = SIG_TO_GEN.get(pair_sig, "?")
        
        # Trigram relationship
        share_lower = (a['lower'] == b['lower'])
        share_upper = (a['upper'] == b['upper'])
        
        pairs.append({
            'idx': k,
            'a': a,
            'b': b,
            'is_inv': is_inv,
            'is_comp': is_comp,
            'xor': xor,
            'pair_gen': pair_gen,
            'orbit_sig': pair_sig,
            'share_lower': share_lower,
            'share_upper': share_upper,
        })
    return pairs


# ══════════════════════════════════════════════════════════════════════════════
# TASK 1: Full trigram decomposition table
# ══════════════════════════════════════════════════════════════════════════════

def task1_decomposition(hexagrams):
    print("=" * 100)
    print("TASK 1: FULL TRIGRAM DECOMPOSITION TABLE")
    print("=" * 100)
    
    # First verify bit ordering with known hexagrams
    print("\n--- Verification ---")
    verify = [
        (28, "Kan", "010010", "Water", "Water"),
        (29, "Li", "101101", "Fire", "Fire"),
        (4,  "Xu", "111010", "Heaven", "Water"),
        (0,  "Qian", "111111", "Heaven", "Heaven"),
        (1,  "Kun", "000000", "Earth", "Earth"),
        (10, "Tai", "111000", "Heaven", "Earth"),
        (11, "Pi", "000111", "Earth", "Heaven"),
    ]
    all_ok = True
    for idx, exp_name, exp_bin, exp_lo, exp_up in verify:
        h = hexagrams[idx]
        lo_ok = (h['lower_name'] == exp_lo)
        up_ok = (h['upper_name'] == exp_up)
        status = "✓" if (lo_ok and up_ok) else "✗"
        if not (lo_ok and up_ok):
            all_ok = False
        print(f"  Hex #{h['num']:2d} {h['name']:10s} {h['binary']} "
              f"lower={h['lower_name']:8s}({'✓' if lo_ok else '✗'}) "
              f"upper={h['upper_name']:8s}({'✓' if up_ok else '✗'})")
    print(f"  All verified: {'YES' if all_ok else 'NO'}")
    
    # Full table
    print(f"\n{'#':>3s}  {'Name':<12s} {'Bits':6s}  "
          f"{'Lower':8s} {'Upper':8s}  "
          f"{'NucLo':8s} {'NucUp':8s}  "
          f"{'Orbit':7s} {'Gen':4s}")
    print("-" * 90)
    
    for h in hexagrams:
        sig_str = ''.join(map(str, h['orbit_sig']))
        print(f"{h['num']:3d}  {h['name']:<12s} {h['binary']}  "
              f"{h['lower_name']:8s} {h['upper_name']:8s}  "
              f"{h['nuc_lower_name']:8s} {h['nuc_upper_name']:8s}  "
              f"({sig_str})  {h['generator']:4s}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK 2: 8×8 trigram-pair grid
# ══════════════════════════════════════════════════════════════════════════════

def task2_grid(hexagrams):
    print("\n" + "=" * 100)
    print("TASK 2: 8×8 TRIGRAM-PAIR GRID")
    print("=" * 100)
    
    tri_order = ["111", "110", "101", "100", "011", "010", "001", "000"]
    tri_labels = [f"{tri_name(t):7s}" for t in tri_order]
    
    # Build grid: grid[lower][upper] = hexagram
    grid = {}
    for h in hexagrams:
        grid[(h['lower'], h['upper'])] = h
    
    # Print grid with KW numbers
    print(f"\n  Grid: rows = lower trigram, columns = upper trigram")
    print(f"  KW numbers:")
    print(f"\n{'':15s}", end="")
    for t in tri_order:
        print(f" {tri_name(t):>7s}", end="")
    print(f"\n{'':15s}", end="")
    for t in tri_order:
        print(f"  ({t})", end=" ")
    print()
    print("  " + "-" * 80)
    
    for lo in tri_order:
        print(f"  {tri_name(lo):7s}({lo})", end=" |")
        for up in tri_order:
            h = grid.get((lo, up))
            if h:
                print(f" {h['num']:5d}  ", end="")
            else:
                print(f"   --  ", end="")
        print()
    
    # Print grid with names
    print(f"\n  Hexagram names:")
    print(f"\n{'':15s}", end="")
    for t in tri_order:
        print(f" {tri_name(t):>9s}", end="")
    print()
    print("  " + "-" * 90)
    
    for lo in tri_order:
        print(f"  {tri_name(lo):7s}({lo})", end=" |")
        for up in tri_order:
            h = grid.get((lo, up))
            if h:
                print(f" {h['name']:>9s}", end="")
            else:
                print(f"       -- ", end="")
        print()
    
    # KW sequence positions on the grid
    print(f"\n  KW sequence position (1-64) on grid:")
    print(f"\n{'':15s}", end="")
    for t in tri_order:
        print(f" {tri_name(t):>7s}", end="")
    print()
    print("  " + "-" * 80)
    
    # Build position map
    pos_map = {}
    for idx, h in enumerate(hexagrams):
        pos_map[(h['lower'], h['upper'])] = idx + 1  # 1-based position
    
    for lo in tri_order:
        print(f"  {tri_name(lo):7s}({lo})", end=" |")
        for up in tri_order:
            pos = pos_map.get((lo, up), 0)
            if pos:
                print(f" {pos:5d}  ", end="")
            else:
                print(f"   --  ", end="")
        print()


# ══════════════════════════════════════════════════════════════════════════════
# TASK 3: KW path through trigram-pair space
# ══════════════════════════════════════════════════════════════════════════════

def task3_path(hexagrams):
    print("\n" + "=" * 100)
    print("TASK 3: KW PATH THROUGH TRIGRAM-PAIR SPACE")
    print("=" * 100)
    
    # Classify all 63 transitions
    transitions = []
    for i in range(63):
        h1 = hexagrams[i]
        h2 = hexagrams[i + 1]
        lo_change = (h1['lower'] != h2['lower'])
        up_change = (h1['upper'] != h2['upper'])
        
        if lo_change and up_change:
            ttype = "both"
        elif lo_change:
            ttype = "lower-only"
        elif up_change:
            ttype = "upper-only"
        else:
            ttype = "neither"
        
        is_within_pair = (i % 2 == 0)  # transition from even to odd index
        
        transitions.append({
            'from_idx': i,
            'to_idx': i + 1,
            'from_num': h1['num'],
            'to_num': h2['num'],
            'from_name': h1['name'],
            'to_name': h2['name'],
            'lo_change': lo_change,
            'up_change': up_change,
            'type': ttype,
            'is_within_pair': is_within_pair,
            'from_lower': h1['lower_name'],
            'from_upper': h1['upper_name'],
            'to_lower': h2['lower_name'],
            'to_upper': h2['upper_name'],
        })
    
    # Full transition list
    print(f"\n  {'Step':>4s}  {'From':>3s}→{'To':>3s}  "
          f"{'From Lo':>8s} {'From Up':>8s}  →  {'To Lo':>8s} {'To Up':>8s}  "
          f"{'Type':>11s}  {'PairBr':>6s}")
    print("  " + "-" * 95)
    
    for t in transitions:
        pair_label = "within" if t['is_within_pair'] else "bridge"
        print(f"  {t['from_idx']+1:>4d}  {t['from_num']:>3d}→{t['to_num']:>3d}  "
              f"{t['from_lower']:>8s} {t['from_upper']:>8s}  →  "
              f"{t['to_lower']:>8s} {t['to_upper']:>8s}  "
              f"{t['type']:>11s}  {pair_label:>6s}")
    
    # Statistics
    print("\n  --- Transition Statistics ---")
    type_counts = Counter(t['type'] for t in transitions)
    print(f"\n  All 63 transitions:")
    for ttype in ["both", "lower-only", "upper-only", "neither"]:
        print(f"    {ttype:>11s}: {type_counts.get(ttype, 0)}")
    
    # Within-pair vs bridge
    within = [t for t in transitions if t['is_within_pair']]
    bridge = [t for t in transitions if not t['is_within_pair']]
    
    print(f"\n  32 within-pair transitions (hex[2k] → hex[2k+1]):")
    within_counts = Counter(t['type'] for t in within)
    for ttype in ["both", "lower-only", "upper-only", "neither"]:
        print(f"    {ttype:>11s}: {within_counts.get(ttype, 0)}")
    
    print(f"\n  31 between-pair bridges (hex[2k+1] → hex[2k+2]):")
    bridge_counts = Counter(t['type'] for t in bridge)
    for ttype in ["both", "lower-only", "upper-only", "neither"]:
        print(f"    {ttype:>11s}: {bridge_counts.get(ttype, 0)}")
    
    # Asymmetry test
    all_lo = sum(1 for t in transitions if t['lo_change'])
    all_up = sum(1 for t in transitions if t['up_change'])
    within_lo = sum(1 for t in within if t['lo_change'])
    within_up = sum(1 for t in within if t['up_change'])
    bridge_lo = sum(1 for t in bridge if t['lo_change'])
    bridge_up = sum(1 for t in bridge if t['up_change'])
    
    print(f"\n  Lower vs upper trigram change frequency:")
    print(f"    All:    lower changes {all_lo}/63, upper changes {all_up}/63")
    print(f"    Within: lower changes {within_lo}/32, upper changes {within_up}/32")
    print(f"    Bridge: lower changes {bridge_lo}/31, upper changes {bridge_up}/31")
    
    return transitions


# ══════════════════════════════════════════════════════════════════════════════
# TASK 4: Two decompositions — trigram vs mirror-pair
# ══════════════════════════════════════════════════════════════════════════════

def task4_decompositions():
    print("\n" + "=" * 100)
    print("TASK 4: TRIGRAM SPLIT vs MIRROR-PAIR SPLIT")
    print("=" * 100)
    
    # Express each generator as trigram-level changes
    print(f"\n  Each generator flips specific bits.")
    print(f"  Lower trigram = (L1, L2, L3), Upper trigram = (L4, L5, L6)")
    print(f"  Lower trigram bit positions: L1=pos0, L2=pos1, L3=pos2")
    print(f"  Upper trigram bit positions: L4=pos0, L5=pos1, L6=pos2")
    print()
    
    print(f"  {'Gen':>4s}  {'Flips':>20s}  {'Lower Δ':>20s}  {'Upper Δ':>20s}  {'Lo bits':>10s}  {'Up bits':>10s}")
    print("  " + "-" * 95)
    
    for gen_name, flip_bits in GENERATORS.items():
        # Which bits in lower trigram change? (bits 0,1,2 = L1,L2,L3)
        lo_changes = [b for b in flip_bits if b < 3]
        # Which bits in upper trigram change? (bits 3,4,5 = L4,L5,L6, mapped to pos 0,1,2)
        up_changes = [b - 3 for b in flip_bits if b >= 3]
        
        flip_str = ','.join(f'L{b+1}' for b in flip_bits) if flip_bits else 'none'
        lo_str = ','.join(f'pos{b}(L{b+1})' for b in lo_changes) if lo_changes else 'none'
        up_str = ','.join(f'pos{b}(L{b+3})' for b in up_changes) if up_changes else 'none'
        lo_bits = len(lo_changes)
        up_bits = len(up_changes)
        
        print(f"  {gen_name:>4s}  {flip_str:>20s}  {lo_str:>20s}  {up_str:>20s}  "
              f"{lo_bits:>10d}  {up_bits:>10d}")
    
    # The cross-trigram nature of generators
    print(f"\n  --- Cross-Trigram Structure ---")
    print(f"\n  Each generator changes bits in BOTH trigrams (except id):")
    print(f"  This is the key difference: mirror-pair operations are cross-trigram.")
    print()
    
    # Detailed: what each generator does to trigram pair
    print(f"  Generator effects on trigram identity:")
    print()
    
    for gen_name, flip_bits in GENERATORS.items():
        if gen_name == "id":
            print(f"  {gen_name}: No change. (lower, upper) → (lower, upper)")
            continue
        
        lo_mask = [0, 0, 0]
        up_mask = [0, 0, 0]
        for b in flip_bits:
            if b < 3:
                lo_mask[b] = 1
            else:
                up_mask[b - 3] = 1
        
        lo_mask_str = ''.join(map(str, lo_mask))
        up_mask_str = ''.join(map(str, up_mask))
        
        # Example: apply to Heaven/Heaven (111 111)
        test_hex = [1, 1, 1, 1, 1, 1]
        result = test_hex.copy()
        for b in flip_bits:
            result[b] ^= 1
        result_lo = ''.join(map(str, result[:3]))
        result_up = ''.join(map(str, result[3:]))
        
        print(f"  {gen_name}: lower XOR {lo_mask_str}, upper XOR {up_mask_str}")
        print(f"       Example: Heaven/Heaven → {tri_name(result_lo)}/{tri_name(result_up)}")
    
    # For each orbit type (signature), what trigram transformation does the pair mask produce?
    print(f"\n  --- Pair Masks as Trigram Transformations ---")
    print(f"\n  The mask=signature identity means each orbit's pairs use a specific generator.")
    print(f"  For each generator, show the trigram XOR pattern:")
    print()
    
    print(f"  {'Gen':>4s}  {'Sig':>5s}  {'Lo XOR':>8s}  {'Up XOR':>8s}  "
          f"{'# Lo bits':>9s}  {'# Up bits':>9s}  {'Cross?':>6s}")
    print("  " + "-" * 65)
    
    for gen_name in ["id", "O", "M", "I", "OM", "OI", "MI", "OMI"]:
        flip_bits = GENERATORS[gen_name]
        sig = GEN_SIGNATURES[gen_name]
        sig_str = ''.join(map(str, sig))
        
        lo_mask = [0, 0, 0]
        up_mask = [0, 0, 0]
        for b in flip_bits:
            if b < 3:
                lo_mask[b] = 1
            else:
                up_mask[b - 3] = 1
        
        lo_xor = ''.join(map(str, lo_mask))
        up_xor = ''.join(map(str, up_mask))
        n_lo = sum(lo_mask)
        n_up = sum(up_mask)
        cross = "yes" if (n_lo > 0 and n_up > 0) else "no"
        
        print(f"  {gen_name:>4s}  ({sig_str})  {lo_xor:>8s}  {up_xor:>8s}  "
              f"{n_lo:>9d}  {n_up:>9d}  {cross:>6s}")
    
    # For complement pairs (OMI), show specific trigram transformation
    print(f"\n  --- Detailed: OMI (complement) pairs ---")
    print(f"  OMI flips ALL bits: lower → complement(lower), upper → complement(upper)")
    print(f"  This preserves the trigram split! Each trigram independently complements.")
    print()
    
    # For inversion pairs, show the non-trivial transformation
    print(f"  --- Inversion vs Trigram ---")
    print(f"  For inversion pairs (b = reverse(a)):")
    print(f"  lower_b = reverse(upper_a), upper_b = reverse(lower_a)")
    print(f"  This SWAPS the trigrams AND reverses each one.")
    print(f"  The inversion operation is NOT decomposable in the trigram basis.")
    print()
    
    # Show which generators preserve vs mix trigrams
    print(f"  --- Trigram Preservation Summary ---")
    for gen_name in ["id", "O", "M", "I", "OM", "OI", "MI", "OMI"]:
        flip_bits = GENERATORS[gen_name]
        lo_changes = [b for b in flip_bits if b < 3]
        up_changes = [b - 3 for b in flip_bits if b >= 3]
        
        if len(lo_changes) == 0 and len(up_changes) == 0:
            desc = "preserves both trigrams"
        elif len(lo_changes) == 0:
            desc = "preserves lower, changes upper"
        elif len(up_changes) == 0:
            desc = "changes lower, preserves upper"
        elif len(lo_changes) == 3 and len(up_changes) == 3:
            desc = "changes both completely (complement)"
        else:
            desc = f"partially changes both (lo:{len(lo_changes)}, up:{len(up_changes)})"
        
        print(f"  {gen_name:>4s}: {desc}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK 5: 32 pairs in trigram space
# ══════════════════════════════════════════════════════════════════════════════

def task5_pairs_trigram(pairs):
    print("\n" + "=" * 100)
    print("TASK 5: THE 32 PAIRS IN TRIGRAM SPACE")
    print("=" * 100)
    
    # Full pair table
    print(f"\n  {'P':>3s}  {'Hex A':>3s} {'Name A':<12s} {'Lo A':>8s} {'Up A':>8s}  "
          f"{'Hex B':>3s} {'Name B':<12s} {'Lo B':>8s} {'Up B':>8s}  "
          f"{'Share':>7s}  {'Gen':>4s}  {'Type':>5s}")
    print("  " + "-" * 115)
    
    for p in pairs:
        a, b = p['a'], p['b']
        
        if p['share_lower'] and p['share_upper']:
            share = "both"
        elif p['share_lower']:
            share = "lower"
        elif p['share_upper']:
            share = "upper"
        else:
            share = "neither"
        
        ptype = "comp" if p['is_comp'] else ("inv" if p['is_inv'] else "?")
        
        print(f"  {p['idx']+1:3d}  {a['num']:3d} {a['name']:<12s} "
              f"{a['lower_name']:>8s} {a['upper_name']:>8s}  "
              f"{b['num']:3d} {b['name']:<12s} "
              f"{b['lower_name']:>8s} {b['upper_name']:>8s}  "
              f"{share:>7s}  {p['pair_gen']:>4s}  {ptype:>5s}")
    
    # Group by sharing type
    print(f"\n  --- Trigram Sharing Summary ---")
    share_types = Counter()
    for p in pairs:
        if p['share_lower'] and p['share_upper']:
            share_types["both"] += 1
        elif p['share_lower']:
            share_types["lower only"] += 1
        elif p['share_upper']:
            share_types["upper only"] += 1
        else:
            share_types["neither"] += 1
    
    for stype in ["both", "lower only", "upper only", "neither"]:
        cnt = share_types.get(stype, 0)
        pair_list = []
        for p in pairs:
            if p['share_lower'] and p['share_upper']:
                s = "both"
            elif p['share_lower']:
                s = "lower only"
            elif p['share_upper']:
                s = "upper only"
            else:
                s = "neither"
            if s == stype:
                pair_list.append(p['idx'] + 1)
        print(f"  {stype:>11s}: {cnt} pairs — {pair_list}")
    
    # Cross-tabulate sharing type with generator
    print(f"\n  --- Sharing Type × Generator ---")
    cross = defaultdict(lambda: defaultdict(int))
    for p in pairs:
        if p['share_lower'] and p['share_upper']:
            s = "both"
        elif p['share_lower']:
            s = "lower"
        elif p['share_upper']:
            s = "upper"
        else:
            s = "neither"
        cross[p['pair_gen']][s] += 1
    
    gens_present = sorted(set(p['pair_gen'] for p in pairs))
    print(f"  {'Gen':>4s}  {'both':>5s}  {'lower':>5s}  {'upper':>5s}  {'neither':>7s}  {'total':>5s}")
    for gen in gens_present:
        row = cross[gen]
        total = sum(row.values())
        print(f"  {gen:>4s}  {row.get('both',0):5d}  {row.get('lower',0):5d}  "
              f"{row.get('upper',0):5d}  {row.get('neither',0):7d}  {total:5d}")
    
    # For inversion pairs: detail the trigram swap
    print(f"\n  --- Inversion Pairs: Trigram Transformation Detail ---")
    print(f"  For inversion: b = reverse(a)")
    print(f"  lower_b = reverse(upper_a), upper_b = reverse(lower_a)")
    print()
    
    inv_pairs = [p for p in pairs if p['is_inv']]
    for p in inv_pairs:
        a, b = p['a'], p['b']
        lo_a = a['lower']
        up_a = a['upper']
        lo_b = b['lower']
        up_b = b['upper']
        
        # Verify reversal relationship
        rev_up_a = up_a[::-1]
        rev_lo_a = lo_a[::-1]
        ok = (lo_b == rev_up_a and up_b == rev_lo_a)
        
        # Check: does reversal change the trigram identity?
        lo_a_rev = lo_a[::-1]
        up_a_rev = up_a[::-1]
        lo_same = (lo_a == lo_a_rev)
        up_same = (up_a == up_a_rev)
        
        # A trigram is palindromic if reverse(t) = t
        # Palindromic trigrams: 000, 010, 101, 111
        # Non-palindromic: 001↔100, 011↔110
        
        print(f"  P{p['idx']+1:2d}: ({a['lower_name']:>8s}/{a['upper_name']:>8s}) → "
              f"({b['lower_name']:>8s}/{b['upper_name']:>8s})  "
              f"rev✓={ok}  gen={p['pair_gen']}")
    
    # Complement pairs: trigram complement
    print(f"\n  --- Complement Pairs: Trigram Transformation ---")
    comp_pairs = [p for p in pairs if p['is_comp']]
    for p in comp_pairs:
        a, b = p['a'], p['b']
        print(f"  P{p['idx']+1:2d}: ({a['lower_name']:>8s}/{a['upper_name']:>8s}) → "
              f"({b['lower_name']:>8s}/{b['upper_name']:>8s})  gen={p['pair_gen']}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK 6: Nuclear trigrams
# ══════════════════════════════════════════════════════════════════════════════

def task6_nuclear(hexagrams, pairs):
    print("\n" + "=" * 100)
    print("TASK 6: NUCLEAR TRIGRAMS")
    print("=" * 100)
    
    # Full nuclear trigram table
    print(f"\n  {'#':>3s}  {'Name':<12s} {'Bits':6s}  "
          f"{'Lo':8s} {'Up':8s}  {'NucLo':8s} {'NucUp':8s}  "
          f"{'NL yang':>7s} {'NU yang':>7s}")
    print("  " + "-" * 85)
    
    for h in hexagrams:
        nl_y = yang_count(h['nuc_lower'])
        nu_y = yang_count(h['nuc_upper'])
        print(f"  {h['num']:3d}  {h['name']:<12s} {h['binary']}  "
              f"{h['lower_name']:8s} {h['upper_name']:8s}  "
              f"{h['nuc_lower_name']:8s} {h['nuc_upper_name']:8s}  "
              f"{nl_y:>7d} {nu_y:>7d}")
    
    # Nuclear trigram frequency
    print(f"\n  --- Nuclear Trigram Frequency ---")
    nuc_lo_freq = Counter(h['nuc_lower_name'] for h in hexagrams)
    nuc_up_freq = Counter(h['nuc_upper_name'] for h in hexagrams)
    
    print(f"\n  {'Trigram':>8s}  {'As NucLo':>8s}  {'As NucUp':>8s}")
    for t_bits in ["111", "110", "101", "100", "011", "010", "001", "000"]:
        tn = tri_name(t_bits)
        print(f"  {tn:>8s}  {nuc_lo_freq.get(tn, 0):>8d}  {nuc_up_freq.get(tn, 0):>8d}")
    
    # Verify Theorem 12: nuclear trigram rule ≡ M-component
    print(f"\n  --- Verification: Nuclear Trigram Rule ≡ M-component ---")
    print(f"  M-component: L2=yin (0) first")
    print(f"  Nuclear rule: nuclear lower yang < nuclear upper yang (first hex)")
    print(f"  These should be identical for all M-decisive pairs.")
    print()
    
    # M-decisive pairs: where L2 ≠ L5 in the first hexagram
    print(f"  {'P':>3s}  {'First':>3s} {'Name':<12s}  {'L2':>2s} {'L5':>2s}  "
          f"{'M-dec?':>6s}  {'L2=yin?':>7s}  "
          f"{'NL yang':>7s} {'NU yang':>7s}  {'NL<NU?':>6s}  {'Match':>5s}")
    print("  " + "-" * 90)
    
    m_decisive = 0
    m_match = 0
    m_l2yin_count = 0
    
    for p in pairs:
        a = p['a']
        h = a['bits']
        L2 = h[1]
        L5 = h[4]
        decisive = (L2 != L5)
        
        if decisive:
            m_decisive += 1
            l2_yin = (L2 == 0)
            nl_y = yang_count(a['nuc_lower'])
            nu_y = yang_count(a['nuc_upper'])
            nl_less = (nl_y < nu_y)
            match = (l2_yin == nl_less)
            if match:
                m_match += 1
            if l2_yin:
                m_l2yin_count += 1
            
            print(f"  {p['idx']+1:3d}  {a['num']:3d} {a['name']:<12s}  "
                  f"{L2:2d} {L5:2d}  {'yes':>6s}  {'yes' if l2_yin else 'no':>7s}  "
                  f"{nl_y:>7d} {nu_y:>7d}  {'yes' if nl_less else 'no':>6s}  "
                  f"{'✓' if match else '✗':>5s}")
        else:
            print(f"  {p['idx']+1:3d}  {a['num']:3d} {a['name']:<12s}  "
                  f"{L2:2d} {L5:2d}  {'no':>6s}  {'---':>7s}  "
                  f"{'---':>7s} {'---':>7s}  {'---':>6s}  {'---':>5s}")
    
    print(f"\n  M-decisive pairs: {m_decisive}")
    print(f"  L2=yin in first hex: {m_l2yin_count}/{m_decisive}")
    print(f"  Nuclear rule matches M-component: {m_match}/{m_decisive}")
    
    # Nuclear trigram relationships: how do nuclear trigrams relate to primary?
    print(f"\n  --- Nuclear vs Primary Trigram Relationships ---")
    print(f"  Nuclear lower (L2,L3,L4) shares L2,L3 with lower tri, L4 with upper tri")
    print(f"  Nuclear upper (L3,L4,L5) shares L3 with lower tri, L4,L5 with upper tri")
    print()
    
    # Count: how often does nuclear lower = primary lower? Or primary upper?
    nl_eq_lo = sum(1 for h in hexagrams if h['nuc_lower'] == h['lower'])
    nl_eq_up = sum(1 for h in hexagrams if h['nuc_lower'] == h['upper'])
    nu_eq_lo = sum(1 for h in hexagrams if h['nuc_upper'] == h['lower'])
    nu_eq_up = sum(1 for h in hexagrams if h['nuc_upper'] == h['upper'])
    
    print(f"  Nuclear lower = Primary lower: {nl_eq_lo}/64")
    print(f"  Nuclear lower = Primary upper: {nl_eq_up}/64")
    print(f"  Nuclear upper = Primary lower: {nu_eq_lo}/64")
    print(f"  Nuclear upper = Primary upper: {nu_eq_up}/64")
    
    # Nuclear trigram pair frequency (which combinations appear)
    nuc_pair_freq = Counter((h['nuc_lower_name'], h['nuc_upper_name']) for h in hexagrams)
    print(f"\n  Nuclear (lower, upper) pair frequency:")
    print(f"  Unique combinations: {len(nuc_pair_freq)}/64")
    for (nl, nu), cnt in sorted(nuc_pair_freq.items(), key=lambda x: -x[1]):
        if cnt > 1:
            which = [h['num'] for h in hexagrams 
                     if h['nuc_lower_name'] == nl and h['nuc_upper_name'] == nu]
            print(f"    ({nl:>8s}, {nu:>8s}): {cnt}× — hex {which}")
    
    # KW path through nuclear trigram space
    print(f"\n  --- KW Path in Nuclear Trigram Space ---")
    print(f"  Nuclear trigram transitions at within-pair and bridge steps:")
    
    nuc_within_changes = {"both": 0, "nuc_lo_only": 0, "nuc_up_only": 0, "neither": 0}
    nuc_bridge_changes = {"both": 0, "nuc_lo_only": 0, "nuc_up_only": 0, "neither": 0}
    
    for i in range(63):
        h1 = hexagrams[i]
        h2 = hexagrams[i + 1]
        nl_change = (h1['nuc_lower'] != h2['nuc_lower'])
        nu_change = (h1['nuc_upper'] != h2['nuc_upper'])
        
        if nl_change and nu_change:
            key = "both"
        elif nl_change:
            key = "nuc_lo_only"
        elif nu_change:
            key = "nuc_up_only"
        else:
            key = "neither"
        
        if i % 2 == 0:  # within pair
            nuc_within_changes[key] += 1
        else:  # bridge
            nuc_bridge_changes[key] += 1
    
    print(f"\n  Nuclear trigram changes:")
    print(f"  {'Type':>15s}  {'Within (32)':>11s}  {'Bridge (31)':>11s}  {'Total (63)':>10s}")
    for key in ["both", "nuc_lo_only", "nuc_up_only", "neither"]:
        w = nuc_within_changes[key]
        b = nuc_bridge_changes[key]
        print(f"  {key:>15s}  {w:>11d}  {b:>11d}  {w+b:>10d}")


# ══════════════════════════════════════════════════════════════════════════════
# ADDITIONAL: Trigram palindrome analysis
# ══════════════════════════════════════════════════════════════════════════════

def additional_palindrome():
    """Which trigrams are palindromic (unchanged by bit reversal)?"""
    print("\n" + "=" * 100)
    print("ADDITIONAL: TRIGRAM PALINDROME STRUCTURE")
    print("=" * 100)
    
    palindromic = []
    non_palindromic_pairs = []
    
    for bits_str, (name, sym, image, family) in TRIGRAM_MAP.items():
        rev = bits_str[::-1]
        if bits_str == rev:
            palindromic.append((bits_str, name))
        else:
            if bits_str < rev:  # avoid counting twice
                non_palindromic_pairs.append((bits_str, rev, name, tri_name(rev)))
    
    print(f"\n  Palindromic trigrams (reverse = self): {len(palindromic)}")
    for bits, name in palindromic:
        print(f"    {bits} = {name}")
    
    print(f"\n  Non-palindromic pairs (reverse ≠ self): {len(non_palindromic_pairs)}")
    for b1, b2, n1, n2 in non_palindromic_pairs:
        print(f"    {b1} ({n1}) ↔ {b2} ({n2})")
    
    print(f"\n  Significance for inversion pairs:")
    print(f"  When a hexagram is reversed (read upside-down),")
    print(f"  lower_b = reverse(upper_a), upper_b = reverse(lower_a)")
    print(f"  If both trigrams are palindromic, inversion = swap (lo↔up)")
    print(f"  If either is non-palindromic, inversion also changes trigram identity")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    hexagrams = build_decomposition()
    pairs = build_pairs(hexagrams)
    
    task1_decomposition(hexagrams)
    task2_grid(hexagrams)
    transitions = task3_path(hexagrams)
    task4_decompositions()
    task5_pairs_trigram(pairs)
    task6_nuclear(hexagrams, pairs)
    additional_palindrome()
    
    print("\n" + "=" * 100)
    print("TRIGRAM DECOMPOSITION COMPLETE")
    print("=" * 100)
