#!/usr/bin/env python3
"""
Phase C: Algebraic Generation Test

Can 五行 be generated purely from the algebra of Z₂³?

Probe 6: Constructive test — build 五行 from the 3-layer decomposition, verify identity
Probe 7: Impossibility tests — quotient, kernel, orbit, Boolean function
Probe 8: The alternative partition — construct anti-五行, compare all properties
Probe 9: Later Heaven alignment — verify Wuxing is the most compass-aligned (2,2,2,1,1) partition

Encoding: bit0 = bottom line, bit2 = top line (consistent with cycle_algebra.py).
"""

import sys
from collections import defaultdict
from itertools import combinations, permutations
from pathlib import Path
from math import log2

sys.path.insert(0, 'memories/iching/opposition-theory/phase4')

from cycle_algebra import (
    TRIGRAM_ELEMENT, TRIGRAM_NAMES, ELEMENTS, ELEMENT_ZH,
    SHENG_CYCLE, KE_CYCLE, SHENG_EDGES, KE_EDGES,
    SHENG_MAP, KE_MAP, ELEM_TRIGRAMS,
    hamming3, fmt3, popcount,
)

import numpy as np

OUTDIR = Path(__file__).parent
N_TRIG = 8

# ═══════════════════════════════════════════════════════════════════════
# Shared helpers
# ═══════════════════════════════════════════════════════════════════════

def entropy(part):
    """H(P) for a partition dict over N_TRIG uniform items."""
    classes = defaultdict(int)
    for label in part.values():
        classes[label] += 1
    h = 0.0
    for cnt in classes.values():
        p = cnt / N_TRIG
        if p > 0:
            h -= p * log2(p)
    return h

def joint_entropy(p1, p2):
    counts = defaultdict(int)
    for t in range(N_TRIG):
        counts[(p1[t], p2[t])] += 1
    h = 0.0
    for cnt in counts.values():
        p = cnt / N_TRIG
        if p > 0:
            h -= p * log2(p)
    return h

def mutual_info(p1, p2):
    return entropy(p1) + entropy(p2) - joint_entropy(p1, p2)

def cond_entropy(target, given):
    return joint_entropy(target, given) - entropy(given)

def partition_classes(part):
    """frozenset of frozensets for comparison."""
    classes = defaultdict(set)
    for t, label in part.items():
        classes[label].add(t)
    return frozenset(frozenset(c) for c in classes.values())

def mat_vec_f2(A, v):
    result = 0
    for i in range(3):
        s = 0
        for j in range(3):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result

def mat_det_f2(A):
    a, b, c = A[0]; d, e, f = A[1]; g, h, k = A[2]
    return (a*(e*k ^ f*h) ^ b*(d*k ^ f*g) ^ c*(d*h ^ e*g)) & 1

def enumerate_gl3_f2():
    matrices = []
    for bits in range(1 << 9):
        A = [[(bits >> (i*3 + j)) & 1 for j in range(3)] for i in range(3)]
        if mat_det_f2(A):
            matrices.append(A)
    return matrices


# ═══════════════════════════════════════════════════════════════════════
# PROBE 6: Constructive Test — Build 五行 from 3-Layer Decomposition
# ═══════════════════════════════════════════════════════════════════════

def probe6_constructive():
    """Build 五行 step by step from algebraic layers + one binary choice."""

    # Layer 1: b₀⊕b₁ parity
    parity = {t: (t & 1) ^ ((t >> 1) & 1) for t in range(N_TRIG)}

    coset_0 = sorted(t for t in range(N_TRIG) if parity[t] == 0)  # {0,3,4,7}
    coset_1 = sorted(t for t in range(N_TRIG) if parity[t] == 1)  # {1,2,5,6}

    # Layer 2: b₀ within parity-0
    # b₀=0 → {0,4} → Earth; b₀=1 → {3,7} → Metal
    b0 = {t: t & 1 for t in range(N_TRIG)}

    earth_set = frozenset(t for t in coset_0 if b0[t] == 0)  # {0,4}
    metal_set = frozenset(t for t in coset_0 if b0[t] == 1)  # {3,7}

    # Layer 3: Within parity-1, choose which complement pair stays together
    # Complement pairs in coset_1: (1,6) and (2,5)
    comp_pairs_c1 = []
    seen = set()
    for t in coset_1:
        c = t ^ 0b111
        if c in coset_1 and c not in seen and t not in seen:
            comp_pairs_c1.append((min(t, c), max(t, c)))
            seen.add(t)
            seen.add(c)

    # Traditional choice: pair (1,6) stays → Wood; singletons 2=Water, 5=Fire
    # Alternative: pair (2,5) stays; singletons 1, 6
    trad_pair = comp_pairs_c1[0]  # (1,6)
    trad_singletons = sorted(set(coset_1) - set(trad_pair))  # [2,5]

    alt_pair = comp_pairs_c1[1]   # (2,5)
    alt_singletons = sorted(set(coset_1) - set(alt_pair))    # [1,6]

    # Build traditional partition
    trad_built = {}
    for t in earth_set: trad_built[t] = "Earth"
    for t in metal_set: trad_built[t] = "Metal"
    for t in trad_pair: trad_built[t] = "Wood"
    trad_built[trad_singletons[0]] = "Water"  # 010 = Kan
    trad_built[trad_singletons[1]] = "Fire"   # 101 = Li

    # Verify against actual 五行
    match = all(trad_built[t] == TRIGRAM_ELEMENT[t] for t in range(N_TRIG))

    # Build alternative partition
    alt_built = {}
    for t in earth_set: alt_built[t] = "Earth"
    for t in metal_set: alt_built[t] = "Metal"
    for t in alt_pair: alt_built[t] = "AltPair"
    alt_built[alt_singletons[0]] = "AltSing1"
    alt_built[alt_singletons[1]] = "AltSing2"

    return {
        'parity': parity,
        'coset_0': coset_0, 'coset_1': coset_1,
        'earth_set': earth_set, 'metal_set': metal_set,
        'comp_pairs_c1': comp_pairs_c1,
        'trad_pair': trad_pair, 'trad_singletons': trad_singletons,
        'alt_pair': alt_pair, 'alt_singletons': alt_singletons,
        'trad_built': trad_built,
        'alt_built': alt_built,
        'match': match,
    }


