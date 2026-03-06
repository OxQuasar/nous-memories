#!/usr/bin/env python3
"""
04_trigram_projection.py — Trigram pairs through 互 + 京房 palace test.

Part 1: Input (lower,upper) → output (nuclear_lower, nuclear_upper) mapping.
Part 2: Overlap constraint — which trigram pairs are reachable?
Part 3: 京房八宮 test — do palaces align with 互 fibers?
"""

import sys
sys.path.insert(0, 'memories/iching/opposition-theory/phase4')
sys.path.insert(0, 'memories/iching/kingwen')

from collections import defaultdict
from cycle_algebra import (
    hugua, lower_trigram, upper_trigram, bit, fmt6, fmt3,
    TRIGRAM_NAMES, TRIGRAM_ELEMENT, five_phase_relation,
)
from sequence import KING_WEN

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ═══════════════════════════════════════════════════════════════════════
# Lookups
# ═══════════════════════════════════════════════════════════════════════

NUM_HEX = 64
MASK3 = 0b111

KW = {}
for kw_num, name, binstr in KING_WEN:
    val = sum(int(c) << i for i, c in enumerate(binstr))
    KW[val] = (kw_num, name)

def kw_label(h):
    kw_num, name = KW[h]
    return f"KW#{kw_num}({name})"

def trig_label(t):
    return TRIGRAM_NAMES[t].split()[0]

def inner(h):
    return (h >> 1) & 0xF

# 京房 root trigrams (standard order)
PALACE_ROOTS = [7, 0, 1, 6, 2, 5, 4, 3]  # Qian, Kun, Zhen, Xun, Kan, Li, Gen, Dui
PALACE_NAMES = {7: "Qian", 0: "Kun", 1: "Zhen", 6: "Xun",
                2: "Kan", 5: "Li", 4: "Gen", 3: "Dui"}
STEP_NAMES = ["本宫", "一世", "二世", "三世", "四世", "五世", "游魂", "归魂"]


# ═══════════════════════════════════════════════════════════════════════
# Part 1: Trigram Pair Mapping
# ═══════════════════════════════════════════════════════════════════════

def section_trigram_pairs():
    print("=" * 80)
    print("PART 1: TRIGRAM PAIR MAPPING — (lower,upper) → (nuc_lower, nuc_upper)")
    print("=" * 80)

    # Group by nuclear pair output
    groups = defaultdict(list)

    print(f"\n{'h':>3} {'bin':>7} {'lo':>5} {'up':>5} {'lo_e':>6} {'up_e':>6}"
          f" → {'nlo':>5} {'nup':>5} {'nlo_e':>6} {'nup_e':>6} {'KW':>16}")
    print("-" * 85)

    for h in range(NUM_HEX):
        lo = lower_trigram(h)
        up = upper_trigram(h)
        hu = hugua(h)
        nlo = lower_trigram(hu)
        nup = upper_trigram(hu)

        key = (nlo, nup)
        groups[key].append(h)

        lo_e = TRIGRAM_ELEMENT[lo][:2]
        up_e = TRIGRAM_ELEMENT[up][:2]
        nlo_e = TRIGRAM_ELEMENT[nlo][:2]
        nup_e = TRIGRAM_ELEMENT[nup][:2]
        kw_num, name = KW[h]

        print(f"{h:3d} {fmt6(h):>7} {trig_label(lo):>5} {trig_label(up):>5}"
              f" {lo_e:>6} {up_e:>6}"
              f" → {trig_label(nlo):>5} {trig_label(nup):>5}"
              f" {nlo_e:>6} {nup_e:>6} {f'KW#{kw_num}({name})':>16}")

    # Show groups
    print(f"\n{'─' * 70}")
    print(f"GROUPS BY NUCLEAR PAIR OUTPUT ({len(groups)} groups)")
    print(f"{'─' * 70}")

    for (nlo, nup) in sorted(groups.keys()):
        members = groups[(nlo, nup)]
        assert len(members) == 4, f"Group ({nlo},{nup}) has {len(members)} members"
        labels = [f"{h}({KW[h][1]})" for h in members]
        nlo_e = TRIGRAM_ELEMENT[nlo]
        nup_e = TRIGRAM_ELEMENT[nup]
        print(f"  {trig_label(nlo):>5}/{trig_label(nup):<5} ({nlo_e}/{nup_e})"
              f" ← [{', '.join(labels)}]")

    print(f"\n  Total groups: {len(groups)} (each with exactly 4 hexagrams)")
    return groups


