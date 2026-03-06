#!/usr/bin/env python3
"""
Probe 2: Palace Generation in Kernel Language

Maps the 8 palace ranks (本宮 through 歸魂) onto the basin/kernel/depth
decomposition. Analyzes 世/應 positions relative to the three-layer onion.
"""

import sys
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "opposition-theory" / "phase4"))
from cycle_algebra import (
    NUM_HEX, TRIGRAM_NAMES, TRIGRAM_ELEMENT,
    lower_trigram, upper_trigram, fmt6, fmt3, bit, hugua,
    five_phase_relation,
)

# ─── Palace Constants ───────────────────────────────────────────────────────

RANK_NAMES = ["本宮", "一世", "二世", "三世", "四世", "五世", "游魂", "歸魂"]

# Cumulative XOR masks from root for each rank
PALACE_MASKS = [
    0b000000,  # 本宮
    0b000001,  # 一世: flip b₀
    0b000011,  # 二世: flip b₀,b₁
    0b000111,  # 三世: flip b₀,b₁,b₂
    0b001111,  # 四世: flip b₀,b₁,b₂,b₃
    0b011111,  # 五世: flip b₀,b₁,b₂,b₃,b₄
    0b010111,  # 游魂: un-flip b₃
    0b010000,  # 歸魂: un-flip b₀,b₁,b₂
]

# 世 line by rank (1-indexed)
SHI_BY_RANK = [6, 1, 2, 3, 4, 5, 4, 3]

# Palace roots = 8 doubled trigrams
PALACE_ROOTS = [t | (t << 3) for t in range(8)]

# ─── Basin / Depth / Onion ──────────────────────────────────────────────────

ATTRACTORS = {0b000000, 0b111111, 0b010101, 0b101010}

ONION_LAYER = {1: "outer", 2: "shell", 3: "interface", 4: "interface",
               5: "shell", 6: "outer"}
BASIN_NAMES = ["Kun", "Qian", "Cycle"]


def ying_line(shi):
    """應 = 世 + 3, wrapping within 1-6."""
    y = shi + 3
    return y if y <= 6 else y - 6


def inner_val(h):
    """Pack inner bits b₁..b₄ as integer."""
    return (h >> 1) & 0xF


ATTRACTOR_INNER_VALS = {inner_val(a) for a in ATTRACTORS}


def basin(h):
    b2, b3 = bit(h, 2), bit(h, 3)
    if b2 == 0 and b3 == 0: return "Kun"
    if b2 == 1 and b3 == 1: return "Qian"
    return "Cycle"


def depth(h):
    if h in ATTRACTORS: return 0
    if inner_val(h) in ATTRACTOR_INNER_VALS: return 1
    return 2


def mask_onion(mask):
    """Decompose a 6-bit mask into onion components."""
    return {
        'O': (bit(mask, 0), bit(mask, 5)),
        'M': (bit(mask, 1), bit(mask, 4)),
        'I': (bit(mask, 2), bit(mask, 3)),
    }


def inner_mask(mask):
    """Extract inner 4 bits of a mask (b₁..b₄)."""
    return (mask >> 1) & 0xF


# ─── Palace Generation ─────────────────────────────────────────────────────

def generate_palaces():
    """Generate all 64 hexagram palace assignments.

    Returns:
        entries: list of 64 dicts (one per hexagram)
        hex_info: dict mapping hex_val → entry
    """
    entries = []
    hex_info = {}

    for root in PALACE_ROOTS:
        trig = lower_trigram(root)
        palace = TRIGRAM_NAMES[trig]
        palace_elem = TRIGRAM_ELEMENT[trig]

        for rank, mask in enumerate(PALACE_MASKS):
            h = root ^ mask
            shi = SHI_BY_RANK[rank]
            entry = {
                'hex': h, 'root': root, 'palace': palace,
                'palace_elem': palace_elem,
                'rank': rank, 'rank_name': RANK_NAMES[rank],
                'shi': shi, 'ying': ying_line(shi),
                'shi_layer': ONION_LAYER[shi],
                'basin': basin(h), 'depth': depth(h),
                'inner': inner_val(h),
                'mask': mask,
                'onion': mask_onion(mask),
                'inner_mask': inner_mask(mask),
            }
            entries.append(entry)
            assert h not in hex_info, f"Collision: {h:06b} in {palace} and {hex_info[h]['palace']}"
            hex_info[h] = entry

    assert len(hex_info) == 64, f"Expected 64 unique hexagrams, got {len(hex_info)}"
    return entries, hex_info