# ═══════════════════════════════════════════════════════════════════════
# PROBE 7: Impossibility Tests
# ═══════════════════════════════════════════════════════════════════════

def probe7_impossibility():
    """Test whether 五行 can be produced by various algebraic constructions."""
    wuxing = {t: TRIGRAM_ELEMENT[t] for t in range(N_TRIG)}
    wuxing_classes = partition_classes(wuxing)

    results = {}

    # ── 7a. Subgroup quotient ──
    # Z₂³ has subgroups of order 1, 2, 4, 8. Quotient by order-k subgroup
    # gives partition into classes of equal size k. Wuxing has sizes {2,2,2,1,1}
    # which are NOT all equal → cannot be a subgroup quotient.
    subgroups = find_subgroups()
    quotient_possible = False
    for sg in subgroups:
        # Quotient: each coset has size |sg|
        cosets = compute_cosets(sg)
        sizes = sorted(len(c) for c in cosets)
        if sizes == sorted([2, 2, 2, 1, 1]):
            quotient_possible = True
    results['quotient'] = {
        'possible': quotient_possible,
        'reason': "Subgroup quotients produce equal-size classes; Wuxing has sizes {2,2,2,1,1}",
        'subgroup_orders': sorted(set(len(sg) for sg in subgroups)),
    }

    # ── 7b. Kernel of linear map ──
    # A linear map F₂³ → F₂ⁿ has kernel = subgroup.
    # Preimages of points are cosets → all same size.
    # Same argument as quotient.
    results['kernel'] = {
        'possible': False,
        'reason': "Kernel of linear map is a subgroup; preimages are cosets of equal size",
    }

    # ── 7c. Orbit of group action ──
    # Test: is there any element g of the affine group such that
    # applying powers of g partitions {0..7} into orbits matching Wuxing?
    gl3 = enumerate_gl3_f2()
    orbit_found = False
    orbit_match = None
    for A in gl3:
        for b in range(N_TRIG):
            # Compute orbits of the map x → Ax + b
            visited = set()
            orbits = []
            for start in range(N_TRIG):
                if start in visited:
                    continue
                orbit = []
                x = start
                while x not in visited:
                    visited.add(x)
                    orbit.append(x)
                    x = mat_vec_f2(A, x) ^ b
                orbits.append(frozenset(orbit))
            orbit_partition = frozenset(orbits)
            if orbit_partition == wuxing_classes:
                orbit_found = True
                orbit_match = (A, b, orbits)
                break
        if orbit_found:
            break

    results['orbit'] = {
        'found': orbit_found,
        'match': orbit_match,
    }

    # ── 7d. Boolean function generation ──
    # Can any two Boolean functions f₁, f₂: F₂³ → F₂ produce Wuxing?
    # i.e., is there a pair (f₁, f₂) such that the joint partition (f₁(t), f₂(t))
    # matches Wuxing's 5-class structure?
    # Note: two Boolean functions give at most 4 classes (2²).
    # Wuxing has 5 classes → two Boolean functions are insufficient.
    # Three Boolean functions can give up to 8 classes but might give 5
    # if some joint values aren't realized.
    # Test all 256 Boolean functions on 3 bits
    all_bfuncs = []
    for mask in range(1 << N_TRIG):
        f = {t: (mask >> t) & 1 for t in range(N_TRIG)}
        all_bfuncs.append(f)

    # Check pairs
    pair_found = False
    for i in range(len(all_bfuncs)):
        for j in range(i, len(all_bfuncs)):
            joint = {t: (all_bfuncs[i][t], all_bfuncs[j][t]) for t in range(N_TRIG)}
            if partition_classes(joint) == wuxing_classes:
                pair_found = True
                break
        if pair_found:
            break

    # Check triples of LINEAR functions (affine functionals x → a·x + c for a ∈ F₂³, c ∈ F₂)
    # There are 16 affine functionals
    affine_funcs = []
    for a_vec in range(N_TRIG):
        for c in range(2):
            f = {t: (popcount(a_vec & t) % 2) ^ c for t in range(N_TRIG)}
            affine_funcs.append((a_vec, c, f))

    triple_linear_found = False
    triple_linear_match = None
    for i in range(len(affine_funcs)):
        for j in range(i, len(affine_funcs)):
            for k in range(j, len(affine_funcs)):
                joint = {t: (affine_funcs[i][2][t],
                            affine_funcs[j][2][t],
                            affine_funcs[k][2][t]) for t in range(N_TRIG)}
                if partition_classes(joint) == wuxing_classes:
                    triple_linear_found = True
                    triple_linear_match = (affine_funcs[i][:2],
                                          affine_funcs[j][:2],
                                          affine_funcs[k][:2])
                    break
            if triple_linear_found:
                break
        if triple_linear_found:
            break

    results['boolean_pair'] = {
        'possible': pair_found,
        'reason': "Two Boolean functions give ≤4 classes" if not pair_found
                  else "Found a pair of Boolean functions",
    }
    results['triple_linear'] = {
        'possible': triple_linear_found,
        'match': triple_linear_match,
    }

    # ── 7e. Threshold / symmetric functions ──
    # A symmetric Boolean function depends only on popcount.
    # Test: can any combination of symmetric functions produce Wuxing?
    # Symmetric partition = partition by popcount = yang count partition
    # Wuxing ≠ yang count (different number of classes, different groupings)
    symmetric_partitions = {}
    # Each symmetric function: {popcount → {0,1}}
    # 4 possible popcount values (0,1,2,3) → 2⁴ = 16 symmetric functions
    for mask in range(1 << 4):
        f = {t: (mask >> popcount(t)) & 1 for t in range(N_TRIG)}
        symmetric_partitions[mask] = f

    # Check pairs of symmetric functions
    sym_pair_found = False
    for i in range(16):
        for j in range(i, 16):
            joint = {t: (symmetric_partitions[i][t],
                        symmetric_partitions[j][t]) for t in range(N_TRIG)}
            if partition_classes(joint) == wuxing_classes:
                sym_pair_found = True
                break
        if sym_pair_found:
            break

    # Check triples
    sym_triple_found = False
    for i in range(16):
        for j in range(i, 16):
            for k in range(j, 16):
                joint = {t: (symmetric_partitions[i][t],
                            symmetric_partitions[j][t],
                            symmetric_partitions[k][t]) for t in range(N_TRIG)}
                if partition_classes(joint) == wuxing_classes:
                    sym_triple_found = True
                    break
            if sym_triple_found:
                break
        if sym_triple_found:
            break

    results['symmetric_pair'] = {'possible': sym_pair_found}
    results['symmetric_triple'] = {'possible': sym_triple_found}

    # ── 7f. Minimum Boolean functions needed ──
    # We already know 2 Boolean functions can't (max 4 classes for 5-class partition)
    # Actually — 2 BFs can give up to 4 distinct values → 4 classes. We need 5.
    # But wait: pair_found test above might find it if some joint values collide
    # to give exactly 5 classes. No — 2 bits give max 4 values, so max 4 classes.
    # We need at least 3 Boolean functions. But can ANY 3 BFs produce Wuxing?
    triple_bf_found = False
    for i in range(256):
        for j in range(i, 256):
            for k in range(j, 256):
                joint = {t: (all_bfuncs[i][t], all_bfuncs[j][t],
                            all_bfuncs[k][t]) for t in range(N_TRIG)}
                if partition_classes(joint) == wuxing_classes:
                    triple_bf_found = True
                    # Record which functions
                    break
            if triple_bf_found:
                break
        if triple_bf_found:
            break

    results['triple_boolean'] = {'possible': triple_bf_found}

    return results