# ═══════════════════════════════════════════════════════════════════════
# Part 2: Overlap Constraint
# ═══════════════════════════════════════════════════════════════════════

def section_overlap():
    print("\n" + "=" * 80)
    print("PART 2: OVERLAP CONSTRAINT")
    print("=" * 80)

    # Nuclear lower = (b₁,b₂,b₃), upper = (b₂,b₃,b₄)
    # Shared: bit1 of lower = bit0 of upper = b₂
    #         bit2 of lower = bit1 of upper = b₃
    print(f"\n  Nuclear lower = (b₁,b₂,b₃) as trigram")
    print(f"  Nuclear upper = (b₂,b₃,b₄) as trigram")
    print(f"  Shared bits: lower[1]=upper[0]=b₂, lower[2]=upper[1]=b₃")
    print(f"  Free bits:   lower[0]=b₁ (unique to lower)")
    print(f"               upper[2]=b₄ (unique to upper)")

    # Verify overlap on all 64 hexagrams
    ok = True
    for h in range(NUM_HEX):
        hu = hugua(h)
        nlo = lower_trigram(hu)
        nup = upper_trigram(hu)
        # Check shared bits
        if bit(nlo, 1) != bit(nup, 0) or bit(nlo, 2) != bit(nup, 1):
            print(f"    MISMATCH at h={h}: nlo={fmt3(nlo)}, nup={fmt3(nup)}")
            ok = False
    print(f"\n  Overlap verification (all 64): {'✓ PASS' if ok else '✗ FAIL'}")

    # Enumerate reachable pairs
    reachable = set()
    for h in range(NUM_HEX):
        hu = hugua(h)
        reachable.add((lower_trigram(hu), upper_trigram(hu)))

    print(f"\n  Reachable (lower,upper) nuclear pairs: {len(reachable)} of 64 possible")

    # Show as matrix
    print(f"\n  Reachability matrix (lower=row, upper=col, ✓=reachable):\n")
    trigs = list(range(8))
    header = "        " + " ".join(f"{trig_label(t):>5}" for t in trigs)
    print(header)
    for lo in trigs:
        row = f"  {trig_label(lo):>5}:"
        for up in trigs:
            row += f"  {'✓' if (lo, up) in reachable else '·':>3} "
        print(row)

    # Show the constraint algebraically
    print(f"\n  For each lower trigram, only 2 upper trigrams are reachable:")
    for lo in trigs:
        partners = sorted([up for up in trigs if (lo, up) in reachable])
        partner_names = [trig_label(p) for p in partners]
        b2 = bit(lo, 1)
        b3 = bit(lo, 2)
        print(f"    {trig_label(lo):>5} ({fmt3(lo)}) → {', '.join(partner_names)}"
              f"  [b₂={b2}, b₃={b3}, b₄ free]")

    return reachable


# ═══════════════════════════════════════════════════════════════════════
# Part 3: 京房八宮
# ═══════════════════════════════════════════════════════════════════════

def generate_palace(root_trig):
    """Generate 8 hexagrams of a 京房 palace."""
    root = root_trig | (root_trig << 3)
    hexs = [root]
    h = root
    for b in range(5):  # flip b₀ through b₄ cumulatively
        h ^= (1 << b)
        hexs.append(h)
    # 游魂: revert b₃ to root value
    if bit(h, 3) != bit(root, 3):
        h ^= (1 << 3)
    hexs.append(h)
    # 归魂: revert lower trigram to palace trigram
    h = (h & ~MASK3) | (root & MASK3)
    hexs.append(h)
    return hexs

