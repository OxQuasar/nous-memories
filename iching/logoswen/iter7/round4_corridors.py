"""
Round 4: Corridor analysis — the lag-4 mechanism, corridor × bridge interaction,
and connection to complementary coverage.

Questions from Round 3:
  1. Do corridors correspond to traditional hexagram groupings?
  2. Do corridors and preserving bridges reinforce each other?
  3. What mechanism produces the lag-4 periodicity?
  4. How does the corridor structure relate to complementary coverage?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN

RNG = np.random.default_rng(42)
N_TRIALS = 100_000

# ── Trigram constants ────────────────────────────────────────────────────────

TRIGRAM_INFO = {
    "111": ("Qian",  "☰", "Heaven"),
    "000": ("Kun",   "☷", "Earth"),
    "100": ("Zhen",  "☳", "Thunder"),
    "010": ("Kan",   "☵", "Water"),
    "001": ("Gen",   "☶", "Mountain"),
    "011": ("Xun",   "☴", "Wind"),
    "101": ("Li",    "☲", "Fire"),
    "110": ("Dui",   "☱", "Lake"),
}

GEN_SIGNATURES = {
    (0,0,0): "id", (1,0,0): "O", (0,1,0): "M", (0,0,1): "I",
    (1,1,0): "OM", (1,0,1): "OI", (0,1,1): "MI", (1,1,1): "OMI",
}


# ── Utility ──────────────────────────────────────────────────────────────────

def tri_name(s): return TRIGRAM_INFO.get(s, ("?",))[0]
def tri_sym(s): return TRIGRAM_INFO.get(s, ("?","?"))[1]
def bits(idx): return [int(b) for b in KING_WEN[idx][2]]
def xor_sig(h): return (h[0]^h[5], h[1]^h[4], h[2]^h[3])

def hamming3(a, b):
    return sum(c1 != c2 for c1, c2 in zip(a, b))

def kernel_dressing(xor_mask):
    kernel = []
    labels = ['O', 'M', 'I']
    for i, (a, b) in enumerate([(0,5), (1,4), (2,3)]):
        if xor_mask[a] == 1 and xor_mask[b] == 1:
            kernel.append(labels[i])
    return ''.join(kernel) if kernel else 'id'


# ── Build data ───────────────────────────────────────────────────────────────

hexagrams = []
for idx in range(64):
    num, name, binary = KING_WEN[idx]
    hexagrams.append({
        'idx': idx, 'num': num, 'name': name, 'binary': binary,
        'lo': binary[:3], 'up': binary[3:],
        'lo_name': tri_name(binary[:3]), 'up_name': tri_name(binary[3:]),
    })

# Build pair data
pair_data = []
for k in range(32):
    a = hexagrams[2*k]
    b = hexagrams[2*k + 1]
    sig_a = xor_sig(bits(2*k))
    gen = GEN_SIGNATURES.get(sig_a, "?")
    pair_data.append({
        'k': k, 'a': a, 'b': b, 'gen': gen,
    })

# Build bridge data
bridge_data = []
for k in range(31):
    exit_idx = 2*k + 1
    entry_idx = 2*k + 2
    exit_bin = KING_WEN[exit_idx][2]
    entry_bin = KING_WEN[entry_idx][2]
    exit_lo, exit_up = exit_bin[:3], exit_bin[3:]
    entry_lo, entry_up = entry_bin[:3], entry_bin[3:]
    lo_dist = hamming3(exit_lo, entry_lo)
    up_dist = hamming3(exit_up, entry_up)
    xor = tuple(int(exit_bin[i]) ^ int(entry_bin[i]) for i in range(6))
    k_dress = kernel_dressing(xor)
    bridge_data.append({
        'k': k, 'b_num': k+1,
        'exit_lo': exit_lo, 'exit_up': exit_up,
        'entry_lo': entry_lo, 'entry_up': entry_up,
        'lo_dist': lo_dist, 'up_dist': up_dist,
        'lo_shared': (lo_dist == 0), 'up_shared': (up_dist == 0),
        'kernel': k_dress,
        'exit_name': KING_WEN[exit_idx][1],
        'entry_name': KING_WEN[entry_idx][1],
        'exit_num': KING_WEN[exit_idx][0],
        'entry_num': KING_WEN[entry_idx][0],
    })

# Meaning confidence and fragility from iter6
meaning_conf = {
    1: 'Clear', 2: 'Clear', 3: 'Suggestive', 4: 'Clear', 5: 'Suggestive',
    6: 'Clear', 7: 'Clear', 8: 'Clear', 9: 'Clear', 10: 'Clear',
    11: 'Suggestive', 12: 'Clear', 13: 'Suggestive', 14: 'Suggestive',
    15: 'Suggestive', 16: 'Clear', 17: 'Suggestive', 18: 'Clear',
    19: 'Clear', 20: 'Clear', 21: 'Clear', 22: 'Clear',
    23: 'Clear', 24: 'Suggestive', 25: 'Clear', 26: 'Clear',
    27: 'Suggestive', 28: 'Clear', 29: 'Suggestive', 30: 'Clear',
    31: 'Suggestive', 32: 'Clear',
}

s2_pair_indices = {13, 14, 20, 26, 28, 30}  # 0-indexed
free_pairs = [i for i in range(32) if i not in s2_pair_indices]
kw_dom_bits = [0,1,2,4,7,8,13,18,19,22,25]
kw_dom_pairs = set()
tradeoff_pairs = set()
for bit_idx, pair_idx in enumerate(free_pairs):
    if bit_idx in kw_dom_bits:
        kw_dom_pairs.add(pair_idx)
    else:
        tradeoff_pairs.add(pair_idx)

def fragility(pair_0idx):
    if pair_0idx in s2_pair_indices: return 'S2'
    if pair_0idx in kw_dom_pairs: return 'KW-dom'
    return 'trade-off'


# ══════════════════════════════════════════════════════════════════════════════
# TASK A: Corridor identification and characterization
# ══════════════════════════════════════════════════════════════════════════════

def task_a():
    print("=" * 90)
    print("TASK A: CORRIDOR IDENTIFICATION AND CHARACTERIZATION")
    print("=" * 90)

    # The full 64-hex sequence as trigram sequences
    lo_seq = [h['lo'] for h in hexagrams]
    up_seq = [h['up'] for h in hexagrams]

    # Find all lag-4 matches (position i and i+4 share a trigram)
    print(f"\n  --- Lag-4 match enumeration ---")
    lag4_matches = []
    for i in range(60):  # i and i+4
        lo_match = (lo_seq[i] == lo_seq[i+4])
        up_match = (up_seq[i] == up_seq[i+4])
        if lo_match or up_match:
            lag4_matches.append({
                'pos': i+1,  # 1-based
                'pos4': i+5,
                'lo_match': lo_match,
                'up_match': up_match,
                'lo_tri': lo_seq[i] if lo_match else None,
                'up_tri': up_seq[i] if up_match else None,
            })

    print(f"  Total lag-4 matches: {len(lag4_matches)}/60")
    print(f"\n  {'Pos':>4s}  {'Pos+4':>5s}  {'Lo match':>10s}  {'Up match':>10s}  "
          f"{'Hex@pos':>12s}  {'Hex@pos+4':>12s}")
    print("  " + "-" * 75)

    for m in lag4_matches:
        p = m['pos'] - 1  # 0-based
        lo_str = f"{tri_name(m['lo_tri'])}" if m['lo_match'] else "—"
        up_str = f"{tri_name(m['up_tri'])}" if m['up_match'] else "—"
        print(f"  {m['pos']:4d}  {m['pos4']:5d}  {lo_str:>10s}  {up_str:>10s}  "
              f"{hexagrams[p]['name']:>12s}  {hexagrams[p+4]['name']:>12s}")

    # Find corridors: maximal chains of consecutive lag-4 matches involving the same trigram
    print(f"\n  --- Corridor extraction ---")
    print(f"  A corridor = maximal chain where positions p, p+4, p+8, ... all share")
    print(f"  the same trigram in the same role (lower or upper)")

    # For each trigram and role, find all positions where it appears
    tri_positions = defaultdict(lambda: defaultdict(list))
    for i, h in enumerate(hexagrams):
        tri_positions['lo'][h['lo']].append(i+1)  # 1-based
        tri_positions['up'][h['up']].append(i+1)

    # Find lag-4 chains
    corridors = []
    for role in ['lo', 'up']:
        for tri in sorted(TRIGRAM_INFO.keys()):
            positions = sorted(tri_positions[role][tri])
            # Find maximal chains where consecutive positions differ by exactly 4
            chains = []
            current_chain = [positions[0]] if positions else []
            for j in range(1, len(positions)):
                if positions[j] - current_chain[-1] == 4:
                    current_chain.append(positions[j])
                else:
                    if len(current_chain) >= 2:
                        chains.append(current_chain[:])
                    current_chain = [positions[j]]
            if len(current_chain) >= 2:
                chains.append(current_chain[:])

            for chain in chains:
                corridors.append({
                    'role': role,
                    'tri': tri,
                    'tri_name': tri_name(tri),
                    'positions': chain,
                    'length': len(chain),
                    'span': (chain[0], chain[-1]),
                    'pair_span': ((chain[0]+1)//2, (chain[-1]+1)//2),
                })

    # Sort by length descending
    corridors.sort(key=lambda c: -c['length'])

    print(f"\n  Found {len(corridors)} corridors (length ≥ 2):")
    print(f"\n  {'Role':>5s}  {'Trigram':>8s}  {'Length':>6s}  {'Positions':>30s}  "
          f"{'Pair span':>12s}  {'Hexagrams':>50s}")
    print("  " + "-" * 120)

    for c in corridors:
        pos_str = ','.join(str(p) for p in c['positions'])
        pair_str = f"P{c['pair_span'][0]}–P{c['pair_span'][1]}"
        hex_names = [hexagrams[p-1]['name'] for p in c['positions']]
        hex_str = ', '.join(hex_names)
        print(f"  {c['role']:>5s}  {c['tri_name']:>8s}  {c['length']:>6d}  "
              f"{pos_str:>30s}  {pair_str:>12s}  {hex_str}")

    # Corridor × pair mapping: which pairs are part of each corridor?
    print(f"\n  --- Corridor → pair membership ---")
    for c in corridors:
        pairs_in = set()
        for p in c['positions']:
            pairs_in.add((p-1)//2)  # 0-based pair index
        pair_list = sorted(pairs_in)
        pair_names = [f"P{k+1}({pair_data[k]['a']['name']}/{pair_data[k]['b']['name']})"
                      for k in pair_list]
        print(f"\n  {c['role'].upper():>5s} {c['tri_name']:>8s} "
              f"(len={c['length']}, pos {c['positions'][0]}–{c['positions'][-1]}):")
        for pn in pair_names:
            print(f"    {pn}")

    return corridors


# ══════════════════════════════════════════════════════════════════════════════
# TASK B: Corridor × bridge preservation interaction
# ══════════════════════════════════════════════════════════════════════════════

def task_b(corridors):
    print("\n" + "=" * 90)
    print("TASK B: CORRIDOR × BRIDGE PRESERVATION INTERACTION")
    print("=" * 90)

    preserving = [b for b in bridge_data if b['lo_shared'] or b['up_shared']]
    pres_set = set(b['k'] for b in preserving)

    # For each corridor, count how many of its internal bridges are preserving
    print(f"\n  --- Bridges within corridors ---")
    print(f"  A bridge Bk is 'within' a corridor if both its exit-pair and entry-pair")
    print(f"  belong to the corridor.")

    corridor_bridges = []
    for c in corridors:
        # Which pair indices belong to this corridor?
        pairs_in = set()
        for p in c['positions']:
            pairs_in.add((p-1)//2)
        # Which bridges connect consecutive pairs within the corridor?
        bridges_in = []
        pairs_sorted = sorted(pairs_in)
        for i in range(len(pairs_sorted) - 1):
            if pairs_sorted[i+1] == pairs_sorted[i] + 1:
                bridge_k = pairs_sorted[i]  # bridge k connects pair k to pair k+1
                if bridge_k < 31:
                    bridges_in.append(bridge_k)

        pres_in = [k for k in bridges_in if k in pres_set]
        corridor_bridges.append({
            'corridor': c,
            'bridges': bridges_in,
            'preserving': pres_in,
        })

        print(f"\n  {c['role'].upper():>5s} {c['tri_name']:>8s} "
              f"(pos {c['positions'][0]}–{c['positions'][-1]}):")
        print(f"    Pairs: {[p+1 for p in sorted(pairs_in)]}")
        print(f"    Internal bridges: {[k+1 for k in bridges_in]}")
        print(f"    Of which preserving: {[k+1 for k in pres_in]} ({len(pres_in)}/{len(bridges_in)})")

        # What do the preserving bridges preserve? Same trigram as corridor or different?
        for k in pres_in:
            b = bridge_data[k]
            if b['lo_shared']:
                pres_role = 'lo'
                pres_tri = b['exit_lo']
            else:
                pres_role = 'up'
                pres_tri = b['exit_up']
            same_as_corridor = (pres_role == c['role'] and pres_tri == c['tri'])
            print(f"      B{k+1}: preserves {pres_role.upper()}={tri_name(pres_tri)} "
                  f"{'← SAME as corridor' if same_as_corridor else '← different from corridor'}")

    # Count: how many preserving bridges fall inside corridors vs outside?
    bridges_in_any_corridor = set()
    for cb in corridor_bridges:
        bridges_in_any_corridor.update(cb['bridges'])

    pres_in_corridor = sum(1 for k in pres_set if k in bridges_in_any_corridor)
    pres_outside = len(pres_set) - pres_in_corridor
    total_in_corridor = len(bridges_in_any_corridor)
    total_outside = 31 - total_in_corridor

    print(f"\n  --- Summary: bridge × corridor ---")
    print(f"  Total bridges in corridors: {total_in_corridor}/31")
    print(f"  Preserving bridges in corridors: {pres_in_corridor}/{len(pres_set)}")
    print(f"  Preserving bridges outside corridors: {pres_outside}/{len(pres_set)}")
    if total_in_corridor > 0:
        rate_in = pres_in_corridor / total_in_corridor
    else:
        rate_in = 0
    if total_outside > 0:
        rate_out = pres_outside / total_outside
    else:
        rate_out = 0
    print(f"  Preservation rate inside corridors: {rate_in:.3f}")
    print(f"  Preservation rate outside corridors: {rate_out:.3f}")

    # Test: do preserving bridges correlate with corridors more than random?
    # Under null: randomly place 9 preserving bridges among 31 positions
    null_in = []
    for _ in range(N_TRIALS):
        perm = RNG.choice(31, size=9, replace=False)
        null_in.append(sum(1 for k in perm if k in bridges_in_any_corridor))
    null_in = np.array(null_in)
    p_val = np.mean(null_in >= pres_in_corridor)
    print(f"\n  MC test (preserving bridges inside corridors):")
    print(f"  KW: {pres_in_corridor}, null mean: {np.mean(null_in):.2f} ± {np.std(null_in):.2f}")
    print(f"  p(≥KW): {p_val:.4f}")

    return corridor_bridges


# ══════════════════════════════════════════════════════════════════════════════
# TASK C: The lag-4 mechanism — what produces it?
# ══════════════════════════════════════════════════════════════════════════════

def task_c():
    print("\n" + "=" * 90)
    print("TASK C: THE LAG-4 MECHANISM")
    print("=" * 90)

    lo_seq = [h['lo'] for h in hexagrams]
    up_seq = [h['up'] for h in hexagrams]

    # Lag-4 in the pair ordering: hex[i] and hex[i+4] connect corresponding
    # positions within pairs separated by 2.
    # Decompose: lag-4 = within-pair + bridge + within-pair + bridge
    # Or equivalently: first hex of pair k shares trigram with first hex of pair k+2

    # Test: is lag-4 carried by pair ordering, orientation, or both?

    # Metric: count of lag-4 trigram matches (lower or upper)
    def count_lag4_matches(seq):
        return sum(1 for i in range(len(seq) - 4) if seq[i] == seq[i+4])

    kw_lo_lag4 = count_lag4_matches(lo_seq)
    kw_up_lag4 = count_lag4_matches(up_seq)
    kw_combined_lag4 = kw_lo_lag4 + kw_up_lag4

    print(f"  KW lag-4 matches: lo={kw_lo_lag4}, up={kw_up_lag4}, combined={kw_combined_lag4}")

    # Decompose into 4 sub-types:
    # Type AA: first of pair k matches first of pair k+2 (positions 2k, 2k+4)
    # Type AB: first of pair k matches second of pair k+2 (positions 2k, 2k+5)
    # Type BA: second of pair k matches first of pair k+2 (positions 2k+1, 2k+3)
    # Type BB: second of pair k matches second of pair k+2 (positions 2k+1, 2k+5)
    # Wait — lag 4 means offset 4 positions. So:
    # pos i and pos i+4. In terms of pairs:
    # If i = 2k (first of pair k):   i+4 = 2k+4 = 2(k+2) = first of pair k+2 → AA
    # If i = 2k+1 (second of pair k): i+4 = 2k+5 = 2(k+2)+1 = second of pair k+2 → BB

    aa_matches_lo = 0
    bb_matches_lo = 0
    aa_matches_up = 0
    bb_matches_up = 0

    for k in range(30):  # k and k+2 pairs
        # AA: position 2k and 2(k+2)
        p1 = 2*k
        p2 = 2*(k+2)
        if p2 < 64:
            if lo_seq[p1] == lo_seq[p2]: aa_matches_lo += 1
            if up_seq[p1] == up_seq[p2]: aa_matches_up += 1

        # BB: position 2k+1 and 2(k+2)+1
        p1 = 2*k + 1
        p2 = 2*(k+2) + 1
        if p2 < 64:
            if lo_seq[p1] == lo_seq[p2]: bb_matches_lo += 1
            if up_seq[p1] == up_seq[p2]: bb_matches_up += 1

    print(f"\n  --- Lag-4 decomposition into AA and BB components ---")
    print(f"  AA (1st of pair k ↔ 1st of pair k+2):")
    print(f"    Lo: {aa_matches_lo}/30, Up: {aa_matches_up}/30")
    print(f"  BB (2nd of pair k ↔ 2nd of pair k+2):")
    print(f"    Lo: {bb_matches_lo}/30, Up: {bb_matches_up}/30")
    print(f"  Total: {aa_matches_lo + bb_matches_lo + aa_matches_up + bb_matches_up}")

    # Note: lag-4 = 60 possible positions total. AA contributes 30, BB contributes 30.
    # Combined lo+up lag-4 = (AA_lo + BB_lo + AA_up + BB_up) / 60

    # ── Test: pair ordering vs orientation ──
    print(f"\n  --- Separating pair ordering from orientation ---")

    # Test 1: Fix pair ordering, randomize orientation (free pairs only)
    # This tells us: does orientation contribute to lag-4?
    pair_hex = []  # [(first_bin, second_bin), ...] for each pair
    for k in range(32):
        pair_hex.append((KING_WEN[2*k][2], KING_WEN[2*k+1][2]))

    s2_set = {13, 14, 20, 26, 28, 30}  # 0-indexed

    null_orient_lag4 = []
    for _ in range(N_TRIALS):
        test_seq_lo = []
        test_seq_up = []
        for k in range(32):
            a, b = pair_hex[k]
            if k not in s2_set and RNG.random() < 0.5:
                a, b = b, a
            test_seq_lo.append(a[:3])
            test_seq_lo.append(b[:3])
            test_seq_up.append(a[3:])
            test_seq_up.append(b[3:])
        null_orient_lag4.append(count_lag4_matches(test_seq_lo) + count_lag4_matches(test_seq_up))

    null_orient_lag4 = np.array(null_orient_lag4)
    print(f"  Fix pair ordering, randomize orientation:")
    print(f"  KW combined lag-4: {kw_combined_lag4}")
    print(f"  Null: {np.mean(null_orient_lag4):.2f} ± {np.std(null_orient_lag4):.2f}")
    print(f"  p(≥KW): {np.mean(null_orient_lag4 >= kw_combined_lag4):.4f}")

    # Test 2: Randomize pair ordering, keep orientation within pairs
    null_order_lag4 = []
    for _ in range(N_TRIALS):
        perm = RNG.permutation(32)
        test_seq_lo = []
        test_seq_up = []
        for k in perm:
            a, b = pair_hex[k]
            test_seq_lo.append(a[:3])
            test_seq_lo.append(b[:3])
            test_seq_up.append(a[3:])
            test_seq_up.append(b[3:])
        null_order_lag4.append(count_lag4_matches(test_seq_lo) + count_lag4_matches(test_seq_up))

    null_order_lag4 = np.array(null_order_lag4)
    print(f"\n  Randomize pair ordering, keep orientation:")
    print(f"  KW combined lag-4: {kw_combined_lag4}")
    print(f"  Null: {np.mean(null_order_lag4):.2f} ± {np.std(null_order_lag4):.2f}")
    print(f"  p(≥KW): {np.mean(null_order_lag4 >= kw_combined_lag4):.4f}")

    # Test 3: Randomize BOTH pair ordering and orientation
    null_both_lag4 = []
    for _ in range(N_TRIALS):
        perm = RNG.permutation(32)
        test_seq_lo = []
        test_seq_up = []
        for k in perm:
            a, b = pair_hex[k]
            if RNG.random() < 0.5:
                a, b = b, a
            test_seq_lo.append(a[:3])
            test_seq_lo.append(b[:3])
            test_seq_up.append(a[3:])
            test_seq_up.append(b[3:])
        null_both_lag4.append(count_lag4_matches(test_seq_lo) + count_lag4_matches(test_seq_up))

    null_both_lag4 = np.array(null_both_lag4)
    print(f"\n  Randomize both pair ordering and orientation:")
    print(f"  KW combined lag-4: {kw_combined_lag4}")
    print(f"  Null: {np.mean(null_both_lag4):.2f} ± {np.std(null_both_lag4):.2f}")
    print(f"  p(≥KW): {np.mean(null_both_lag4 >= kw_combined_lag4):.4f}")

    # ── AA vs BB contribution ──
    print(f"\n  --- AA vs BB: which drives lag-4? ---")
    # Under null (random pair ordering), what are AA and BB separately?
    null_aa = []
    null_bb = []
    for _ in range(min(N_TRIALS, 50000)):
        perm = RNG.permutation(32)
        test_seq_lo = []
        test_seq_up = []
        for k in perm:
            a, b = pair_hex[k]
            test_seq_lo.append(a[:3])
            test_seq_lo.append(b[:3])
            test_seq_up.append(a[3:])
            test_seq_up.append(b[3:])

        aa = 0
        bb = 0
        for j in range(30):
            p1a = 2*j
            p2a = 2*(j+2)
            p1b = 2*j + 1
            p2b = 2*(j+2) + 1
            if p2a < 64:
                if test_seq_lo[p1a] == test_seq_lo[p2a]: aa += 1
                if test_seq_up[p1a] == test_seq_up[p2a]: aa += 1
            if p2b < 64:
                if test_seq_lo[p1b] == test_seq_lo[p2b]: bb += 1
                if test_seq_up[p1b] == test_seq_up[p2b]: bb += 1
        null_aa.append(aa)
        null_bb.append(bb)

    null_aa = np.array(null_aa)
    null_bb = np.array(null_bb)

    kw_aa = aa_matches_lo + aa_matches_up
    kw_bb = bb_matches_lo + bb_matches_up

    print(f"  KW AA: {kw_aa}, null: {np.mean(null_aa):.2f} ± {np.std(null_aa):.2f}, "
          f"p(≥KW): {np.mean(null_aa >= kw_aa):.4f}")
    print(f"  KW BB: {kw_bb}, null: {np.mean(null_bb):.2f} ± {np.std(null_bb):.2f}, "
          f"p(≥KW): {np.mean(null_bb >= kw_bb):.4f}")

    # ── Pair-level trigram sharing ──
    print(f"\n  --- Pair-level trigram sharing between pairs k and k+2 ---")
    print(f"  For each pair k, does pair k share any trigram with pair k+2?")
    print(f"  (A pair 'has' a trigram if either member uses it as lower or upper)")

    for k in range(30):
        p1 = pair_data[k]
        p2 = pair_data[k+2]
        tris1 = {p1['a']['lo'], p1['a']['up'], p1['b']['lo'], p1['b']['up']}
        tris2 = {p2['a']['lo'], p2['a']['up'], p2['b']['lo'], p2['b']['up']}
        shared = tris1 & tris2
        shared_names = [tri_name(t) for t in shared]
        if shared:
            print(f"    P{k+1}↔P{k+3}: shared={shared_names}")

    # ── Orbit pattern in lag-4 ──
    print(f"\n  --- Orbit (generator) pattern at lag-4 matches ---")
    print(f"  Does pair k and pair k+2 sharing a trigram correlate with generator type?")

    gen_at_match = []
    gen_at_nonmatch = []
    for k in range(30):
        p1a = 2*k
        p2a = 2*(k+2)
        has_match = (lo_seq[p1a] == lo_seq[p2a]) or (up_seq[p1a] == up_seq[p2a])
        if has_match:
            gen_at_match.append(pair_data[k]['gen'])
            gen_at_match.append(pair_data[k+2]['gen'])
        else:
            gen_at_nonmatch.append(pair_data[k]['gen'])
            gen_at_nonmatch.append(pair_data[k+2]['gen'])

    print(f"  Generators at lag-4 AA-matching pairs: {dict(Counter(gen_at_match))}")
    print(f"  Generators at non-matching pairs: {dict(Counter(gen_at_nonmatch))}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK D: Corridors × complementary coverage
# ══════════════════════════════════════════════════════════════════════════════

def task_d(corridors):
    print("\n" + "=" * 90)
    print("TASK D: CORRIDORS × COMPLEMENTARY COVERAGE")
    print("=" * 90)

    # For each pair, determine if it's in a corridor
    pairs_in_corridors = set()
    for c in corridors:
        for p in c['positions']:
            pairs_in_corridors.add((p-1)//2)  # 0-indexed pair

    print(f"\n  Pairs in at least one corridor: {len(pairs_in_corridors)}/32")
    print(f"  Pairs: {sorted(k+1 for k in pairs_in_corridors)}")

    pairs_outside = set(range(32)) - pairs_in_corridors
    print(f"  Pairs outside all corridors: {len(pairs_outside)}/32")
    print(f"  Pairs: {sorted(k+1 for k in pairs_outside)}")

    # Cross-tabulate: corridor membership × fragility class
    print(f"\n  --- Corridor membership × fragility class ---")
    frag_in = Counter(fragility(k) for k in pairs_in_corridors)
    frag_out = Counter(fragility(k) for k in pairs_outside)

    print(f"  {'':>15s}  {'KW-dom':>8s}  {'trade-off':>10s}  {'S2':>5s}  {'Total':>6s}")
    n_in = len(pairs_in_corridors)
    n_out = len(pairs_outside)
    print(f"  {'In corridor':>15s}  "
          f"{frag_in.get('KW-dom',0):>8d}  "
          f"{frag_in.get('trade-off',0):>10d}  "
          f"{frag_in.get('S2',0):>5d}  {n_in:>6d}")
    print(f"  {'Outside':>15s}  "
          f"{frag_out.get('KW-dom',0):>8d}  "
          f"{frag_out.get('trade-off',0):>10d}  "
          f"{frag_out.get('S2',0):>5d}  {n_out:>6d}")

    # Cross-tabulate: corridor membership × meaning confidence
    print(f"\n  --- Corridor membership × meaning confidence ---")
    conf_in = Counter(meaning_conf.get(k+1, '?') for k in pairs_in_corridors)
    conf_out = Counter(meaning_conf.get(k+1, '?') for k in pairs_outside)

    print(f"  {'':>15s}  {'Clear':>7s}  {'Suggestive':>11s}  {'Total':>6s}")
    print(f"  {'In corridor':>15s}  "
          f"{conf_in.get('Clear',0):>7d}  "
          f"{conf_in.get('Suggestive',0):>11d}  {n_in:>6d}")
    print(f"  {'Outside':>15s}  "
          f"{conf_out.get('Clear',0):>7d}  "
          f"{conf_out.get('Suggestive',0):>11d}  {n_out:>6d}")

    # Rates
    if n_in > 0:
        print(f"\n  In corridor:  Clear rate = {100*conf_in.get('Clear',0)/n_in:.0f}%, "
              f"trade-off rate = {100*frag_in.get('trade-off',0)/n_in:.0f}%")
    if n_out > 0:
        print(f"  Outside:      Clear rate = {100*conf_out.get('Clear',0)/n_out:.0f}%, "
              f"trade-off rate = {100*frag_out.get('trade-off',0)/n_out:.0f}%")

    # Detailed pair-by-pair table
    print(f"\n  --- Full pair table with corridor membership ---")
    print(f"  {'P':>3s}  {'Name':>20s}  {'In corr?':>8s}  {'Frag':>10s}  {'Conf':>10s}  "
          f"{'Corridors':>30s}")
    print("  " + "-" * 95)

    for k in range(32):
        in_corr = k in pairs_in_corridors
        which_corridors = []
        for c in corridors:
            for p in c['positions']:
                if (p-1)//2 == k:
                    which_corridors.append(f"{c['role'].upper()[:1]}:{c['tri_name']}")
                    break
        corr_str = ', '.join(set(which_corridors))
        name = f"{pair_data[k]['a']['name']}/{pair_data[k]['b']['name']}"
        print(f"  {k+1:3d}  {name:>20s}  {'yes' if in_corr else 'no':>8s}  "
              f"{fragility(k):>10s}  {meaning_conf.get(k+1,'?'):>10s}  "
              f"{corr_str:>30s}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK E: The trigram persistence profile — what makes a corridor?
# ══════════════════════════════════════════════════════════════════════════════

def task_e():
    print("\n" + "=" * 90)
    print("TASK E: TRIGRAM PERSISTENCE PROFILE")
    print("=" * 90)

    # For each of 8 trigrams × 2 roles, count the number of lag-4 chains
    # and total chain length. This is the trigram's "corridor score"
    lo_seq = [h['lo'] for h in hexagrams]
    up_seq = [h['up'] for h in hexagrams]

    print(f"\n  --- Trigram persistence by role ---")
    print(f"  Persistence = fraction of possible lag-4 matches that are actual matches")
    print(f"  Each trigram appears 8 times. Maximum lag-4 matches among those 8 positions")
    print(f"  depends on spacing. If positions are p1,p2,...,p8 (sorted),")
    print(f"  a match at (pi, pj) requires pj - pi = 4.")

    for role, seq in [('lo', lo_seq), ('up', up_seq)]:
        print(f"\n  Role: {role.upper()}")
        for tri in sorted(TRIGRAM_INFO.keys()):
            positions = sorted(i+1 for i, t in enumerate(seq) if t == tri)
            # Count lag-4 matches among these positions
            pos_set = set(positions)
            matches = sum(1 for p in positions if (p+4) in pos_set and p+4 <= 64)
            # Max possible matches = how many positions have position+4 also occupied?
            # This depends on the specific positions
            print(f"    {tri_name(tri):>8s}: positions={positions}, "
                  f"lag-4 internal matches={matches}")

    # ── Which pairs of consecutive pairs share the most trigrams? ──
    print(f"\n  --- Trigram sharing density across the sequence ---")
    print(f"  For consecutive pair-pairs (k, k+1): count of trigrams shared between the")
    print(f"  4 hexagrams of pair k and the 4 hexagrams of pair k+1")

    for k in range(31):
        p1 = pair_data[k]
        p2 = pair_data[k+1]
        tris1 = set()
        for h in [p1['a'], p1['b']]:
            tris1.add(('lo', h['lo']))
            tris1.add(('up', h['up']))
        tris2 = set()
        for h in [p2['a'], p2['b']]:
            tris2.add(('lo', h['lo']))
            tris2.add(('up', h['up']))
        shared = tris1 & tris2
        shared_names = [(r, tri_name(t)) for r, t in shared]
        b = bridge_data[k]
        pres = "PRES" if b['lo_shared'] or b['up_shared'] else ""
        # Also note if the shared trigrams include the corridor trigram
        print(f"    B{k+1:2d} (P{k+1}→P{k+2}): shared={(shared_names)} "
              f"kernel={b['kernel']} {pres}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK F: Corridor meaning characterization
# ══════════════════════════════════════════════════════════════════════════════

def task_f(corridors):
    print("\n" + "=" * 90)
    print("TASK F: CORRIDOR MEANING CHARACTERIZATION")
    print("=" * 90)

    # For the major corridors (length ≥ 3), list the hexagrams with their
    # trigram decomposition and developmental context
    major = [c for c in corridors if c['length'] >= 3]

    for c in major:
        print(f"\n  ═══ {c['role'].upper()} {c['tri_name']}{tri_sym(c['tri'])} CORRIDOR "
              f"(positions {c['positions'][0]}–{c['positions'][-1]}) ═══")

        for p in c['positions']:
            h = hexagrams[p-1]
            pair_k = (p-1)//2
            is_first = (p-1) % 2 == 0
            partner_idx = (p-1) ^ 1  # XOR to get partner
            partner = hexagrams[partner_idx]

            # Mark whether this hex's corridor-trigram is in the expected role
            if c['role'] == 'lo':
                has_corridor_tri = (h['lo'] == c['tri'])
            else:
                has_corridor_tri = (h['up'] == c['tri'])

            pos_label = "1st" if is_first else "2nd"
            print(f"    Pos {p:2d} (P{pair_k+1}, {pos_label}): "
                  f"#{h['num']:2d} {h['name']:12s} "
                  f"lo={h['lo_name']:>8s} up={h['up_name']:>8s}  "
                  f"{'✓' if has_corridor_tri else '✗'} corridor tri in {c['role']}")

        # The developmental arc
        print(f"\n    Developmental arc:")
        hex_names = [hexagrams[p-1]['name'] for p in c['positions']]
        pair_names = []
        seen_pairs = set()
        for p in c['positions']:
            pk = (p-1)//2
            if pk not in seen_pairs:
                seen_pairs.add(pk)
                pair_names.append(
                    f"P{pk+1}({pair_data[pk]['a']['name']}/{pair_data[pk]['b']['name']})")
        print(f"    Hexagrams: {', '.join(hex_names)}")
        print(f"    Pairs: {', '.join(pair_names)}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK G: Extended lag analysis — lag-2 at pair level
# ══════════════════════════════════════════════════════════════════════════════

def task_g():
    print("\n" + "=" * 90)
    print("TASK G: EXTENDED LAG ANALYSIS — PAIR-LEVEL STRUCTURE")
    print("=" * 90)

    # Lag-4 at the hexagram level = lag-2 at the pair level
    # Let's define pair-level trigram sets and analyze pair-to-pair periodicity

    # Each pair contributes 4 trigram slots: (a_lo, a_up, b_lo, b_up)
    # But within a pair, the cross-trigram theorem forces a and b to differ
    # in both lo and up. So a pair's "trigram profile" = {a_lo, a_up, b_lo, b_up}
    # with a_lo ≠ b_lo and a_up ≠ b_up.

    print(f"\n  --- Pair trigram profiles ---")
    print(f"  {'P':>3s}  {'1st Lo':>8s} {'1st Up':>8s}  {'2nd Lo':>8s} {'2nd Up':>8s}  "
          f"{'Unique tris':>11s}  {'Gen':>4s}")
    print("  " + "-" * 65)

    for k in range(32):
        a = pair_data[k]['a']
        b = pair_data[k]['b']
        tris = {a['lo'], a['up'], b['lo'], b['up']}
        tri_list = [tri_name(t) for t in sorted(tris)]
        print(f"  {k+1:3d}  {a['lo_name']:>8s} {a['up_name']:>8s}  "
              f"{b['lo_name']:>8s} {b['up_name']:>8s}  "
              f"{len(tris):>11d}  {pair_data[k]['gen']:>4s}")

    # At pair level: pair k and pair k+2 sharing
    print(f"\n  --- Pair-level lag-2 sharing ---")
    print(f"  Pairs k and k+2: how many of 4 trigram slots match?")

    total_slot_matches = 0
    total_possible = 0
    for k in range(30):
        a1, b1 = pair_data[k]['a'], pair_data[k]['b']
        a2, b2 = pair_data[k+2]['a'], pair_data[k+2]['b']

        # Slot-by-slot comparison
        matches = []
        if a1['lo'] == a2['lo']: matches.append('1st_lo')
        if a1['up'] == a2['up']: matches.append('1st_up')
        if b1['lo'] == b2['lo']: matches.append('2nd_lo')
        if b1['up'] == b2['up']: matches.append('2nd_up')

        total_slot_matches += len(matches)
        total_possible += 4

        if matches:
            match_str = ', '.join(matches)
            print(f"    P{k+1}↔P{k+3}: {len(matches)} matches [{match_str}]")

    print(f"\n  Total slot matches: {total_slot_matches}/{total_possible} "
          f"= {total_slot_matches/total_possible:.3f}")
    print(f"  Expected under random: {total_possible/8:.1f} = {1/8:.3f}")

    # MC significance
    null_slot_matches = []
    for _ in range(min(N_TRIALS, 50000)):
        perm = RNG.permutation(32)
        total = 0
        for k in range(30):
            pk1 = perm[k]
            pk2 = perm[k+2] if k+2 < 32 else perm[k+2-32]
            if k+2 >= 32:
                continue
            pk2 = perm[k+2]
            a1 = pair_data[pk1]['a']
            b1 = pair_data[pk1]['b']
            a2 = pair_data[pk2]['a']
            b2 = pair_data[pk2]['b']

            if a1['lo'] == a2['lo']: total += 1
            if a1['up'] == a2['up']: total += 1
            if b1['lo'] == b2['lo']: total += 1
            if b1['up'] == b2['up']: total += 1

        null_slot_matches.append(total)

    null_slot_matches = np.array(null_slot_matches)
    print(f"\n  MC significance (pair-level lag-2 slot matches):")
    print(f"  KW: {total_slot_matches}, "
          f"null: {np.mean(null_slot_matches):.2f} ± {np.std(null_slot_matches):.2f}")
    print(f"  p(≥KW): {np.mean(null_slot_matches >= total_slot_matches):.4f}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    corridors = task_a()
    task_b(corridors)
    task_c()
    task_d(corridors)
    task_e()
    task_f(corridors)
    task_g()

    print("\n" + "=" * 90)
    print("ROUND 4 ANALYSIS COMPLETE")
    print("=" * 90)