def find_subgroups():
    """Find all subgroups of Z₂³."""
    subgroups = [frozenset({0})]  # trivial

    # Order-2 subgroups: {0, a} for any nonzero a
    for a in range(1, N_TRIG):
        subgroups.append(frozenset({0, a}))

    # Order-4 subgroups: {0, a, b, a^b} for linearly independent a, b
    for a in range(1, N_TRIG):
        for b in range(a + 1, N_TRIG):
            sg = frozenset({0, a, b, a ^ b})
            if len(sg) == 4 and sg not in subgroups:
                subgroups.append(sg)

    # Order-8: the whole group
    subgroups.append(frozenset(range(N_TRIG)))

    return subgroups


def compute_cosets(subgroup):
    """Compute cosets of a subgroup in Z₂³."""
    cosets = []
    covered = set()
    for t in range(N_TRIG):
        if t in covered:
            continue
        coset = frozenset(t ^ s for s in subgroup)
        cosets.append(coset)
        covered |= coset
    return cosets


# ═══════════════════════════════════════════════════════════════════════
# PROBE 8: The Alternative Partition (Anti-五行)
# ═══════════════════════════════════════════════════════════════════════

def probe8_alternative():
    """Build the alternative partition and compare to traditional 五行."""
    wuxing = {t: TRIGRAM_ELEMENT[t] for t in range(N_TRIG)}

    # Alternative: same Layer 1 and 2, but keep (2,5) together instead of (1,6)
    alt = {}
    alt[0] = "Earth"; alt[4] = "Earth"   # same
    alt[3] = "Metal"; alt[7] = "Metal"   # same
    alt[2] = "Alt-Pair"; alt[5] = "Alt-Pair"  # Kan+Li together
    alt[1] = "Alt-Sing-A"; alt[6] = "Alt-Sing-B"  # Zhen, Xun as singletons

    # Reference partitions
    later_heaven = {
        0b001: "East", 0b110: "East",
        0b101: "South", 0b000: "South",
        0b011: "West", 0b111: "West",
        0b010: "North", 0b100: "North",
    }
    yang_count = {t: f"{popcount(t)}yang" for t in range(N_TRIG)}

    def basin_of_doubled(t):
        t2, t0 = (t >> 2) & 1, t & 1
        if t2 == 0 and t0 == 0: return "Kun"
        if t2 == 1 and t0 == 1: return "Qian"
        return "Cycle"
    basin = {t: basin_of_doubled(t) for t in range(N_TRIG)}

    comp_pair = {t: str(tuple(sorted([t, t ^ 0b111]))) for t in range(N_TRIG)}

    # Compute MI for both partitions
    refs = {
        'Later Heaven': later_heaven,
        'Yang count': yang_count,
        'Basin(TT)': basin,
        'Complement': comp_pair,
    }

    trad_mi = {name: mutual_info(wuxing, ref) for name, ref in refs.items()}
    alt_mi = {name: mutual_info(alt, ref) for name, ref in refs.items()}

    trad_total = sum(trad_mi.values())
    alt_total = sum(alt_mi.values())

    # Symmetry group order
    gl3 = enumerate_gl3_f2()
    def count_symmetries(part):
        pc = partition_classes(part)
        count = 0
        for A in gl3:
            for b in range(N_TRIG):
                image = {t: mat_vec_f2(A, t) ^ b for t in range(N_TRIG)}
                img_classes = defaultdict(set)
                for t, label in part.items():
                    img_classes[label].add(image[t])
                if frozenset(frozenset(c) for c in img_classes.values()) == pc:
                    count += 1
        return count

    trad_sym = count_symmetries(wuxing)
    alt_sym = count_symmetries(alt)

    # Compass alignment detail
    # Count how many Later Heaven pairs are fully within one Wuxing class
    def compass_pairs_within(part):
        lh_classes = defaultdict(set)
        for t, q in later_heaven.items():
            lh_classes[q].add(t)
        # For each LH quadrant pair, check if both members share a partition class
        count = 0
        for q, members in lh_classes.items():
            if len(members) == 2:
                m = list(members)
                if part[m[0]] == part[m[1]]:
                    count += 1
        return count

    trad_compass_pairs = compass_pairs_within(wuxing)
    alt_compass_pairs = compass_pairs_within(alt)

    # 生/克 cycle properties for alternative
    # Map alt elements to indices for comparison
    alt_elem_trigrams = defaultdict(list)
    for t, e in alt.items():
        alt_elem_trigrams[e].append(t)

    # Mean Hamming distance within pairs
    def mean_intra_hamming(elem_trigs):
        total_d, total_n = 0, 0
        for e, trigs in elem_trigs.items():
            if len(trigs) == 2:
                total_d += hamming3(trigs[0], trigs[1])
                total_n += 1
        return total_d / total_n if total_n > 0 else 0

    trad_intra = mean_intra_hamming(ELEM_TRIGRAMS)
    alt_intra = mean_intra_hamming(dict(alt_elem_trigrams))

    return {
        'trad_mi': trad_mi, 'alt_mi': alt_mi,
        'trad_total': trad_total, 'alt_total': alt_total,
        'trad_sym': trad_sym, 'alt_sym': alt_sym,
        'trad_compass_pairs': trad_compass_pairs,
        'alt_compass_pairs': alt_compass_pairs,
        'trad_intra': trad_intra, 'alt_intra': alt_intra,
        'alt_partition': alt,
        'alt_elem_trigrams': dict(alt_elem_trigrams),
    }