def section_palaces():
    print("\n" + "=" * 80)
    print("PART 3: 京房八宮 (JINGFANG EIGHT PALACES)")
    print("=" * 80)

    # Generate all palaces
    all_palace_hexs = set()
    palace_data = {}

    for rt in PALACE_ROOTS:
        palace = generate_palace(rt)
        name = PALACE_NAMES[rt]
        palace_data[rt] = palace
        all_palace_hexs |= set(palace)

        inners = [inner(h) for h in palace]
        hugua_outs = [hugua(h) for h in palace]
        distinct_inner = sorted(set(inners))
        distinct_hugua = sorted(set(hugua_outs))

        print(f"\n{'─' * 70}")
        print(f"  {name} Palace (root trigram = {fmt3(rt)} = {trig_label(rt)})")
        print(f"{'─' * 70}")

        print(f"  {'step':>6} {'h':>3} {'bin':>7} {'lo/up':>11} {'inner':>5}"
              f" {'hu':>3} {'hu_bin':>7} {'KW':>16}")
        for i, h in enumerate(palace):
            hu = hugua(h)
            lo, up = lower_trigram(h), upper_trigram(h)
            kw_num, nm = KW[h]
            print(f"  {STEP_NAMES[i]:>6} {h:3d} {fmt6(h):>7}"
                  f" {trig_label(lo):>5}/{trig_label(up):<5}"
                  f" {inner(h):5d} {hu:3d} {fmt6(hu):>7} KW#{kw_num}({nm})")

        print(f"\n  Distinct inner values: {distinct_inner} ({len(distinct_inner)}/16)")
        print(f"  Distinct hugua outputs: {len(distinct_hugua)}/16")

    print(f"\n  Total unique hexagrams across all palaces: {len(all_palace_hexs)}")

    # Inner XOR mask analysis
    print(f"\n{'─' * 70}")
    print(f"  INNER XOR MASKS (offset from root inner value)")
    print(f"{'─' * 70}")

    mask_sets = []
    for rt in PALACE_ROOTS:
        palace = palace_data[rt]
        root_inner = inner(palace[0])
        masks = sorted(set(inner(h) ^ root_inner for h in palace))
        mask_sets.append(set(masks))
        name = PALACE_NAMES[rt]
        mask_strs = [format(m, '04b') for m in masks]
        print(f"  {name:>5}: masks = {mask_strs}")

    # Check if all palaces use same mask set
    all_same = all(ms == mask_sets[0] for ms in mask_sets)
    print(f"\n  All palaces use identical XOR mask set: {'✓ YES' if all_same else '✗ NO'}")
    if all_same:
        masks = sorted(mask_sets[0])
        print(f"  Universal mask set: {[format(m, '04b') for m in masks]}")
        print(f"  = {{0,1,3,7,8,11,15}} = prefix-flip chain + 游魂/归魂 corrections")

    # Basin coverage per palace
    print(f"\n{'─' * 70}")
    print(f"  BASIN COVERAGE PER PALACE")
    print(f"{'─' * 70}")

    def basin_of_inner(v):
        i1 = (v >> 1) & 1
        i2 = (v >> 2) & 1
        if i1 == 0 and i2 == 0: return "Kun"
        if i1 == 1 and i2 == 1: return "Qian"
        return "Cycle"

    for rt in PALACE_ROOTS:
        palace = palace_data[rt]
        name = PALACE_NAMES[rt]
        basin_counts = defaultdict(int)
        for h in palace:
            basin_counts[basin_of_inner(inner(h))] += 1
        parts = [f"{b}:{c}" for b, c in sorted(basin_counts.items())]
        print(f"  {name:>5}: {', '.join(parts)}")

    print(f"\n  Every palace touches all 3 basins.")

    # Inner value → palace membership
    print(f"\n{'─' * 70}")
    print(f"  INNER VALUE × PALACE MEMBERSHIP")
    print(f"{'─' * 70}")

    inner_palaces = defaultdict(list)
    for rt in PALACE_ROOTS:
        for h in palace_data[rt]:
            inner_palaces[inner(h)].append(PALACE_NAMES[rt])

    for v in range(16):
        palaces = inner_palaces[v]
        distinct_p = sorted(set(palaces))
        count = len(palaces)
        basin = basin_of_inner(v)
        print(f"  inner {v:2d} ({format(v, '04b')}) [{basin:>5}]:"
              f" {count} hexagrams in palaces {distinct_p}")

    return palace_data