# ═══════════════════════════════════════════════════════════════════════════
# Verification
# ═══════════════════════════════════════════════════════════════════════════

def verify(hex_info):
    print("=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    # 姤 should be 乾宮 一世
    gou = 0b111110
    e = hex_info[gou]
    ok1 = e['palace'] == "Qian ☰" and e['rank'] == 1
    print(f"\n  姤 ({fmt6(gou)}): {e['palace']} {e['rank_name']} {'✓' if ok1 else '✗'}")

    # 遁: standard 京房 algorithm → 乾宮 二世
    # (Note: example.md labels it 三世, which appears to be an error)
    dun = 0b111100
    e = hex_info[dun]
    ok2 = e['palace'] == "Qian ☰" and e['rank'] == 2
    print(f"  遁 ({fmt6(dun)}): {e['palace']} {e['rank_name']} {'✓' if ok2 else '✗'}")
    if e['rank'] != 3:
        print(f"    Note: example.md says 三世, algorithm gives {e['rank_name']}")

    # Check attractors' palace positions
    print("\n  Attractor palace positions:")
    for a in sorted(ATTRACTORS):
        e = hex_info[a]
        print(f"    {fmt6(a)}: {e['palace']} {e['rank_name']} (depth={e['depth']})")

    # Check 既濟 and 未濟
    jiji = 0b010101
    weiji = 0b101010
    print(f"\n  既濟 ({fmt6(jiji)}): {hex_info[jiji]['palace']} {hex_info[jiji]['rank_name']}")
    print(f"  未濟 ({fmt6(weiji)}): {hex_info[weiji]['palace']} {hex_info[weiji]['rank_name']}")

    # Print 乾宮 full listing
    print("\n  乾宮 full listing:")
    for e in sorted([v for v in hex_info.values() if v['palace'] == "Qian ☰"],
                    key=lambda x: x['rank']):
        lo, up = lower_trigram(e['hex']), upper_trigram(e['hex'])
        print(f"    {e['rank_name']:4s}: {fmt6(e['hex'])} "
              f"({TRIGRAM_NAMES[lo]}/{TRIGRAM_NAMES[up]}) "
              f"世={e['shi']} basin={e['basin']} depth={e['depth']}")

    return ok1 and ok2


# ═══════════════════════════════════════════════════════════════════════════
# Analysis
# ═══════════════════════════════════════════════════════════════════════════

def analyze_rank_basin(entries):
    """Task 2: rank → basin cross-tabulation."""
    print("\n" + "=" * 60)
    print("RANK → BASIN")
    print("=" * 60)

    table = defaultdict(Counter)
    for e in entries:
        table[e['rank']][e['basin']] += 1

    print(f"\n  {'Rank':6s} | {'Kun':>4} {'Qian':>5} {'Cycle':>6} | Individual basin change?")
    print(f"  {'─'*6}─┼─{'─'*4}─{'─'*5}─{'─'*6}─┼─{'─'*30}")
    for r in range(8):
        row = table[r]
        m = PALACE_MASKS[r]
        changes = (bit(m, 2) ^ bit(m, 3)) == 1
        note = "each hex changes basin from root" if changes else ""
        print(f"  {RANK_NAMES[r]:4s}   | {row['Kun']:>4} {row['Qian']:>5} {row['Cycle']:>6} | {note}")

    # Basin change analysis
    print("\n  Basin change from root:")
    for r in range(8):
        mask = PALACE_MASKS[r]
        b2m, b3m = bit(mask, 2), bit(mask, 3)
        flips_basin = (b2m ^ b3m) == 1
        print(f"    {RANK_NAMES[r]:4s}: mask interface=({b2m},{b3m}) → "
              f"{'CHANGES' if flips_basin else 'preserves'} basin")

    return table


def analyze_rank_depth(entries):
    """Task 3: rank → convergence depth."""
    print("\n" + "=" * 60)
    print("RANK → DEPTH")
    print("=" * 60)

    table = defaultdict(Counter)
    for e in entries:
        table[e['rank']][e['depth']] += 1

    print(f"\n  {'Rank':6s} | {'d=0':>4} {'d=1':>4} {'d=2':>4}")
    print(f"  {'─'*6}─┼─{'─'*4}─{'─'*4}─{'─'*4}")
    for r in range(8):
        row = table[r]
        print(f"  {RANK_NAMES[r]:4s}   | {row[0]:>4} {row[1]:>4} {row[2]:>4}")

    # Which roots hit attractor inner values at each rank?
    print("\n  Rank → inner mask → which roots produce depth ≤ 1:")
    for r in range(8):
        im = inner_mask(PALACE_MASKS[r])
        hits = []
        for root in PALACE_ROOTS:
            rv = inner_val(root)
            new_v = rv ^ im
            if new_v in ATTRACTOR_INNER_VALS:
                h = root ^ PALACE_MASKS[r]
                d = depth(h)
                hits.append(f"{TRIGRAM_NAMES[lower_trigram(root)]}(d{d})")
        if hits:
            print(f"    {RANK_NAMES[r]:4s} (imask={im:04b}): {', '.join(hits)}")
        else:
            print(f"    {RANK_NAMES[r]:4s} (imask={im:04b}): none")

    return table


def analyze_inner_masks():
    """Task 4: inner XOR mask decomposition by rank."""
    print("\n" + "=" * 60)
    print("INNER XOR MASK DECOMPOSITION")
    print("=" * 60)

    print(f"\n  {'Rank':6s} | {'Mask':>6} | {'O(b₀,b₅)':>9} {'M(b₁,b₄)':>9} {'I(b₂,b₃)':>9} | inner | ker? | im?")
    print(f"  {'─'*6}─┼─{'─'*6}─┼─{'─'*9}─{'─'*9}─{'─'*9}─┼─{'─'*5}─┼─{'─'*4}─┼─{'─'*3}")

    # ker(M_inner) = {v : b₂=0, b₃=0} in inner space
    # im(M_inner) = {(b₂,b₃,b₂,b₃)} = {v : b₁=b₃, b₂=b₄}
    def in_ker(v):
        return bit(v, 1) == 0 and bit(v, 2) == 0  # b₂=0, b₃=0

    def in_im(v):
        return bit(v, 0) == bit(v, 2) and bit(v, 1) == bit(v, 3)  # b₁=b₃, b₂=b₄

    for r in range(8):
        mask = PALACE_MASKS[r]
        o = mask_onion(mask)
        im_val = inner_mask(mask)
        ik = in_ker(im_val)
        ii = in_im(im_val)
        print(f"  {RANK_NAMES[r]:4s}   | {mask:06b} | {str(o['O']):>9} {str(o['M']):>9} {str(o['I']):>9} "
              f"| {im_val:04b}  | {'✓' if ik else ' ':>4} | {'✓' if ii else ' ':>3}")

    # Progression narrative
    print("\n  Onion penetration by rank:")
    for r in range(8):
        o = mask_onion(PALACE_MASKS[r])
        touches = []
        if any(o['O']): touches.append("outer")
        if any(o['M']): touches.append("shell")
        if any(o['I']): touches.append("interface")
        print(f"    {RANK_NAMES[r]:4s}: {' + '.join(touches) if touches else '(identity)'}")

    # b₅ never touched
    b5_ever = any(bit(m, 5) for m in PALACE_MASKS)
    print(f"\n  b₅ (line 6, top line) flipped by any mask: {'YES' if b5_ever else 'NEVER'}")
    print(f"  → Line 6 is the palace invariant. 本宮 places 世 at this invariant position.")


def analyze_shi_onion(entries):
    """Task 5: 世 line → onion layer mapping."""
    print("\n" + "=" * 60)
    print("世 LINE → ONION LAYER")
    print("=" * 60)

    print(f"\n  {'Rank':6s} | 世 line | bit  | layer")
    print(f"  {'─'*6}─┼─{'─'*7}─┼─{'─'*4}─┼─{'─'*9}")
    for r in range(8):
        shi = SHI_BY_RANK[r]
        layer = ONION_LAYER[shi]
        bit_name = f"b{shi-1}"
        print(f"  {RANK_NAMES[r]:4s}   | {shi:>5}   | {bit_name:>4} | {layer}")

    # Count by layer
    layer_ranks = defaultdict(list)
    for r in range(8):
        layer_ranks[ONION_LAYER[SHI_BY_RANK[r]]].append(RANK_NAMES[r])

    print(f"\n  世 on outer:     {', '.join(layer_ranks['outer'])} (2 ranks)")
    print(f"  世 on shell:     {', '.join(layer_ranks['shell'])} (2 ranks)")
    print(f"  世 on interface: {', '.join(layer_ranks['interface'])} (4 ranks)")

    # Basin distribution for 世-on-interface hexagrams
    interface_ranks = [r for r in range(8) if ONION_LAYER[SHI_BY_RANK[r]] == "interface"]
    print(f"\n  Basin distribution for 世-on-interface ({len(interface_ranks)} ranks × 8 palaces = "
          f"{len(interface_ranks)*8} hexagrams):")
    basin_count = Counter()
    for e in entries:
        if e['rank'] in interface_ranks:
            basin_count[e['basin']] += 1
    for b in BASIN_NAMES:
        print(f"    {b}: {basin_count[b]}")

    # Compare with 世-on-outer and 世-on-shell
    for layer_name in ["outer", "shell"]:
        ranks = [r for r in range(8) if ONION_LAYER[SHI_BY_RANK[r]] == layer_name]
        bc = Counter(e['basin'] for e in entries if e['rank'] in ranks)
        print(f"  世 on {layer_name} ({len(ranks)} ranks × 8 = {len(ranks)*8}):")
        for b in BASIN_NAMES:
            print(f"    {b}: {bc[b]}")


def analyze_cross_tab(entries):
    """Task 6: full cross-tabulation rank × basin × depth."""
    print("\n" + "=" * 60)
    print("CROSS-TABULATION: RANK × BASIN × DEPTH")
    print("=" * 60)

    # 3D table
    table = defaultdict(int)
    for e in entries:
        table[(e['rank'], e['basin'], e['depth'])] += 1

    print(f"\n  {'Rank':6s} | {'Kun':^12s} | {'Qian':^12s} | {'Cycle':^12s}")
    print(f"  {'':6s} | {'d0 d1 d2':^12s} | {'d0 d1 d2':^12s} | {'d0 d1 d2':^12s}")
    print(f"  {'─'*6}─┼─{'─'*12}─┼─{'─'*12}─┼─{'─'*12}")

    for r in range(8):
        parts = []
        for b in BASIN_NAMES:
            cells = [table.get((r, b, d), 0) for d in range(3)]
            parts.append(f"{cells[0]:>2} {cells[1]:>2} {cells[2]:>2}   ")
        print(f"  {RANK_NAMES[r]:4s}   | {'| '.join(parts)}")

    # Column totals
    print(f"  {'─'*6}─┼─{'─'*12}─┼─{'─'*12}─┼─{'─'*12}")
    parts = []
    for b in BASIN_NAMES:
        cells = [sum(table.get((r, b, d), 0) for r in range(8)) for d in range(3)]
        parts.append(f"{cells[0]:>2} {cells[1]:>2} {cells[2]:>2}   ")
    print(f"  {'Total':6s} | {'| '.join(parts)}")

    # Attractor locations
    print("\n  Attractor locations in rank × basin space:")
    for e in entries:
        if e['depth'] == 0:
            print(f"    {fmt6(e['hex'])}: {e['palace']} {e['rank_name']} → basin={e['basin']}")


def analyze_palace_element_vs_basin(entries):
    """Task 7: palace element vs basin attractor element."""
    print("\n" + "=" * 60)
    print("PALACE ELEMENT vs BASIN ATTRACTOR ELEMENT")
    print("=" * 60)

    # Basin attractor elements
    basin_elem = {"Kun": "Earth", "Qian": "Metal", "Cycle": "Fire/Water"}
    # For Cycle basin: both attractors have elements (既濟→Water in 坎宮, 未濟→Fire in 離宮)
    # But the BASIN doesn't have a single element — use both

    print(f"\n  Basin attractor elements: Kun=Earth(坤), Qian=Metal(乾), Cycle=mixed")

    # For each rank, list palace_element × basin pairs
    for r in range(8):
        rank_entries = [e for e in entries if e['rank'] == r]
        print(f"\n  {RANK_NAMES[r]}:")
        for e in sorted(rank_entries, key=lambda x: x['basin']):
            pe = e['palace_elem']
            b = e['basin']
            if b == "Kun":
                be = "Earth"
                rel = five_phase_relation(pe, be) if pe != be else "比和"
            elif b == "Qian":
                be = "Metal"
                rel = five_phase_relation(pe, be) if pe != be else "比和"
            else:
                be = "—"
                rel = "—"
            print(f"    {e['palace']:10s} ({pe:>5}) → {b:5s} ({be:>5}) : {rel}")


# ═══════════════════════════════════════════════════════════════════════════
# Findings
# ═══════════════════════════════════════════════════════════════════════════

def write_findings(entries, hex_info, rank_basin, rank_depth):
    lines = []
    w = lines.append

    w("# Probe 2: Palace Generation in Kernel Language\n")

    # ── 1. Palace generation ──
    w("## 1. Palace Generation Verified\n")
    w("Standard 京房 algorithm: from doubled root TT, cumulatively flip")
    w("b₀→b₄ (ranks 1–5), un-flip b₃ (游魂), un-flip b₀,b₁,b₂ (歸魂).\n")
    w("All 64 hexagrams uniquely assigned to 8 palaces × 8 ranks. ✓\n")

    w("### Cumulative XOR masks\n")
    w("| Rank | Mask | Bits flipped |")
    w("|------|------|-------------|")
    bit_labels = {0: "b₀", 1: "b₁", 2: "b₂", 3: "b₃", 4: "b₄", 5: "b₅"}
    for r in range(8):
        m = PALACE_MASKS[r]
        flipped = [bit_labels[i] for i in range(6) if bit(m, i)]
        w(f"| {RANK_NAMES[r]} | {m:06b} | {', '.join(flipped) if flipped else '(none)'} |")
    w("")

    w("**Key observation:** b₅ (line 6) is NEVER flipped. The top line is the palace")
    w("invariant — the unchanging bit across all 8 members. 本宮 places 世 at this")
    w("invariant position (世=6).\n")

    w("### Verification\n")
    gou = hex_info[0b111110]
    dun = hex_info[0b111100]
    w(f"- 姤 (111110): {gou['palace']} {gou['rank_name']} ✓")
    w(f"- 遁 (111100): {dun['palace']} {dun['rank_name']}")
    w(f"  (Note: example.md labels 遁 as 三世. Standard 京房 algorithm gives 二世.)\n")

    # ── 2. Rank → basin ──
    w("## 2. Rank → Basin\n")
    w("| Rank | Kun | Qian | Cycle | Basin change? |")
    w("|------|-----|------|-------|---------------|")
    for r in range(8):
        row = rank_basin[r]
        m = PALACE_MASKS[r]
        changes = (bit(m, 2) ^ bit(m, 3)) == 1
        w(f"| {RANK_NAMES[r]} | {row['Kun']} | {row['Qian']} | {row['Cycle']} | "
          f"{'Yes' if changes else 'No'} |")
    w("")

    w("**The distribution is 2-2-4 at every rank** — perfectly uniform. Rank and basin")
    w("are statistically independent.\n")
    w("At ranks 3 and 6, every individual hexagram changes basin from its root (the mask")
    w("flips b₂ but not b₃, toggling b₂⊕b₃). But the aggregate distribution is preserved")
    w("because the root distribution is already 2-2-4 and the basin permutation is symmetric:")
    w("Kun↔Cycle (for roots with b₃=0), Qian↔Cycle (for roots with b₃=1).\n")

    # ── 3. Rank → depth ──
    w("## 3. Rank → Depth\n")
    w("| Rank | d=0 | d=1 | d=2 |")
    w("|------|-----|-----|-----|")
    for r in range(8):
        row = rank_depth[r]
        w(f"| {RANK_NAMES[r]} | {row[0]} | {row[1]} | {row[2]} |")
    w("")

    # Attractor positions
    w("### Attractor positions\n")
    w("| Attractor | Palace | Rank |")
    w("|-----------|--------|------|")
    for e in entries:
        if e['depth'] == 0:
            w(f"| {fmt6(e['hex'])} | {e['palace']} | {e['rank_name']} |")
    w("")
    w("The two **fixed-point** attractors (乾, 坤) sit at **rank 0** (本宮) — the palace roots.\n")
    w("The two **cycle** attractors (既濟, 未濟) sit at **rank 3** (三世) — the rank where")
    w("the palace algorithm first penetrates the interface layer. The oscillating attractors")
    w("appear exactly when the generation walk reaches the basin-determining core.\n")

    # ── 4. Inner mask decomposition ──
    w("## 4. Inner XOR Mask — Onion Decomposition\n")
    w("| Rank | Full mask | O(b₀,b₅) | M(b₁,b₄) | I(b₂,b₃) | Inner | ker(M)? | im(M)? |")
    w("|------|-----------|-----------|-----------|-----------|-------|---------|--------|")
    for r in range(8):
        m = PALACE_MASKS[r]
        o = mask_onion(m)
        iv = inner_mask(m)
        ik = bit(iv, 1) == 0 and bit(iv, 2) == 0
        ii = bit(iv, 0) == bit(iv, 2) and bit(iv, 1) == bit(iv, 3)
        w(f"| {RANK_NAMES[r]} | {m:06b} | {o['O']} | {o['M']} | {o['I']} | "
          f"{iv:04b} | {'✓' if ik else ''} | {'✓' if ii else ''} |")
    w("")

    w("### The palace walk as onion traversal\n")
    w("```")
    w("Rank 0 (本宮):  identity         — no change")
    w("Rank 1 (一世):  outer only        — surface perturbation")
    w("Rank 2 (二世):  outer + shell     — enters ker(M)")
    w("Rank 3 (三世):  + one interface   — CROSSES into core ← basin changes")
    w("Rank 4 (四世):  + both interface  — full core engagement (basin returns)")
    w("Rank 5 (五世):  all inner bits    — complete inner inversion ∈ im(M)")
    w("Rank 6 (游魂):  partial retract   — un-flip one interface ← basin changes again")
    w("Rank 7 (歸魂):  shell only        — returns to ker(M)")
    w("```\n")
    w("The palace generation is a **drill-in, then retract** pattern through the onion.")
    w("It starts at the surface, penetrates to the core, then partially withdraws.\n")

    # ── 5. 世 → onion layer ──
    w("## 5. 世 Line → Onion Layer\n")
    w("| Rank | 世 | 應 | 世 layer | 應 layer |")
    w("|------|----|----|----------|----------|")
    for r in range(8):
        shi = SHI_BY_RANK[r]
        ying = ying_line(shi)
        w(f"| {RANK_NAMES[r]} | L{shi} (b{shi-1}) | L{ying} (b{ying-1}) | "
          f"{ONION_LAYER[shi]} | {ONION_LAYER[ying]} |")
    w("")

    w("### Layer occupancy count\n")
    layer_count = Counter(ONION_LAYER[SHI_BY_RANK[r]] for r in range(8))
    w("| Layer | Ranks with 世 | Count |")
    w("|-------|--------------|-------|")
    for layer in ["outer", "shell", "interface"]:
        ranks = [RANK_NAMES[r] for r in range(8) if ONION_LAYER[SHI_BY_RANK[r]] == layer]
        w(f"| {layer} | {', '.join(ranks)} | {len(ranks)} |")
    w("")

    w("**Interface gets the most 世 occupancy** (4 of 8 ranks). The querent's self (世)")
    w("sits on the basin-determining bits at ranks 三世, 四世, 游魂, 歸魂. At these ranks,")
    w("the structural core of the hexagram is literally the querent's position.\n")

    w("### 世-on-interface basin distribution\n")
    interface_ranks = {r for r in range(8) if ONION_LAYER[SHI_BY_RANK[r]] == "interface"}
    bc = Counter(e['basin'] for e in entries if e['rank'] in interface_ranks)
    w(f"32 hexagrams with 世 on interface: Kun={bc['Kun']}, Qian={bc['Qian']}, Cycle={bc['Cycle']}")
    w(f"(Compare uniform: 8, 8, 16 for the Kun/Qian/Cycle ratio.)\n")

    # ── 6. Cross-tabulation ──
    w("## 6. Full Cross-Tabulation: Rank × Basin × Depth\n")
    table = defaultdict(int)
    for e in entries:
        table[(e['rank'], e['basin'], e['depth'])] += 1

    w("```")
    w(f"{'Rank':6s}  Kun(d0,d1,d2)  Qian(d0,d1,d2)  Cycle(d0,d1,d2)")
    w("─" * 60)
    for r in range(8):
        parts = []
        for b in BASIN_NAMES:
            cells = [table.get((r, b, d), 0) for d in range(3)]
            parts.append(f"  {cells[0]:>1}  {cells[1]:>1}  {cells[2]:>1}  ")
        w(f"{RANK_NAMES[r]:4s}  {''.join(parts)}")
    w("```\n")

    # Summary statistics
    total_d0 = sum(1 for e in entries if e['depth'] == 0)
    total_d1 = sum(1 for e in entries if e['depth'] == 1)
    total_d2 = sum(1 for e in entries if e['depth'] == 2)
    w(f"Totals: depth-0={total_d0}, depth-1={total_d1}, depth-2={total_d2} (of 64)\n")

    # ── 7. Key findings ──
    w("## 7. Key Findings\n")

    w("### Finding 1: Palace walk = onion traversal\n")
    w("The palace generation algorithm is a structured walk through the three-layer onion:")
    w("outer → shell → interface → (retract). This is NOT coincidental — the algorithm")
    w("cumulatively flips bits from b₀ inward, which exactly follows the onion layers.\n")

    w("### Finding 2: Attractors mark structural boundaries\n")
    w("Fixed-point attractors (乾, 坤) = palace roots (rank 0).")
    w("Cycle attractors (既濟, 未濟) = rank 3 (first interface penetration).")
    w("The 4 attractors of the 互 system appear at exactly the two structurally")
    w("distinguished ranks in the palace system.\n")

    w("### Finding 3: Basin distribution invariant across ranks\n")
    w("Despite individual hexagrams changing basins at ranks 3 and 6 (where the mask")
    w("toggles b₂⊕b₃), the aggregate distribution 2-2-4 (Kun-Qian-Cycle) is identical")
    w("at every rank. The root basin distribution happens to be 2-2-4 (坤/坎 in Kun,")
    w("乾/離 in Qian, 4 others in Cycle), and the basin permutation at ranks 3/6")
    w("preserves this ratio.\n")

    w("### Finding 4: 世 favors the interface\n")
    w("The 世 line occupies the interface (b₂ or b₃) at 4 of 8 ranks — double the")
    w("frequency of outer or shell. When 世 sits on an interface bit, the querent's")
    w("identity is bound to the basin-determining structure.\n")

    w("### Finding 5: Line 6 is the palace invariant\n")
    w("b₅ (line 6, top line) is never touched by the palace algorithm. It is the only")
    w("bit that stays constant across all 8 members of any palace. The 本宮 hexagram")
    w("places 世 precisely at this invariant — the self is anchored to what never changes.\n")

    w("### Finding 6: 世 and 應 sit on complementary layers\n")
    w("世 and 應 are always 3 lines apart. The line pairs (1,4), (2,5), (3,6) map to")
    w("layer pairs (outer,interface), (shell,shell), (interface,outer). So 世 and 應")
    w("always occupy complementary onion layers — when the self is on the surface,")
    w("the other is at the core, and vice versa. The only exception is shell-shell")
    w("(二世, 五世), where both sit at the same depth.\n")

    w("### Finding 7: Rank ≠ depth (orthogonality maintained)\n")
    w("There is no rank that concentrates depth-0 or depth-1 hexagrams beyond what")
    w("the attractor positions force. The 1:3:12 ratio within basins means most cells")
    w("in the rank×basin×depth table are sparse. Rank and convergence depth are")
    w("effectively independent coordinates.\n")

    out = Path(__file__).parent / "02_findings.md"
    out.write_text("\n".join(lines))
    print(f"\nFindings → {out}")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    entries, hex_info = generate_palaces()

    if not verify(hex_info):
        print("\n*** VERIFICATION ISSUE ***")

    rank_basin = analyze_rank_basin(entries)
    rank_depth = analyze_rank_depth(entries)
    analyze_inner_masks()
    analyze_shi_onion(entries)
    analyze_cross_tab(entries)
    analyze_palace_element_vs_basin(entries)
    write_findings(entries, hex_info, rank_basin, rank_depth)


if __name__ == "__main__":
    main()