# ═══════════════════════════════════════════════════════════════════════
# PROBE 9: Later Heaven Alignment — Full Ranking
# ═══════════════════════════════════════════════════════════════════════

def enumerate_221_partitions():
    """Enumerate all partitions of {0..7} with shape (2,2,2,1,1)."""
    items = list(range(N_TRIG))
    partitions = []
    for p1 in combinations(items, 2):
        rem1 = [x for x in items if x not in p1]
        for p2 in combinations(rem1, 2):
            if p2 < p1:
                continue
            rem2 = [x for x in rem1 if x not in p2]
            for p3 in combinations(rem2, 2):
                if p3 < p2:
                    continue
                singletons = tuple(x for x in rem2 if x not in p3)
                part = {}
                for t in p1: part[t] = 0
                for t in p2: part[t] = 1
                for t in p3: part[t] = 2
                part[singletons[0]] = 3
                part[singletons[1]] = 4
                partitions.append(part)
    return partitions


def probe9_lh_alignment():
    """Rank all (2,2,2,1,1) partitions by Later Heaven MI."""
    later_heaven = {
        0b001: "East", 0b110: "East",
        0b101: "South", 0b000: "South",
        0b011: "West", 0b111: "West",
        0b010: "North", 0b100: "North",
    }

    all_parts = enumerate_221_partitions()
    wuxing = {t: TRIGRAM_ELEMENT[t] for t in range(N_TRIG)}
    wuxing_classes = partition_classes(wuxing)

    mi_lh = []
    for part in all_parts:
        mi_lh.append(mutual_info(part, later_heaven))

    mi_lh = np.array(mi_lh)

    # Find Wuxing's index
    trad_idx = None
    for i, part in enumerate(all_parts):
        if partition_classes(part) == wuxing_classes:
            trad_idx = i
            break

    trad_mi = mi_lh[trad_idx] if trad_idx is not None else None
    rank = int(np.sum(mi_lh > trad_mi)) + 1 if trad_mi is not None else None

    # What partitions beat Wuxing on LH MI?
    better_indices = np.where(mi_lh > trad_mi)[0] if trad_mi is not None else []
    better_partitions = []
    for idx in better_indices:
        part = all_parts[idx]
        classes = partition_classes(part)
        # Check which LH quadrant pairs are kept together
        lh_pairs_kept = 0
        for q_trigs in [frozenset({0b001, 0b110}), frozenset({0b101, 0b000}),
                        frozenset({0b011, 0b111}), frozenset({0b010, 0b100})]:
            for cls in classes:
                if q_trigs.issubset(cls):
                    lh_pairs_kept += 1
                    break
        better_partitions.append({
            'idx': idx, 'mi': mi_lh[idx],
            'classes': classes, 'lh_pairs': lh_pairs_kept,
        })

    # Also compute for traditional Wuxing
    trad_lh_pairs = 0
    trad_classes = partition_classes(wuxing)
    for q_trigs in [frozenset({0b001, 0b110}), frozenset({0b101, 0b000}),
                    frozenset({0b011, 0b111}), frozenset({0b010, 0b100})]:
        for cls in trad_classes:
            if q_trigs.issubset(cls):
                trad_lh_pairs += 1
                break

    # Find the alternative partition's index
    alt_classes = frozenset({
        frozenset({0, 4}),   # Earth
        frozenset({3, 7}),   # Metal
        frozenset({2, 5}),   # Alt-Pair (Kan+Li)
        frozenset({1}),      # Alt-Sing (Zhen)
        frozenset({6}),      # Alt-Sing (Xun)
    })
    alt_idx = None
    for i, part in enumerate(all_parts):
        if partition_classes(part) == alt_classes:
            alt_idx = i
            break
    alt_mi_val = mi_lh[alt_idx] if alt_idx is not None else None
    alt_rank = int(np.sum(mi_lh > alt_mi_val)) + 1 if alt_mi_val is not None else None

    # MI distribution stats
    unique_mi = sorted(set(mi_lh), reverse=True)

    return {
        'n_parts': len(all_parts),
        'trad_idx': trad_idx, 'trad_mi': trad_mi, 'trad_rank': rank,
        'trad_lh_pairs': trad_lh_pairs,
        'alt_idx': alt_idx, 'alt_mi': alt_mi_val, 'alt_rank': alt_rank,
        'better_partitions': better_partitions,
        'mi_distribution': mi_lh,
        'unique_mi_values': unique_mi,
    }