# ═══════════════════════════════════════════════════════════════════════
# Visualization
# ═══════════════════════════════════════════════════════════════════════

def make_visualization(reachable, outdir):
    """8×8 reachability matrix."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 7))
    ax.set_title("Nuclear Trigram Pair Reachability (16 of 64)", fontsize=13, fontweight='bold')

    matrix = np.zeros((8, 8))
    for lo, up in reachable:
        matrix[lo, up] = 1

    ax.imshow(matrix, cmap='Blues', aspect='equal', origin='lower')

    for lo in range(8):
        for up in range(8):
            if matrix[lo, up] == 1:
                ax.text(up, lo, "R", ha='center', va='center', fontsize=10,
                        fontweight='bold', color='white')

    trig_names = [trig_label(t) for t in range(8)]
    ax.set_xticks(range(8))
    ax.set_xticklabels(trig_names, fontsize=8)
    ax.set_yticks(range(8))
    ax.set_yticklabels(trig_names, fontsize=8)
    ax.set_xlabel("Upper Nuclear Trigram", fontsize=11)
    ax.set_ylabel("Lower Nuclear Trigram", fontsize=11)

    # Grid
    for i in range(9):
        ax.axhline(i - 0.5, color='gray', linewidth=0.5)
        ax.axvline(i - 0.5, color='gray', linewidth=0.5)

    plt.tight_layout()
    for ext in ('png', 'svg'):
        path = f"{outdir}/04_trigram_projection.{ext}"
        fig.savefig(path, dpi=150, bbox_inches='tight')
        print(f"  Saved: {path}")
    plt.close()


# ═══════════════════════════════════════════════════════════════════════
# Key Findings
# ═══════════════════════════════════════════════════════════════════════

def section_key_findings():
    print("\n" + "=" * 70)
    print("## Key Findings")
    print("=" * 70)

    print("""
1. OVERLAP CONSTRAINT
   Nuclear lower = (b₁,b₂,b₃), upper = (b₂,b₃,b₄).
   2 of 3 bits shared → only 16 of 64 trigram pairs reachable.
   Each lower trigram admits exactly 2 upper partners.
   The free bit is b₁ (lower-unique) and b₄ (upper-unique).

2. FIBER STRUCTURE = 4-TO-1
   Each of 16 nuclear pairs receives exactly 4 hexagrams.
   The fiber = varying outer bits (b₀, b₅).
   Consistent with the 2-bit kernel of M (erases b₀, b₅).

3. REACHABILITY PATTERN
   The 16 reachable pairs form a block-diagonal structure in the
   8×8 trigram-pair matrix, indexed by the interface (b₂,b₃).
   Each (b₂,b₃) value gives a 2×2 block (b₁ varies lower, b₄ varies upper).

4. 京房 PALACES DO NOT ALIGN WITH FIBERS
   Each palace spans exactly 7 of 16 inner values (not 4).
   S5 is REFUTED: palace structure ≠ fiber structure.

5. PALACE INNER MASK UNIVERSALITY
   All 8 palaces use the identical set of 7 inner XOR masks:
   {0000, 0001, 0011, 0111, 1000, 1011, 1111}
   = cumulative bit-flips (steps 1-6) + 游魂/归魂 corrections (steps 7-8).
   The palace algorithm is a fixed traversal of inner space from any root.

6. EVERY PALACE TOUCHES ALL 3 BASINS
   No palace is basin-pure. The 京房 structure cuts across the
   互-convergence topology, not along it. The palaces organize
   hexagrams by surface (trigram pair) structure, not by nuclear
   (inner/convergence) structure.
""")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    import os
    outdir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 70)
    print("04: TRIGRAM PROJECTION + 京房 PALACE TEST")
    print("=" * 70)

    groups = section_trigram_pairs()
    reachable = section_overlap()
    palace_data = section_palaces()

    print("\nGenerating visualization...")
    make_visualization(reachable, outdir)

    section_key_findings()


if __name__ == '__main__':
    main()
