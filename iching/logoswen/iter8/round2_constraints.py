"""
Round 2: Pair ordering degrees of freedom — how many orderings preserve corridors?

Corridors (from iter7):
  Earth (lo+up): {P4, P6, P8, P10} — consecutive even-spaced (spacing-2 at pair level)
  Heaven (lo):   {P1, P3, P5}      — consecutive even-spaced
  Thunder/Mountain: {P9, P11}      — consecutive even-spaced
  Wind (lo):     {P14, P16}        — consecutive even-spaced  
  Lake/Wind:     {P27, P29}        — consecutive even-spaced

A corridor requires its member pairs to occupy positions with spacing exactly 2
in the pair ordering (i.e., positions k, k+2, k+4, ...).

Question: How many of 32! pair orderings preserve all corridor structures?
And: what is the internal permutation freedom within corridors?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

import numpy as np
from math import factorial, log2
from itertools import permutations
from collections import defaultdict

# ── Corridor definitions ──────────────────────────────────────────────────────
# 0-indexed pair indices

CORRIDORS = {
    'Earth':            [3, 5, 7, 9],      # P4, P6, P8, P10
    'Heaven':           [0, 2, 4],          # P1, P3, P5
    'Thunder/Mountain': [8, 10],            # P9, P11
    'Wind':             [13, 15],           # P14, P16
    'Lake/Wind':        [26, 28],           # P27, P29
}

N_PAIRS = 32

# ── Analytical computation ────────────────────────────────────────────────────

def analytical_count():
    """
    Count orderings that preserve corridor structure analytically.
    
    A corridor of length L must occupy L positions with pairwise spacing of 2,
    i.e., positions {s, s+2, s+4, ..., s+2(L-1)} for some starting position s.
    
    The corridors are:
      Earth (L=4): footprint width = 2*3+1 = 7 positions  
      Heaven (L=3): footprint width = 2*2+1 = 5 positions
      Thunder/Mountain (L=2): footprint = 3 positions
      Wind (L=2): footprint = 3 positions
      Lake/Wind (L=2): footprint = 3 positions
    
    Corridors can interleave: one corridor's members occupy even-indexed positions
    within its footprint, and another corridor can use the odd positions.
    
    Method: enumerate by placing corridor blocks sequentially, counting valid placements.
    Since the corridors are disjoint in pairs, we can use a slot-assignment approach.
    """
    print("=" * 80)
    print("ANALYTICAL CORRIDOR CONSTRAINT COUNT")
    print("=" * 80)
    
    corridor_pairs = set()
    for name, members in CORRIDORS.items():
        corridor_pairs.update(members)
    
    non_corridor = set(range(N_PAIRS)) - corridor_pairs
    n_corridor = len(corridor_pairs)
    n_free = len(non_corridor)
    
    print(f"\nCorridor pairs: {n_corridor}")
    print(f"Non-corridor pairs: {n_free}")
    
    # Internal permutations: within each corridor, the members can be reordered
    # while maintaining the spacing-2 constraint.
    # A corridor of length L has L! internal orderings.
    internal_perms = 1
    for name, members in CORRIDORS.items():
        L = len(members)
        internal_perms *= factorial(L)
        print(f"  {name}: {L}! = {factorial(L)}")
    print(f"  Total internal permutations: {internal_perms}")
    
    # The non-corridor pairs can fill any remaining slots: n_free! orderings
    free_perms = factorial(n_free)
    print(f"  Non-corridor permutations: {n_free}! = {free_perms:.4e}")
    
    return internal_perms, free_perms, n_corridor, n_free


def monte_carlo_count():
    """
    Monte Carlo estimation of corridor-preserving orderings.
    """
    print(f"\n{'='*80}")
    print("MONTE CARLO CORRIDOR CONSTRAINT ESTIMATION")
    print("=" * 80)
    
    N_TRIALS = 10_000_000
    RNG = np.random.default_rng(42)
    
    corridor_list = [(name, np.array(members)) for name, members in CORRIDORS.items()]
    
    # For speed: vectorized check
    def check_corridors_fast(ordering):
        pos = np.empty(N_PAIRS, dtype=np.int32)
        for i in range(N_PAIRS):
            pos[ordering[i]] = i
        
        for name, members in corridor_list:
            positions = np.sort(pos[members])
            diffs = np.diff(positions)
            if not np.all(diffs == 2):
                return False
        return True
    
    count_any = 0       # corridors at spacing-2, any internal order
    count_kw = 0        # corridors at spacing-2, KW internal order
    
    # KW internal order: members listed in CORRIDORS are already in KW order
    for trial in range(N_TRIALS):
        ordering = RNG.permutation(N_PAIRS)
        
        pos = np.empty(N_PAIRS, dtype=np.int32)
        for i in range(N_PAIRS):
            pos[ordering[i]] = i
        
        valid = True
        kw_order = True
        for name, members in corridor_list:
            positions = pos[members]
            sorted_pos = np.sort(positions)
            diffs = np.diff(sorted_pos)
            if not np.all(diffs == 2):
                valid = False
                break
            # Check KW internal order: members should appear in same order as listed
            if kw_order:
                for i in range(len(members) - 1):
                    if pos[members[i]] > pos[members[i+1]]:
                        kw_order = False
                        break
        
        if valid:
            count_any += 1
            if kw_order:
                count_kw += 1
    
    total_orderings = factorial(N_PAIRS)
    
    print(f"\n  Trials: {N_TRIALS:,}")
    print(f"\n  --- Any internal order ---")
    print(f"  Corridor-preserving orderings found: {count_any}")
    rate_any = count_any / N_TRIALS if count_any > 0 else 1.0 / N_TRIALS
    estimated_any = rate_any * total_orderings
    print(f"  Rate: {rate_any:.2e}")
    print(f"  Estimated corridor-preserving: {estimated_any:.4e}")
    
    print(f"\n  --- KW internal order ---")
    print(f"  Also preserving KW order: {count_kw}")
    rate_kw = count_kw / N_TRIALS if count_kw > 0 else 1.0 / N_TRIALS
    estimated_kw = rate_kw * total_orderings
    print(f"  Rate: {rate_kw:.2e}")
    print(f"  Estimated: {estimated_kw:.4e}")
    
    if count_any > 0 and count_kw > 0:
        print(f"\n  Ratio (any/KW): {count_any / count_kw:.1f}")
    
    print(f"\n  --- Degrees of freedom ---")
    print(f"  Total: log2(32!) = {log2(total_orderings):.1f} bits")
    if count_any > 0:
        bits_corridor = log2(total_orderings) - log2(estimated_any)
        print(f"  Bits removed by corridors: ~{bits_corridor:.1f}")
        print(f"  Remaining: ~{log2(estimated_any):.1f} bits")
    else:
        print(f"  No corridor-preserving orderings found in {N_TRIALS:,} trials")
        print(f"  Corridor constraint removes > {log2(N_TRIALS):.1f} bits")
    
    return count_any, count_kw, N_TRIALS


def slot_placement_analysis():
    """
    Analyze corridor placement as a slot assignment problem.
    
    Model: 32 positions. Place 5 corridor blocks.
    Each block is a 'comb' pattern: L teeth at spacing 2.
    A block of length L at starting position s occupies {s, s+2, ..., s+2(L-1)}.
    
    Blocks must be non-overlapping in positions.
    After placing blocks, remaining positions filled by free pairs.
    """
    print(f"\n{'='*80}")
    print("SLOT PLACEMENT ANALYSIS")
    print("=" * 80)
    
    blocks = [
        ('Earth', 4),
        ('Heaven', 3),
        ('Thunder/Mountain', 2),
        ('Wind', 2),
        ('Lake/Wind', 2),
    ]
    
    total_corridor_pairs = sum(L for _, L in blocks)
    print(f"\nTotal corridor pairs: {total_corridor_pairs}")
    print(f"Total positions: {N_PAIRS}")
    print(f"Free positions after corridors: {N_PAIRS - total_corridor_pairs}")
    
    # For each block, the starting position s must satisfy:
    # s + 2*(L-1) <= N_PAIRS - 1 (0-indexed)
    # i.e., s <= N_PAIRS - 1 - 2*(L-1) = N_PAIRS - 2L + 1
    
    for name, L in blocks:
        max_s = N_PAIRS - 2*L + 1
        print(f"  {name:20s} (L={L}): starting positions 0 to {max_s} ({max_s+1} options)")
    
    # Brute-force enumerate placements of all 5 blocks
    # A placement assigns each block a starting position.
    # The positions occupied by a block at start s with length L are:
    # {s, s+2, ..., s+2(L-1)}
    # Blocks must not overlap (no two blocks occupy the same position).
    
    print(f"\n  Enumerating valid placements of 5 corridor blocks...")
    
    def occupied_positions(start, length):
        return set(range(start, start + 2*(length-1) + 1, 2))
    
    blocks_sorted = sorted(blocks, key=lambda b: -b[1])  # largest first
    
    count_placements = 0
    
    # Earth (L=4): 25 options
    earth_max = N_PAIRS - 2*4 + 1
    for s_earth in range(earth_max + 1):
        occ_earth = occupied_positions(s_earth, 4)
        
        # Heaven (L=3): 27 options
        heaven_max = N_PAIRS - 2*3 + 1
        for s_heaven in range(heaven_max + 1):
            occ_heaven = occupied_positions(s_heaven, 3)
            if occ_earth & occ_heaven:
                continue
            occ_eh = occ_earth | occ_heaven
            
            # Thunder/Mountain (L=2): 29 options
            tm_max = N_PAIRS - 2*2 + 1
            for s_tm in range(tm_max + 1):
                occ_tm = occupied_positions(s_tm, 2)
                if occ_eh & occ_tm:
                    continue
                occ_eht = occ_eh | occ_tm
                
                # Wind (L=2): 29 options
                for s_wind in range(tm_max + 1):
                    occ_wind = occupied_positions(s_wind, 2)
                    if occ_eht & occ_wind:
                        continue
                    occ_ehtw = occ_eht | occ_wind
                    
                    # Lake/Wind (L=2): 29 options
                    for s_lw in range(tm_max + 1):
                        occ_lw = occupied_positions(s_lw, 2)
                        if occ_ehtw & occ_lw:
                            continue
                        count_placements += 1
    
    print(f"  Valid placements (all corridor blocks, no overlap): {count_placements:,}")
    
    # But three L=2 blocks are interchangeable (we assigned specific corridors
    # to specific positions). The L=2 blocks are distinguishable (different pairs),
    # so no overcounting.
    
    # Total corridor-preserving orderings:
    # = placements × internal_perms × free_perms
    internal_perms = 1
    for _, L in blocks:
        internal_perms *= factorial(L)
    
    n_free = N_PAIRS - total_corridor_pairs
    free_perms = factorial(n_free)
    
    total_any = count_placements * internal_perms * free_perms
    total_kw = count_placements * free_perms  # fixed internal order
    
    total_orderings = factorial(N_PAIRS)
    
    print(f"\n  --- Results ---")
    print(f"  Block placements: {count_placements:,}")
    print(f"  Internal permutations: {internal_perms}")
    print(f"  Free pair permutations: {n_free}! = {free_perms:.4e}")
    print(f"\n  Corridor-preserving (any internal order):")
    print(f"    {count_placements} × {internal_perms} × {free_perms:.4e} = {total_any:.4e}")
    print(f"    Fraction of 32!: {total_any / total_orderings:.6e}")
    print(f"    Bits removed: {log2(total_orderings) - log2(total_any):.1f}")
    
    print(f"\n  Corridor-preserving (KW internal order):")
    print(f"    {count_placements} × 1 × {free_perms:.4e} = {total_kw:.4e}")
    print(f"    Fraction of 32!: {total_kw / total_orderings:.6e}")
    print(f"    Bits removed: {log2(total_orderings) - log2(total_kw):.1f}")
    
    print(f"\n  For reference:")
    print(f"    32! = {total_orderings:.4e}")
    print(f"    log2(32!) = {log2(total_orderings):.1f} bits")
    
    return count_placements, internal_perms, free_perms


if __name__ == "__main__":
    analytical_count()
    placements, internal, free = slot_placement_analysis()
    
    # Skip MC for large trial counts — analytical is exact
    # monte_carlo_count()
    
    print(f"\n{'='*80}")
    print(f"ANALYSIS COMPLETE")
    print(f"{'='*80}")