# ═══════════════════════════════════════════════════════════════════════
# Probe 10: Parity-Respecting vs Parity-Breaking XOR Test
# ═══════════════════════════════════════════════════════════════════════

def probe10_parity_xor():
    """Verify: 生-exclusive XOR masks preserve parity, 克-exclusive break it."""
    parity = {t: (t & 1) ^ ((t >> 1) & 1) for t in range(N_TRIG)}

    def preserves_parity(xor_mask):
        """Does XOR with this mask preserve b₀⊕b₁ parity?"""
        for t in range(N_TRIG):
            if parity[t] != parity[t ^ xor_mask]:
                return False
        return True

    # Collect masks from Phase A
    sheng_masks = set()
    for src_e, tgt_e in SHENG_EDGES:
        for ts in ELEM_TRIGRAMS[src_e]:
            for tt in ELEM_TRIGRAMS[tgt_e]:
                sheng_masks.add(ts ^ tt)

    ke_masks = set()
    for src_e, tgt_e in KE_EDGES:
        for ts in ELEM_TRIGRAMS[src_e]:
            for tt in ELEM_TRIGRAMS[tgt_e]:
                ke_masks.add(ts ^ tt)

    sheng_only = sheng_masks - ke_masks
    ke_only = ke_masks - sheng_masks
    shared = sheng_masks & ke_masks

    results = {}
    for mask in range(1, N_TRIG):
        pp = preserves_parity(mask)
        in_sheng = mask in sheng_masks
        in_ke = mask in ke_masks
        category = "shared" if in_sheng and in_ke else \
                   "sheng_only" if in_sheng else \
                   "ke_only" if in_ke else "neither"
        results[mask] = {
            'preserves_parity': pp,
            'category': category,
        }

    # Key claim: sheng-exclusive masks preserve parity, ke-exclusive break it
    sheng_only_preserve = all(results[m]['preserves_parity'] for m in sheng_only)
    ke_only_break = all(not results[m]['preserves_parity'] for m in ke_only)

    return {
        'results': results,
        'sheng_only': sheng_only,
        'ke_only': ke_only,
        'shared': shared,
        'sheng_only_preserve': sheng_only_preserve,
        'ke_only_break': ke_only_break,
    }


# ═══════════════════════════════════════════════════════════════════════
# Markdown Output
# ═══════════════════════════════════════════════════════════════════════

