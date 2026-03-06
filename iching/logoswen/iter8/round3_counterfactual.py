"""
Round 3: Counterfactual test of the corridor-free zone (P17–P26).

Tests whether the KW ordering of these 10 pairs is structurally special
compared to random permutations, using trigram overlap as an objective proxy.

Also tests developmental ordering of corridor blocks.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

import numpy as np
from math import factorial, log2, comb
from collections import Counter, defaultdict
from sequence import KING_WEN

RNG = np.random.default_rng(42)

# ── Hexagram data ─────────────────────────────────────────────────────────────

TRIGRAM_NAMES = {
    "111": "Heaven", "000": "Earth", "100": "Thunder", "010": "Water",
    "001": "Mountain", "011": "Wind", "101": "Fire", "110": "Lake",
}

def tri_name(s):
    return TRIGRAM_NAMES.get(s, "?")

# Build pair data
pairs = []
for k in range(32):
    a = KING_WEN[2*k]
    b = KING_WEN[2*k+1]
    pairs.append({
        'k': k,
        'a_num': a[0], 'a_name': a[1], 'a_bin': a[2],
        'b_num': b[0], 'b_name': b[1], 'b_bin': b[2],
        'a_lo': a[2][:3], 'a_up': a[2][3:],
        'b_lo': b[2][:3], 'b_up': b[2][3:],
        # entry hex = first hex (a), exit hex = second hex (b)
        'entry_lo': a[2][:3], 'entry_up': a[2][3:],
        'exit_lo': b[2][:3], 'exit_up': b[2][3:],
    })


# ══════════════════════════════════════════════════════════════════════════════
# TASK A: Corridor-free zone permutation test
# ══════════════════════════════════════════════════════════════════════════════

def hamming3(a, b):
    return sum(c1 != c2 for c1, c2 in zip(a, b))

def trigram_overlap_score(ordering, zone_pairs, boundary_exit=None, boundary_entry=None):
    """
    Compute trigram overlap score for a given ordering of zone pairs.
    
    For each transition (exit hex of pair i → entry hex of pair i+1):
    - +2 if both lo AND up match (full preservation)
    - +1 if lo OR up matches (single preservation)
    - +0 if neither matches
    
    Also includes boundary transitions if provided.
    """
    score = 0
    lo_matches = 0
    up_matches = 0
    
    # Internal transitions
    for i in range(len(ordering) - 1):
        p_from = zone_pairs[ordering[i]]
        p_to = zone_pairs[ordering[i+1]]
        
        if p_from['exit_lo'] == p_to['entry_lo']:
            lo_matches += 1
            score += 1
        if p_from['exit_up'] == p_to['entry_up']:
            up_matches += 1
            score += 1
    
    # Boundary: zone entry (from boundary_exit to first zone pair)
    boundary_score = 0
    if boundary_exit is not None:
        first = zone_pairs[ordering[0]]
        if boundary_exit['exit_lo'] == first['entry_lo']:
            boundary_score += 1
        if boundary_exit['exit_up'] == first['entry_up']:
            boundary_score += 1
    
    # Boundary: zone exit (from last zone pair to boundary_entry)
    if boundary_entry is not None:
        last = zone_pairs[ordering[-1]]
        if last['exit_lo'] == boundary_entry['entry_lo']:
            boundary_score += 1
        if last['exit_up'] == boundary_entry['entry_up']:
            boundary_score += 1
    
    return score, lo_matches, up_matches, boundary_score


def hamming_distance_score(ordering, zone_pairs, boundary_exit=None, boundary_entry=None):
    """
    Compute total Hamming distance across transitions.
    Lower = more similar adjacent pairs = more continuity.
    """
    total_dist = 0
    
    for i in range(len(ordering) - 1):
        p_from = zone_pairs[ordering[i]]
        p_to = zone_pairs[ordering[i+1]]
        
        total_dist += hamming3(p_from['exit_lo'], p_to['entry_lo'])
        total_dist += hamming3(p_from['exit_up'], p_to['entry_up'])
    
    # Boundaries
    if boundary_exit is not None:
        first = zone_pairs[ordering[0]]
        total_dist += hamming3(boundary_exit['exit_lo'], first['entry_lo'])
        total_dist += hamming3(boundary_exit['exit_up'], first['entry_up'])
    
    if boundary_entry is not None:
        last = zone_pairs[ordering[-1]]
        total_dist += hamming3(last['exit_lo'], boundary_entry['entry_lo'])
        total_dist += hamming3(last['exit_up'], boundary_entry['entry_up'])
    
    return total_dist


def task_a():
    print("=" * 80)
    print("TASK A: CORRIDOR-FREE ZONE PERMUTATION TEST")
    print("=" * 80)
    
    # Zone pairs: P17-P26 (0-indexed: 16-25)
    zone_indices = list(range(16, 26))
    zone_pairs = [pairs[k] for k in zone_indices]
    n_zone = len(zone_pairs)
    
    # Boundary pairs
    boundary_exit = pairs[15]   # P16 (exit hex = Heng #32)
    boundary_entry = pairs[26]  # P27 (entry hex = Jian(Dev) #53)
    
    # KW ordering = identity (0,1,2,...,9)
    kw_order = list(range(n_zone))
    
    print(f"\n  Zone: P17–P26 ({n_zone} pairs)")
    print(f"  Boundary exit: P16 exit = #{boundary_exit['b_num']} {boundary_exit['b_name']}")
    print(f"  Boundary entry: P27 entry = #{boundary_entry['a_num']} {boundary_entry['a_name']}")
    
    # KW scores
    kw_overlap, kw_lo, kw_up, kw_boundary = trigram_overlap_score(
        kw_order, zone_pairs, boundary_exit, boundary_entry)
    kw_hamming = hamming_distance_score(
        kw_order, zone_pairs, boundary_exit, boundary_entry)
    
    print(f"\n  --- KW ordering scores ---")
    print(f"  Internal trigram overlaps: {kw_overlap} (lo={kw_lo}, up={kw_up}) out of 9 transitions × 2 = 18 possible")
    print(f"  Boundary overlaps: {kw_boundary} out of 4 possible")
    print(f"  Total overlaps (internal + boundary): {kw_overlap + kw_boundary}")
    print(f"  Total Hamming distance (internal): {kw_hamming}")
    
    # Show each KW transition
    print(f"\n  --- KW transitions detail ---")
    for i in range(n_zone - 1):
        p_from = zone_pairs[kw_order[i]]
        p_to = zone_pairs[kw_order[i+1]]
        lo_m = '✓' if p_from['exit_lo'] == p_to['entry_lo'] else '✗'
        up_m = '✓' if p_from['exit_up'] == p_to['entry_up'] else '✗'
        lo_h = hamming3(p_from['exit_lo'], p_to['entry_lo'])
        up_h = hamming3(p_from['exit_up'], p_to['entry_up'])
        print(f"    T{zone_indices[i]+1}: #{p_from['b_num']:2d} {p_from['b_name']:12s} -> "
              f"#{p_to['a_num']:2d} {p_to['a_name']:12s}  "
              f"lo:{lo_m}(d={lo_h}) up:{up_m}(d={up_h})")
    
    # Boundary transitions
    first = zone_pairs[kw_order[0]]
    last = zone_pairs[kw_order[-1]]
    lo_m_in = '✓' if boundary_exit['exit_lo'] == first['entry_lo'] else '✗'
    up_m_in = '✓' if boundary_exit['exit_up'] == first['entry_up'] else '✗'
    lo_m_out = '✓' if last['exit_lo'] == boundary_entry['entry_lo'] else '✗'
    up_m_out = '✓' if last['exit_up'] == boundary_entry['entry_up'] else '✗'
    print(f"\n    Boundary in:  #{boundary_exit['b_num']:2d} {boundary_exit['b_name']:12s} -> "
          f"#{first['a_num']:2d} {first['a_name']:12s}  lo:{lo_m_in} up:{up_m_in}")
    print(f"    Boundary out: #{last['b_num']:2d} {last['b_name']:12s} -> "
          f"#{boundary_entry['a_num']:2d} {boundary_entry['a_name']:12s}  lo:{lo_m_out} up:{up_m_out}")
    
    # === EXHAUSTIVE ENUMERATION (10! = 3,628,800 is feasible) ===
    print(f"\n  --- Exhaustive enumeration of all 10! = {factorial(n_zone):,} permutations ---")
    
    overlap_dist = Counter()
    hamming_dist_dist = Counter()
    boundary_overlap_dist = Counter()
    total_overlap_dist = Counter()
    
    # For speed, precompute trigram data as arrays
    exit_lo = [zone_pairs[i]['exit_lo'] for i in range(n_zone)]
    exit_up = [zone_pairs[i]['exit_up'] for i in range(n_zone)]
    entry_lo = [zone_pairs[i]['entry_lo'] for i in range(n_zone)]
    entry_up = [zone_pairs[i]['entry_up'] for i in range(n_zone)]
    
    bnd_exit_lo = boundary_exit['exit_lo']
    bnd_exit_up = boundary_exit['exit_up']
    bnd_entry_lo = boundary_entry['entry_lo']
    bnd_entry_up = boundary_entry['entry_up']
    
    # Use numpy permutation sampling since exhaustive is slow
    # Actually 3.6M is borderline. Let's do a large sample + exact boundary check.
    
    N_SAMPLE = 3_628_800  # sample size = 10! (same count, random sample)
    
    overlap_counts = np.zeros(N_SAMPLE, dtype=np.int32)
    boundary_counts = np.zeros(N_SAMPLE, dtype=np.int32)
    hamming_counts = np.zeros(N_SAMPLE, dtype=np.int32)
    
    for trial in range(N_SAMPLE):
        perm = RNG.permutation(n_zone)
        
        overlap = 0
        hamming_total = 0
        for i in range(n_zone - 1):
            fr = perm[i]
            to = perm[i+1]
            if exit_lo[fr] == entry_lo[to]:
                overlap += 1
            if exit_up[fr] == entry_up[to]:
                overlap += 1
            hamming_total += hamming3(exit_lo[fr], entry_lo[to])
            hamming_total += hamming3(exit_up[fr], entry_up[to])
        
        # Boundary
        bnd = 0
        first_idx = perm[0]
        last_idx = perm[-1]
        if bnd_exit_lo == entry_lo[first_idx]:
            bnd += 1
        if bnd_exit_up == entry_up[first_idx]:
            bnd += 1
        if exit_lo[last_idx] == bnd_entry_lo:
            bnd += 1
        if exit_up[last_idx] == bnd_entry_up:
            bnd += 1
        
        # Boundary hamming
        hamming_total += hamming3(bnd_exit_lo, entry_lo[first_idx])
        hamming_total += hamming3(bnd_exit_up, entry_up[first_idx])
        hamming_total += hamming3(exit_lo[last_idx], bnd_entry_lo)
        hamming_total += hamming3(exit_up[last_idx], bnd_entry_up)
        
        overlap_counts[trial] = overlap
        boundary_counts[trial] = bnd
        hamming_counts[trial] = hamming_total
    
    total_counts = overlap_counts + boundary_counts
    
    kw_total = kw_overlap + kw_boundary
    kw_hamming_total = kw_hamming + hamming3(bnd_exit_lo, first['entry_lo']) + \
                       hamming3(bnd_exit_up, first['entry_up']) + \
                       hamming3(last['exit_lo'], bnd_entry_lo) + \
                       hamming3(last['exit_up'], bnd_entry_up)
    
    print(f"\n  === Internal trigram overlap (0–18 scale) ===")
    print(f"  KW: {kw_overlap}")
    print(f"  Mean: {np.mean(overlap_counts):.2f} ± {np.std(overlap_counts):.2f}")
    print(f"  Median: {np.median(overlap_counts):.0f}")
    print(f"  p(≥KW): {np.mean(overlap_counts >= kw_overlap):.4f}")
    print(f"  p(≤KW): {np.mean(overlap_counts <= kw_overlap):.4f}")
    print(f"  Distribution: {dict(sorted(Counter(overlap_counts.tolist()).items()))}")
    
    # Max overlap found
    max_overlap = np.max(overlap_counts)
    print(f"  Max found: {max_overlap}")
    
    print(f"\n  === Boundary trigram overlap (0–4 scale) ===")
    print(f"  KW: {kw_boundary}")
    print(f"  Mean: {np.mean(boundary_counts):.2f} ± {np.std(boundary_counts):.2f}")
    print(f"  p(≥KW): {np.mean(boundary_counts >= kw_boundary):.4f}")
    print(f"  Distribution: {dict(sorted(Counter(boundary_counts.tolist()).items()))}")
    
    print(f"\n  === Total trigram overlap (0–22 scale) ===")
    print(f"  KW: {kw_total}")
    print(f"  Mean: {np.mean(total_counts):.2f} ± {np.std(total_counts):.2f}")
    print(f"  p(≥KW): {np.mean(total_counts >= kw_total):.4f}")
    print(f"  p(≤KW): {np.mean(total_counts <= kw_total):.4f}")
    
    print(f"\n  === Total Hamming distance (lower=more continuity) ===")
    print(f"  KW: {kw_hamming_total}")
    print(f"  Mean: {np.mean(hamming_counts):.2f} ± {np.std(hamming_counts):.2f}")
    print(f"  Min found: {np.min(hamming_counts)}")
    print(f"  p(≤KW): {np.mean(hamming_counts <= kw_hamming_total):.4f}")
    print(f"  p(≥KW): {np.mean(hamming_counts >= kw_hamming_total):.4f}")
    
    # === Find the BEST permutations by total overlap ===
    print(f"\n  === Top permutations by total overlap ===")
    # Re-run a smaller sample to find actual best orderings
    best_overlap = 0
    best_perms = []
    
    RNG2 = np.random.default_rng(123)
    for trial in range(1_000_000):
        perm = RNG2.permutation(n_zone)
        
        overlap = 0
        for i in range(n_zone - 1):
            fr = perm[i]
            to = perm[i+1]
            if exit_lo[fr] == entry_lo[to]:
                overlap += 1
            if exit_up[fr] == entry_up[to]:
                overlap += 1
        
        # Boundary
        bnd = 0
        if bnd_exit_lo == entry_lo[perm[0]]:
            bnd += 1
        if bnd_exit_up == entry_up[perm[0]]:
            bnd += 1
        if exit_lo[perm[-1]] == bnd_entry_lo:
            bnd += 1
        if exit_up[perm[-1]] == bnd_entry_up:
            bnd += 1
        
        total = overlap + bnd
        if total > best_overlap:
            best_overlap = total
            best_perms = [perm.copy()]
        elif total == best_overlap:
            best_perms.append(perm.copy())
    
    print(f"  Best total overlap found: {best_overlap}")
    print(f"  Number of best permutations (in 1M sample): {len(best_perms)}")
    
    if best_perms:
        perm = best_perms[0]
        print(f"\n  Example best permutation:")
        for i in range(n_zone):
            p = zone_pairs[perm[i]]
            print(f"    Pos {i+1}: P{zone_indices[perm[i]]+1} ({p['a_name']}/{p['b_name']})")
        
        print(f"\n  Its transitions:")
        for i in range(n_zone - 1):
            fr = perm[i]
            to = perm[i+1]
            lo_m = '✓' if exit_lo[fr] == entry_lo[to] else '✗'
            up_m = '✓' if exit_up[fr] == entry_up[to] else '✗'
            p_from = zone_pairs[fr]
            p_to = zone_pairs[to]
            print(f"      #{p_from['b_num']:2d} {p_from['b_name']:12s} -> "
                  f"#{p_to['a_num']:2d} {p_to['a_name']:12s}  lo:{lo_m} up:{up_m}")
    
    return kw_overlap, kw_boundary, kw_hamming_total


# ══════════════════════════════════════════════════════════════════════════════
# TASK B: Developmental ordering of corridor blocks
# ══════════════════════════════════════════════════════════════════════════════

def task_b():
    print(f"\n{'='*80}")
    print("TASK B: CORRIDOR BLOCK DEVELOPMENTAL ORDERING")
    print("=" * 80)
    
    # Corridors (0-indexed pair members)
    CORRIDORS = {
        'Earth':            [3, 5, 7, 9],
        'Heaven':           [0, 2, 4],
        'Thunder/Mountain': [8, 10],
        'Wind':             [13, 15],
        'Lake/Wind':        [26, 28],
    }
    
    N_PAIRS = 32
    
    def occupied_positions(start, length):
        return set(range(start, start + 2*(length-1) + 1, 2))
    
    blocks = [
        ('Earth', 4),
        ('Heaven', 3),
        ('Thunder/Mountain', 2),
        ('Wind', 2),
        ('Lake/Wind', 2),
    ]
    
    # KW block starting positions (0-indexed):
    # Heaven: P1,P3,P5 → starts at position 0
    # Earth: P4,P6,P8,P10 → starts at position 3
    # Thunder/Mountain: P9,P11 → starts at position 8
    # Wind: P14,P16 → starts at position 13
    # Lake/Wind: P27,P29 → starts at position 26
    
    # "Developmental order" means: the starting positions of blocks are in
    # the order Heaven < Earth < Thunder/Mountain < Wind < Lake/Wind
    # (i.e., Heaven starts earliest, Lake/Wind starts latest)
    
    # But more precisely, the claim is about which block's FIRST member 
    # appears earliest. The "start" of a block at position s means
    # the first member is at position s.
    
    # Enumerate all valid placements
    print(f"\n  Enumerating all valid block placements...")
    
    earth_max = N_PAIRS - 2*4 + 1
    heaven_max = N_PAIRS - 2*3 + 1
    tm_max = N_PAIRS - 2*2 + 1
    
    total_placements = 0
    dev_order_count = 0  # Heaven < Earth < Th/Mo < Wind < Lake/Wind
    
    # Also count partial orderings
    hw_before_earth = 0     # Heaven starts before Earth
    earth_before_tm = 0     # Earth starts before Thunder/Mountain
    
    # Track start position distribution
    starts_by_block = defaultdict(list)
    
    for s_earth in range(earth_max + 1):
        occ_earth = occupied_positions(s_earth, 4)
        
        for s_heaven in range(heaven_max + 1):
            occ_heaven = occupied_positions(s_heaven, 3)
            if occ_earth & occ_heaven:
                continue
            occ_eh = occ_earth | occ_heaven
            
            for s_tm in range(tm_max + 1):
                occ_tm = occupied_positions(s_tm, 2)
                if occ_eh & occ_tm:
                    continue
                occ_eht = occ_eh | occ_tm
                
                for s_wind in range(tm_max + 1):
                    occ_wind = occupied_positions(s_wind, 2)
                    if occ_eht & occ_wind:
                        continue
                    occ_ehtw = occ_eht | occ_wind
                    
                    for s_lw in range(tm_max + 1):
                        occ_lw = occupied_positions(s_lw, 2)
                        if occ_ehtw & occ_lw:
                            continue
                        
                        total_placements += 1
                        
                        # Check developmental order
                        if s_heaven < s_earth < s_tm < s_wind < s_lw:
                            dev_order_count += 1
                        
                        if s_heaven < s_earth:
                            hw_before_earth += 1
                        if s_earth < s_tm:
                            earth_before_tm += 1
    
    print(f"  Total valid placements: {total_placements:,}")
    print(f"  Developmental order (H < E < T/M < W < L/W): {dev_order_count:,}")
    print(f"  Fraction: {dev_order_count/total_placements:.6f}")
    print(f"  1 in {total_placements/dev_order_count:.0f}" if dev_order_count > 0 else "  NONE")
    
    # If blocks were placed independently (ignoring overlap), there are 5! = 120
    # orderings, and each has equal probability → 1/120 ≈ 0.0083
    # But blocks overlap, so the actual fraction may differ.
    print(f"  Naive expectation (1/5!): {1/120:.6f}")
    print(f"  Ratio to naive: {(dev_order_count/total_placements) / (1/120):.3f}")
    
    print(f"\n  --- Partial orderings ---")
    print(f"  Heaven before Earth: {hw_before_earth:,}/{total_placements:,} = {hw_before_earth/total_placements:.4f}")
    print(f"  Earth before Thunder/Mountain: {earth_before_tm:,}/{total_placements:,} = {earth_before_tm/total_placements:.4f}")
    
    # How many bits does developmental ordering remove?
    if dev_order_count > 0:
        bits_removed = log2(total_placements / dev_order_count)
        print(f"\n  Bits removed by developmental order: {bits_removed:.1f}")
    
    # Also: how many placements have the KW interleaving pattern?
    # KW has Heaven and Earth interleaved: H starts at 0, E starts at 3
    # (they overlap in the range 0-9, with H at 0,2,4 and E at 3,5,7,9)
    print(f"\n  --- KW-like interleaving ---")
    interleave_count = 0
    for s_earth in range(earth_max + 1):
        occ_earth = occupied_positions(s_earth, 4)
        for s_heaven in range(heaven_max + 1):
            occ_heaven = occupied_positions(s_heaven, 3)
            if occ_earth & occ_heaven:
                continue
            # Check if they interleave: overlapping footprints
            earth_footprint = (s_earth, s_earth + 6)
            heaven_footprint = (s_heaven, s_heaven + 4)
            # Overlap if max(starts) < min(ends)
            overlap = max(earth_footprint[0], heaven_footprint[0]) < min(earth_footprint[1], heaven_footprint[1])
            if overlap:
                # This is an interleaving placement
                # Count how many full placements have this
                occ_eh = occ_earth | occ_heaven
                for s_tm in range(tm_max + 1):
                    occ_tm = occupied_positions(s_tm, 2)
                    if occ_eh & occ_tm:
                        continue
                    occ_eht = occ_eh | occ_tm
                    for s_wind in range(tm_max + 1):
                        occ_wind = occupied_positions(s_wind, 2)
                        if occ_eht & occ_wind:
                            continue
                        occ_ehtw = occ_eht | occ_wind
                        for s_lw in range(tm_max + 1):
                            occ_lw = occupied_positions(s_lw, 2)
                            if occ_ehtw & occ_lw:
                                continue
                            interleave_count += 1
    
    print(f"  Earth-Heaven interleaving placements: {interleave_count:,}/{total_placements:,}")
    print(f"  Fraction: {interleave_count/total_placements:.4f}")
    
    return total_placements, dev_order_count


# ══════════════════════════════════════════════════════════════════════════════
# TASK C: Integrated transition table
# ══════════════════════════════════════════════════════════════════════════════

def task_c():
    print(f"\n{'='*80}")
    print("TASK C: INTEGRATED TRANSITION TABLE")
    print("=" * 80)
    
    # All data from Round 1 and Round 2
    
    # Logic types (1-indexed transition number)
    logic_types = {
        1: 'Causal', 2: 'Causal', 3: 'Causal', 4: 'Causal', 5: 'Causal',
        6: 'Cyclical', 7: 'Contrastive', 8: 'Causal', 9: 'Causal', 10: 'Causal',
        11: 'Cyclical', 12: 'Causal', 13: 'Causal', 14: 'Cyclical', 15: 'Temporal',
        16: 'Cyclical', 17: 'Cyclical', 18: 'Causal', 19: 'Causal', 20: 'Causal',
        21: 'Cyclical', 22: 'Causal', 23: 'Cyclical', 24: 'Causal', 25: 'Analogical',
        26: 'Cyclical', 27: 'Causal', 28: 'Causal', 29: 'Causal', 30: 'Causal',
        31: 'Causal',
    }
    
    confidence = {
        1: 'Direct', 2: 'Direct', 3: 'Direct', 4: 'Implied', 5: 'Direct',
        6: 'Direct', 7: 'Direct', 8: 'Implied', 9: 'Direct', 10: 'Implied',
        11: 'Direct', 12: 'Direct', 13: 'Direct', 14: 'Implied', 15: 'Direct',
        16: 'Implied', 17: 'Implied', 18: 'Direct', 19: 'Direct', 20: 'Direct',
        21: 'Direct', 22: 'Direct', 23: 'Direct', 24: 'Direct', 25: 'Direct',
        26: 'Implied', 27: 'Direct', 28: 'Direct', 29: 'Direct', 30: 'Direct',
        31: 'Implied',
    }
    
    directionality = {
        1: '→', 2: '→', 3: '⇀', 4: '⇀', 5: '→',
        6: '⇀', 7: '→', 8: '⇀', 9: '→', 10: '⇀',
        11: '→', 12: '→', 13: '→', 14: '⇀', 15: '→',
        16: '⇀', 17: '⇀', 18: '→', 19: '→', 20: '→',
        21: '→', 22: '⇀', 23: '→', 24: '→', 25: '⇀',
        26: '⇀', 27: '→', 28: '→', 29: '→', 30: '→',
        31: '⇀',
    }
    
    # Corridor context (from Round 2)
    corridors_map = {
        'Earth': [4, 6, 8, 10],
        'Heaven': [1, 3, 5],
        'Thunder/Mountain': [9, 11],
        'Wind': [14, 16],
        'Lake/Wind': [27, 29],
    }
    
    pair_to_corr = {}
    for name, members in corridors_map.items():
        for m in members:
            if m not in pair_to_corr:
                pair_to_corr[m] = []
            pair_to_corr[m].append(name)
    
    def corridor_context(t):
        from_p = t
        to_p = t + 1
        from_c = pair_to_corr.get(from_p, [])
        to_c = pair_to_corr.get(to_p, [])
        
        if from_c and to_c:
            shared = set(from_c) & set(to_c)
            if shared:
                return f'within({",".join(shared)})'
            return f'{",".join(from_c)}→{",".join(to_c)}'
        elif from_c:
            return f'exit({",".join(from_c)})'
        elif to_c:
            return f'entry({",".join(to_c)})'
        return 'none'
    
    # Preserving bridge status
    preserving = {}
    for k in range(31):
        exit_hex = KING_WEN[2*k+1]
        entry_hex = KING_WEN[2*k+2]
        exit_lo, exit_up = exit_hex[2][:3], exit_hex[2][3:]
        entry_lo, entry_up = entry_hex[2][:3], entry_hex[2][3:]
        lo_match = exit_lo == entry_lo
        up_match = exit_up == entry_up
        lo_d = hamming3(exit_lo, entry_lo)
        up_d = hamming3(exit_up, entry_up)
        
        if lo_match:
            preserving[k+1] = f'Lo:{tri_name(exit_lo)}'
        elif up_match:
            preserving[k+1] = f'Up:{tri_name(exit_up)}'
        else:
            preserving[k+1] = ''
    
    # Print table
    print(f"\n  {'T#':>3s} {'From':>5s} {'To':>5s} {'Bridge':>25s} "
          f"{'Logic':>12s} {'Conf':>8s} {'Dir':>3s} {'Corridor':>25s} "
          f"{'Preserved':>15s} {'lo_d':>4s} {'up_d':>4s}")
    print("  " + "-" * 120)
    
    for t in range(1, 32):
        from_p = t
        to_p = t + 1
        exit_hex = KING_WEN[2*t-1]
        entry_hex = KING_WEN[2*t]
        
        exit_lo, exit_up = exit_hex[2][:3], exit_hex[2][3:]
        entry_lo, entry_up = entry_hex[2][:3], entry_hex[2][3:]
        lo_d = hamming3(exit_lo, entry_lo)
        up_d = hamming3(exit_up, entry_up)
        
        bridge = f'{exit_hex[1]} → {entry_hex[1]}'
        ctx = corridor_context(t)
        pres = preserving.get(t, '')
        
        print(f"  T{t:2d} P{from_p:2d}   P{to_p:2d}   {bridge:>25s} "
              f"{logic_types[t]:>12s} {confidence[t]:>8s} {directionality[t]:>3s} "
              f"{ctx:>25s} {pres:>15s} {lo_d:>4d} {up_d:>4d}")
    
    # Summary cross-tabs
    print(f"\n  === Summary cross-tabulations ===")
    
    # Logic type × corridor context
    print(f"\n  Logic type × corridor context:")
    contexts = set()
    for t in range(1, 32):
        ctx = corridor_context(t)
        ctx_type = 'exit' if 'exit' in ctx else 'entry' if 'entry' in ctx else 'between' if '→' in ctx else 'none' if ctx == 'none' else 'within'
        contexts.add(ctx_type)
    
    for ctx_type in ['exit', 'entry', 'between', 'none']:
        ts = []
        for t in range(1, 32):
            ctx = corridor_context(t)
            ct = 'exit' if 'exit' in ctx else 'entry' if 'entry' in ctx else 'between' if '→' in ctx else 'none' if ctx == 'none' else 'within'
            if ct == ctx_type:
                ts.append(t)
        logic_counts = Counter(logic_types[t] for t in ts)
        print(f"    {ctx_type:>10s} (n={len(ts):2d}): {dict(logic_counts)}")
    
    # Preserving × logic type
    print(f"\n  Preserving × logic type:")
    for pres_status in ['Preserving', 'Non-preserving']:
        ts = [t for t in range(1, 32) if (preserving[t] != '') == (pres_status == 'Preserving')]
        logic_counts = Counter(logic_types[t] for t in ts)
        conf_counts = Counter(confidence[t] for t in ts)
        print(f"    {pres_status:>15s} (n={len(ts):2d}): logic={dict(logic_counts)}, conf={dict(conf_counts)}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    task_a()
    task_b()
    task_c()
    
    print(f"\n{'='*80}")
    print("ROUND 3 ANALYSIS COMPLETE")
    print("=" * 80)