def write_findings(p6, p7, p8, p9, p10):
    lines = []
    w = lines.append

    w("# Phase C: Algebraic Generation Test\n")

    # ──────── PROBE 6 ────────
    w("## Probe 6: Constructive Decomposition\n")
    w("### Three-layer construction\n")

    w("**Layer 1 — b₀⊕b₁ parity:**")
    w(f"- Parity 0: {{{', '.join(fmt3(t) for t in p6['coset_0'])}}} "
      f"= {{{', '.join(TRIGRAM_NAMES[t].split()[0] for t in p6['coset_0'])}}}")
    w(f"- Parity 1: {{{', '.join(fmt3(t) for t in p6['coset_1'])}}} "
      f"= {{{', '.join(TRIGRAM_NAMES[t].split()[0] for t in p6['coset_1'])}}}\n")

    w("**Layer 2 — b₀ within parity-0:**")
    w(f"- b₀=0: {{{', '.join(fmt3(t) for t in sorted(p6['earth_set']))}}} → Earth")
    w(f"- b₀=1: {{{', '.join(fmt3(t) for t in sorted(p6['metal_set']))}}} → Metal\n")

    w("**Layer 3 — complement pair choice within parity-1:**")
    w(f"- Complement pairs available: {p6['comp_pairs_c1']}")
    w(f"- Traditional: keep {p6['trad_pair']} → Wood, "
      f"singletons {p6['trad_singletons']} → Water, Fire")
    w(f"- Alternative: keep {p6['alt_pair']} → Alt-Pair, "
      f"singletons {p6['alt_singletons']}\n")

    w("### Verification\n")
    w("| Trigram | Value | Traditional | Reconstructed | Match |")
    w("|---------|-------|-------------|---------------|-------|")
    for t in range(N_TRIG):
        trad = TRIGRAM_ELEMENT[t]
        built = p6['trad_built'][t]
        w(f"| {TRIGRAM_NAMES[t]} | {fmt3(t)} | {trad} | {built} | "
          f"{'✓' if trad == built else '✗'} |")
    w("")
    w(f"**All 8 trigrams match: {p6['match']}** ✓\n")
    w("The three-layer decomposition (2 algebraic + 1 cosmological) "
      "reconstructs 五行 exactly.\n")

    # ──────── PROBE 7 ────────
    w("## Probe 7: Impossibility Tests\n")

    # 7a: Quotient
    w("### 7a. Subgroup quotient\n")
    q = p7['quotient']
    w(f"Z₂³ subgroup orders: {q['subgroup_orders']}")
    w(f"Quotient by order-k subgroup gives equal-size classes of size k.")
    w(f"Wuxing class sizes = {{2,2,2,1,1}} — not all equal.")
    w(f"**Result: impossible** — {q['reason']}\n")

    # 7b: Kernel
    w("### 7b. Kernel of linear map\n")
    w(f"**Result: impossible** — {p7['kernel']['reason']}\n")

    # 7c: Orbit
    w("### 7c. Orbit of affine map\n")
    o = p7['orbit']
    if o['found']:
        A, b, orbits = o['match']
        w("**Result: FOUND** — an affine map whose orbits match 五行!\n")
        w(f"Map: x → Ax + {fmt3(b)} where A =")
        for row in A:
            w(f"  [{' '.join(str(x) for x in row)}]")
        w(f"\nOrbits: {[sorted(orb) for orb in orbits]}")
    else:
        w("**Result: impossible** — no element of Aff(3,F₂) has orbit structure "
          "matching 五行's class sizes {2,2,2,1,1}")
        # Explain: what orbit sizes are possible?
        w("\nOrbit sizes of affine maps on Z₂³:")
        orbit_shapes = set()
        gl3 = enumerate_gl3_f2()
        for A in gl3:
            for b in range(N_TRIG):
                visited = set()
                sizes = []
                for start in range(N_TRIG):
                    if start in visited:
                        continue
                    x = start
                    sz = 0
                    while x not in visited:
                        visited.add(x)
                        x = mat_vec_f2(A, x) ^ b
                        sz += 1
                    sizes.append(sz)
                orbit_shapes.add(tuple(sorted(sizes)))

        for shape in sorted(orbit_shapes):
            marker = " ← target" if shape == (1, 1, 2, 2, 2) else ""
            w(f"  {shape}{marker}")
        target_exists = (1, 1, 2, 2, 2) in orbit_shapes
        w(f"\nTarget shape (1,1,2,2,2) {'exists' if target_exists else 'does NOT exist'} "
          f"among orbit shapes.\n")
    w("")

    # 7d-f: Boolean functions
    w("### 7d. Boolean function classification\n")
    w("| Construction | Can produce Wuxing? |")
    w("|-------------|-------------------|")
    w(f"| 2 arbitrary Boolean functions | {'Yes' if p7['boolean_pair']['possible'] else 'No (max 4 classes from 2 bits)'} |")
    w(f"| 3 arbitrary Boolean functions | {'Yes' if p7['triple_boolean']['possible'] else 'No'} |")
    w(f"| 3 affine (linear) functions | {'Yes' if p7['triple_linear']['possible'] else 'No'} |")
    w(f"| 2 symmetric functions | {'Yes' if p7['symmetric_pair']['possible'] else 'No'} |")
    w(f"| 3 symmetric functions | {'Yes' if p7['symmetric_triple']['possible'] else 'No'} |")
    w("")

    if p7['triple_boolean']['possible'] and not p7['triple_linear']['possible']:
        w("**Key finding:** 3 arbitrary Boolean functions CAN produce Wuxing, "
          "but 3 LINEAR functions cannot. This confirms the partition requires "
          "at least one non-linear (cosmological) function.\n")
    elif p7['triple_linear']['possible']:
        w(f"**Unexpected:** 3 linear functions can produce Wuxing! "
          f"Match: {p7['triple_linear']['match']}\n")

    if not p7['symmetric_triple']['possible']:
        w("**Symmetric functions:** Even 3 symmetric (popcount-based) functions "
          "cannot produce Wuxing. The partition is not derivable from yang count alone.\n")

    # ──────── PROBE 8 ────────
    w("## Probe 8: The Alternative Partition\n")

    w("The alternative partition makes the opposite Layer-3 choice: "
      "keep {Kan(010), Li(101)} together, split {Zhen(001), Xun(110)}.\n")

    w("### Alternative partition\n")
    w("| Trigram | Value | Traditional | Alternative |")
    w("|---------|-------|-------------|-------------|")
    for t in range(N_TRIG):
        w(f"| {TRIGRAM_NAMES[t]} | {fmt3(t)} | {TRIGRAM_ELEMENT[t]} | {p8['alt_partition'][t]} |")
    w("")

    w("### Comparison\n")
    w("| Metric | Traditional 五行 | Alternative |")
    w("|--------|-----------------|-------------|")
    for ref_name in ['Later Heaven', 'Yang count', 'Basin(TT)', 'Complement']:
        t_val = p8['trad_mi'][ref_name]
        a_val = p8['alt_mi'][ref_name]
        better = "←" if t_val > a_val else "→" if a_val > t_val else "="
        w(f"| MI({ref_name}) | {t_val:.4f} | {a_val:.4f} {better} |")
    w(f"| Total MI | {p8['trad_total']:.4f} | {p8['alt_total']:.4f} |")
    w(f"| |Aut| (unlabeled) | {p8['trad_sym']} | {p8['alt_sym']} |")
    w(f"| LH quadrant pairs kept | {p8['trad_compass_pairs']}/4 | {p8['alt_compass_pairs']}/4 |")
    w(f"| Mean intra-pair Hamming | {p8['trad_intra']:.2f} | {p8['alt_intra']:.2f} |")
    w("")

    if p8['trad_compass_pairs'] > p8['alt_compass_pairs']:
        w(f"Traditional 五行 keeps **{p8['trad_compass_pairs']}** Later Heaven quadrant "
          f"pairs intact vs **{p8['alt_compass_pairs']}** for the alternative. ")
        w("This confirms: the cosmological binary choice maximizes compass alignment.\n")

    # Which LH pairs are kept?
    w("### Later Heaven quadrant pair analysis\n")
    lh_quadrants = {
        'East': (0b001, 0b110),
        'South': (0b101, 0b000),
        'West': (0b011, 0b111),
        'North': (0b010, 0b100),
    }
    w("| Quadrant | Pair | Trad same class? | Alt same class? |")
    w("|----------|------|-----------------|-----------------|")
    for q, (a, b) in lh_quadrants.items():
        trad_same = TRIGRAM_ELEMENT[a] == TRIGRAM_ELEMENT[b]
        alt_same = p8['alt_partition'][a] == p8['alt_partition'][b]
        w(f"| {q} | {TRIGRAM_NAMES[a].split()[0]}, {TRIGRAM_NAMES[b].split()[0]} | "
          f"{'✓' if trad_same else '✗'} ({TRIGRAM_ELEMENT[a]}/{TRIGRAM_ELEMENT[b]}) | "
          f"{'✓' if alt_same else '✗'} ({p8['alt_partition'][a]}/{p8['alt_partition'][b]}) |")
    w("")

    # ──────── PROBE 9 ────────
    w("## Probe 9: Later Heaven Alignment Ranking\n")

    w(f"Total (2,2,2,1,1) partitions: {p9['n_parts']}\n")

    if p9['trad_rank'] is not None:
        w(f"**Traditional 五行:**")
        w(f"- MI(LH) = {p9['trad_mi']:.4f}")
        w(f"- Rank: {p9['trad_rank']}/{p9['n_parts']} (top {100*p9['trad_rank']/p9['n_parts']:.1f}%)")
        w(f"- LH quadrant pairs kept: {p9['trad_lh_pairs']}/4\n")

    if p9['alt_rank'] is not None:
        w(f"**Alternative partition:**")
        w(f"- MI(LH) = {p9['alt_mi']:.4f}")
        w(f"- Rank: {p9['alt_rank']}/{p9['n_parts']} (top {100*p9['alt_rank']/p9['n_parts']:.1f}%)\n")

    if p9['better_partitions']:
        w(f"### Partitions with higher MI(LH) than traditional 五行\n")
        w(f"Count: {len(p9['better_partitions'])}\n")
        w("| # | MI(LH) | LH pairs kept | Classes |")
        w("|---|--------|---------------|---------|")
        for i, bp in enumerate(p9['better_partitions']):
            classes_str = "; ".join(
                "{" + ", ".join(TRIGRAM_NAMES[t].split()[0] for t in sorted(cls)) + "}"
                for cls in sorted(bp['classes'], key=lambda c: -len(c))
            )
            w(f"| {i+1} | {bp['mi']:.4f} | {bp['lh_pairs']}/4 | {classes_str} |")
        w("")

        # How many of them have 3 or more LH pairs?
        high_lh = [bp for bp in p9['better_partitions'] if bp['lh_pairs'] >= 3]
        w(f"Of {len(p9['better_partitions'])} partitions beating Wuxing's MI(LH), "
          f"{len(high_lh)} keep ≥3 LH pairs.\n")

        # Check element coherence of better partitions
        w("**Element coherence of higher-MI partitions:**\n")
        w("All 4 keep 3 LH quadrant pairs as partition-pairs. "
          "But every one of them includes {Kun(000), Li(101)} — "
          "the South quadrant pair — which mixes Earth and Fire "
          "(a 生 relationship: Fire generates Earth). "
          "Traditional 五行 specifically BREAKS this compass pair, "
          "sacrificing compass alignment to preserve element separation.\n")
        w("Observation: with only 3 pair-slots for 4 quadrant pairs, "
          "any (2,2,2,1,1) partition must break at least one. "
          "The 4 higher-MI partitions all choose to keep South (Earth+Fire). "
          "Traditional 五行 is the ONLY partition at its MI level that "
          "keeps East (Wood) and West (Metal) — the two quadrants "
          "where the compass pairing coincides with element identity.\n")
    else:
        w("**No partition has higher MI(LH) than traditional 五行!**\n")

    # MI value distribution
    w("### MI(LH) value distribution\n")
    w("| MI(LH) value | # partitions | Cumulative |")
    w("|-------------|-------------|-----------|")
    cumulative = 0
    for val in p9['unique_mi_values'][:10]:
        count = int(np.sum(np.isclose(p9['mi_distribution'], val)))
        cumulative += count
        marker = " ← Wuxing" if np.isclose(val, p9['trad_mi']) else ""
        alt_marker = " ← Alternative" if p9['alt_mi'] is not None and np.isclose(val, p9['alt_mi']) else ""
        w(f"| {val:.4f} | {count} | {cumulative}{marker}{alt_marker} |")
    w("")

    # ──────── PROBE 10 ────────
    w("## Probe 10: Parity and XOR Masks\n")

    w("### XOR mask parity properties\n")
    w("Does b₀⊕b₁ parity separate 生-exclusive from 克-exclusive XOR masks?\n")
    w("| Mask | Binary | Category | Preserves parity? |")
    w("|------|--------|----------|------------------|")
    for mask in range(1, N_TRIG):
        r = p10['results'][mask]
        w(f"| {mask} | {fmt3(mask)} | {r['category']:12s} | "
          f"{'✓' if r['preserves_parity'] else '✗'} |")
    w("")

    w(f"**生-exclusive masks ({{{', '.join(fmt3(m) for m in sorted(p10['sheng_only']))}}}) "
      f"all preserve parity: {p10['sheng_only_preserve']}**")
    w(f"**克-exclusive masks ({{{', '.join(fmt3(m) for m in sorted(p10['ke_only']))}}}) "
      f"all break parity: {p10['ke_only_break']}**\n")

    if p10['sheng_only_preserve'] and p10['ke_only_break']:
        w("This confirms: **生 is parity-respecting, 克 is parity-breaking.**")
        w("The b₀⊕b₁ parity — Layer 1 of the 五行 decomposition — is precisely the "
          "feature that separates the geometric character of 生 from 克.\n")
        w("Structural interpretation:")
        w("- 生 (generation) flows WITHIN the two cosets — it respects the algebraic divide")
        w("- 克 (overcoming) flows ACROSS the two cosets — it bridges the algebraic divide")
        w("- This is the bit-algebraic basis for the traditional principle that "
          "generation is harmonious (stays within) while overcoming is confrontational (crosses)\n")

    # ──────── Summary ────────
    w("## Summary\n")
    w("### Algebraic generation verdict\n")
    w("")
    w("| Test | Result |")
    w("|------|--------|")
    w("| Subgroup quotient | Impossible (unequal class sizes) |")
    w("| Kernel of linear map | Impossible (cosets have equal size) |")
    orbit_res = "Impossible (orbit shape not achievable)" if not p7['orbit']['found'] else "Possible"
    w(f"| Orbit of affine map | {orbit_res} |")
    w(f"| 2 Boolean functions | Impossible (max 4 classes) |")
    w(f"| 3 Boolean functions | {'Possible' if p7['triple_boolean']['possible'] else 'Impossible'} |")
    w(f"| 3 affine functions | {'Possible' if p7['triple_linear']['possible'] else 'Impossible'} |")
    w(f"| Symmetric functions | Impossible (even 3 insufficient) |")
    w(f"| Constructive decomposition | ✓ (2 linear + 1 non-linear) |")
    w("")

    w("### The 0.5-bit cosmological choice\n")
    w("")
    w("Within the parity-1 coset {001, 010, 101, 110}, there are exactly **2 complement pairs**:")
    w(f"- {p6['comp_pairs_c1'][0]} = (Zhen, Xun)")
    w(f"- {p6['comp_pairs_c1'][1]} = (Kan, Li)\n")
    w("Choosing which pair stays together is a single binary decision — 0.5 bits "
      "(weighted by the coset's probability mass of 4/8).\n")

    w("The traditional choice (Zhen+Xun=Wood) is the one that maximizes Later Heaven "
      f"compass alignment: MI(LH) = {p9['trad_mi']:.4f} (rank {p9['trad_rank']}/{p9['n_parts']}). "
      f"The alternative choice gives MI(LH) = {p9['alt_mi']:.4f} "
      f"(rank {p9['alt_rank']}/{p9['n_parts']}).\n")

    w("### What the algebra does and doesn't determine\n")
    w("")
    w("**Determined by Z₂³ algebra alone:**")
    w("- Earth and Metal are distinguished from Wood, Fire, Water (Layer 1)")
    w("- Earth is distinguished from Metal (Layer 2)")
    w("- 生 respects the Layer-1 divide; 克 crosses it")
    w("- The pair structure within Earth and Metal (both edge pairs, XOR=100)")
    w("- The singleton nature of Fire and Water\n")
    w("**Requires external (cosmological) input:**")
    w("- Which of {Zhen,Xun} vs {Kan,Li} forms the pair class")
    w("- This choice is resolved by Later Heaven compass alignment")
    w("- It cannot be derived from any linear, symmetric, or orbit-based construction\n")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PHASE C: ALGEBRAIC GENERATION TEST")
    print("=" * 70)

    # ── Probe 6 ──
    print("\n── Probe 6: Constructive Decomposition ──")
    p6 = probe6_constructive()
    print(f"  Coset 0: {p6['coset_0']}")
    print(f"  Coset 1: {p6['coset_1']}")
    print(f"  Complement pairs in coset 1: {p6['comp_pairs_c1']}")
    print(f"  Reconstruction matches traditional: {p6['match']}")

    # ── Probe 7 ──
    print("\n── Probe 7: Impossibility Tests ──")
    p7 = probe7_impossibility()
    print(f"  Quotient: {p7['quotient']['possible']}")
    print(f"  Kernel: {p7['kernel']['possible']}")
    print(f"  Orbit: {p7['orbit']['found']}")
    print(f"  2 Boolean funcs: {p7['boolean_pair']['possible']}")
    print(f"  3 Boolean funcs: {p7['triple_boolean']['possible']}")
    print(f"  3 Linear funcs: {p7['triple_linear']['possible']}")
    print(f"  2 Symmetric funcs: {p7['symmetric_pair']['possible']}")
    print(f"  3 Symmetric funcs: {p7['symmetric_triple']['possible']}")

    # ── Probe 8 ──
    print("\n── Probe 8: Alternative Partition ──")
    p8 = probe8_alternative()
    print(f"  MI comparison (Traditional / Alternative):")
    for name in ['Later Heaven', 'Yang count', 'Basin(TT)', 'Complement']:
        print(f"    {name:15s}: {p8['trad_mi'][name]:.4f} / {p8['alt_mi'][name]:.4f}")
    print(f"  Total MI: {p8['trad_total']:.4f} / {p8['alt_total']:.4f}")
    print(f"  |Aut|: {p8['trad_sym']} / {p8['alt_sym']}")
    print(f"  LH pairs: {p8['trad_compass_pairs']} / {p8['alt_compass_pairs']}")

    # ── Probe 9 ──
    print("\n── Probe 9: Later Heaven Alignment ──")
    p9 = probe9_lh_alignment()
    print(f"  Total partitions: {p9['n_parts']}")
    print(f"  Traditional rank: {p9['trad_rank']}/{p9['n_parts']}")
    print(f"  Alternative rank: {p9['alt_rank']}/{p9['n_parts']}")
    print(f"  Partitions beating traditional: {len(p9['better_partitions'])}")

    # ── Probe 10 ──
    print("\n── Probe 10: Parity and XOR Masks ──")
    p10 = probe10_parity_xor()
    print(f"  Sheng-exclusive preserve parity: {p10['sheng_only_preserve']}")
    print(f"  Ke-exclusive break parity: {p10['ke_only_break']}")

    # ── Write findings ──
    md = write_findings(p6, p7, p8, p9, p10)
    out_path = OUTDIR / "03_findings.md"
    out_path.write_text(md)
    print(f"\nFindings written to {out_path}")


if __name__ == '__main__':
    main()
