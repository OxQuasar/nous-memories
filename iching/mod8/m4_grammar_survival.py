#!/usr/bin/env python3
"""Probe M4: Grammar (GMS/valve) survival at hexagram level.

For a fixed day (upper_raw = (Y+M+D) mod 8), hour H ∈ {1..12} sweeps out a
12-step 体用 sequence. We test whether the GMS grammar (no consecutive 克) and
the valve (克→生 = 0) survive the passage from the Q₃ trigram cycle to the
mod-8 hexagram formula.

Three possible outcomes:
  1. GMS holds at undirected level → grammar visible at coarsest level
  2. GMS fails undirected, holds directed → mod-6 体 assignment acts as filter
  3. GMS fails at both levels → grammar does not survive
"""

from collections import Counter, defaultdict

# ─── Definitions (from m3) ───────────────────────────────────────────────

XIANTIAN = [
    (1, "乾", (1,1,1)), (2, "兌", (0,1,1)), (3, "離", (1,0,1)), (4, "震", (0,0,1)),
    (5, "巽", (1,1,0)), (6, "坎", (0,1,0)), (7, "艮", (1,0,0)), (8, "坤", (0,0,0)),
]

NAMES = {v: name for _, name, v in XIANTIAN}
POS   = {v: pos  for pos, _, v in XIANTIAN}
VEC   = {pos: v  for pos, _, v in XIANTIAN}
NAME_BY_POS = {pos: name for pos, name, _ in XIANTIAN}

WUXING_MAP = {
    (1,1,1): 0, (0,1,1): 0, (0,1,0): 1,
    (0,0,1): 2, (1,1,0): 2, (1,0,1): 3,
    (0,0,0): 4, (1,0,0): 4,
}
Z5_NAMES = {0: "Metal", 1: "Water", 2: "Wood", 3: "Fire", 4: "Earth"}

def wuxing_type(a, b):
    """Undirected 五行 relation: 比和/生/克."""
    d = abs(a - b); d = min(d, 5 - d)
    return {0: "比和", 1: "生", 2: "克"}[d]

def directed_rel(ti_wx, yong_wx):
    """Directed relation from 体's perspective.
    diff = (用-体) mod 5:
      0 → 比和, 1 → 体生用, 2 → 体克用, 3 → 克体, 4 → 生体
    """
    return {0: "比和", 1: "体生用", 2: "体克用", 3: "克体", 4: "生体"}[(yong_wx - ti_wx) % 5]

def raw_to_pos(r):
    """Mod-8 raw value (0-7) to 先天 position (1-8). 0 → 8."""
    return 8 if r == 0 else r

DIZHI_NAMES = {
    1: "子", 2: "丑", 3: "寅", 4: "卯", 5: "辰", 6: "巳",
    7: "午", 8: "未", 9: "申", 10: "酉", 11: "戌", 12: "亥",
}

# ─── Helpers ─────────────────────────────────────────────────────────────

def moving_lines_for(lower_raw):
    """Return the 3 possible moving line values given lower_raw = S mod 8.
    S mod 6 ∈ {r%6, (r+2)%6, (r+4)%6}, with 0→6.
    """
    ml_raws = [(lower_raw + 2 * k) % 6 for k in range(3)]
    return [6 if m == 0 else m for m in ml_raws]

def directed_for_ml(uw, lw, ml):
    """Compute directed relation given a specific moving line.
    ml 1-3: upper=体 (line in lower trigram → lower changes).
    ml 4-6: lower=体 (line in upper trigram → upper changes).
    """
    if ml <= 3:
        return directed_rel(uw, lw)  # upper = 体
    else:
        return directed_rel(lw, uw)  # lower = 体

def hour_data(u, H):
    """Compute all data for a (upper_raw, hour) pair.
    Returns: (lower_raw, uw, lw, utype, moving_lines, directed_options)
    """
    r = (u + H) % 8
    up, lp = raw_to_pos(u), raw_to_pos(r)
    uw, lw = WUXING_MAP[VEC[up]], WUXING_MAP[VEC[lp]]
    utype = wuxing_type(uw, lw)
    mls = moving_lines_for(r)
    dirs = [directed_for_ml(uw, lw, ml) for ml in mls]
    return r, uw, lw, utype, mls, dirs


# ═══════════════════════════════════════════════════════════════════════════
# 1. PER-UPPER 12-HOUR UNDIRECTED SEQUENCES
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 100)
print("1. PER-UPPER 12-HOUR UNDIRECTED SEQUENCES")
print("=" * 100)
print("For each upper_raw u ∈ {0..7}, the 12-hour sequence of undirected 五行 types.")
print("★ = consecutive 克 pair (GMS violation)")

TYPE_SHORT = {"比和": "比", "生": "生", "克": "克"}

all_undirected_seqs = {}  # u → [type for H=1..12]

for u in range(8):
    up = raw_to_pos(u)
    uw = WUXING_MAP[VEC[up]]
    seq = []
    for H in range(1, 13):
        r, _, _, utype, _, _ = hour_data(u, H)
        seq.append(utype)
    all_undirected_seqs[u] = seq

    # Find consecutive 克
    consec_ke = []
    for i in range(11):
        if seq[i] == "克" and seq[i+1] == "克":
            consec_ke.append(i+1)  # 1-indexed hour

    up_name = NAME_BY_POS[up]
    print(f"\n  u={u} ({up_name}, {Z5_NAMES[uw]})")
    # Header
    hours_hdr = " ".join(f"{DIZHI_NAMES[H]:>3}" for H in range(1, 13))
    print(f"  Hour:  {hours_hdr}")
    shifts_hdr = " ".join(f"{H%8:>3}" for H in range(1, 13))
    print(f"  Shift: {shifts_hdr}")

    # Show lower trigram names
    lowers = []
    for H in range(1, 13):
        r = (u + H) % 8
        lp = raw_to_pos(r)
        lowers.append(NAME_BY_POS[lp])
    lower_hdr = " ".join(f"{n:>3}" for n in lowers)
    print(f"  Lower: {lower_hdr}")

    # Show types with markers
    type_strs = []
    for i, t in enumerate(seq):
        marker = "★" if i in [c-1 for c in consec_ke] or i in [c for c in consec_ke] else " "
        type_strs.append(f"{TYPE_SHORT[t]}{marker}")
    type_hdr = " ".join(f"{s:>3}" for s in type_strs)
    print(f"  Type:  {type_hdr}")

    counts = Counter(seq)
    viol = len(consec_ke)
    print(f"  Counts: 比和={counts.get('比和',0)}, 生={counts.get('生',0)}, 克={counts.get('克',0)}"
          f"  | Consecutive 克 pairs: {viol}")

# ═══════════════════════════════════════════════════════════════════════════
# 2. PER-UPPER 12-HOUR DIRECTED SEQUENCES
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 100)
print("2. PER-UPPER 12-HOUR DIRECTED SEQUENCES (with moving line uncertainty)")
print("=" * 100)
print("For each hour: 3 equally likely moving lines → 3 possible directed relations.")
print("Showing probability-weighted most-likely direction + all 3 options.")

DIR_SHORT = {"比和": "比和", "生体": "生体", "体生用": "体生", "体克用": "体克", "克体": "克体"}

all_directed_options = {}  # u → [[(dir, ml), ...] for H=1..12]

for u in range(8):
    up = raw_to_pos(u)
    uw = WUXING_MAP[VEC[up]]

    hour_options = []
    for H in range(1, 13):
        r, _, lw_h, utype, mls, dirs = hour_data(u, H)
        hour_options.append((r, utype, mls, dirs))
    all_directed_options[u] = hour_options

    up_name = NAME_BY_POS[up]
    print(f"\n  u={u} ({up_name}, {Z5_NAMES[uw]})")
    print(f"  {'H':>3} {'地支':>3} {'shift':>5} {'lower':>5} {'undir':>5} │ {'ml₁':>3}→{'dir₁':>4}  {'ml₂':>3}→{'dir₂':>4}  {'ml₃':>3}→{'dir₃':>4}  │ {'P(克体)':>7}")
    print(f"  " + "─" * 85)

    for H in range(1, 13):
        r, utype, mls, dirs = hour_options[H-1]
        lp = raw_to_pos(r)
        lw_h = WUXING_MAP[VEC[lp]]
        shift = H % 8

        ml_dir_strs = []
        for ml, d in zip(mls, dirs):
            ml_dir_strs.append(f"{ml:>3}→{DIR_SHORT[d]:>4}")

        p_keti = sum(1 for d in dirs if d == "克体") / 3
        print(f"  {H:>3} {DIZHI_NAMES[H]:>3} {shift:>5} {NAME_BY_POS[lp]:>5} {TYPE_SHORT[utype]:>5} │ "
              + "  ".join(ml_dir_strs) + f"  │ {p_keti:>7.3f}")


# ═══════════════════════════════════════════════════════════════════════════
# 3. GMS TEST — UNDIRECTED
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 100)
print("3. GMS TEST — UNDIRECTED (consecutive 克 = violation)")
print("=" * 100)

total_pairs = 0
total_ke_ke = 0
# Also count transition types
trans_counts = Counter()  # (type_h, type_h+1) → count

print(f"\n  {'upper':>8} {'Name':>5} {'Consec 克':>10} {'Pairs':>6}")
print(f"  " + "─" * 35)

for u in range(8):
    up = raw_to_pos(u)
    seq = all_undirected_seqs[u]
    ke_ke = 0
    for i in range(11):
        trans_counts[(seq[i], seq[i+1])] += 1
        total_pairs += 1
        if seq[i] == "克" and seq[i+1] == "克":
            ke_ke += 1
            total_ke_ke += 1
    print(f"  raw={u:>3} {NAME_BY_POS[up]:>5} {ke_ke:>10} {11:>6}")

print(f"\n  TOTAL consecutive 克 pairs: {total_ke_ke} / {total_pairs}")
print(f"  GMS violation rate: {total_ke_ke/total_pairs*100:.1f}%")
print(f"  GMS HOLDS at undirected level? {'YES' if total_ke_ke == 0 else 'NO'}")

# ═══════════════════════════════════════════════════════════════════════════
# 4. GMS TEST — DIRECTED (worst case over moving line assignments)
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 100)
print("4. GMS TEST — DIRECTED (consecutive 克体 under ANY moving line assignment)")
print("=" * 100)
print("For each undirected 克-克 pair: check all 9 moving-line combos for 克体-克体.")

directed_violations = 0
directed_possible = 0

print(f"\n  {'upper':>5} {'H→H+1':>8} {'Lower₁':>7} {'Lower₂':>7} │ {'combos':>6} {'克体-克体':>9} │ {'exists?':>7}")
print(f"  " + "─" * 65)

for u in range(8):
    seq = all_undirected_seqs[u]
    options = all_directed_options[u]
    for i in range(11):
        if seq[i] != "克" or seq[i+1] != "克":
            continue
        directed_possible += 1

        H1, H2 = i + 1, i + 2
        r1, _, mls1, dirs1 = options[i]
        r2, _, mls2, dirs2 = options[i+1]

        # Check all 9 combos
        ke_ke_count = 0
        for d1 in dirs1:
            for d2 in dirs2:
                if d1 == "克体" and d2 == "克体":
                    ke_ke_count += 1

        exists = ke_ke_count > 0
        if exists:
            directed_violations += 1

        lp1 = NAME_BY_POS[raw_to_pos(r1)]
        lp2 = NAME_BY_POS[raw_to_pos(r2)]
        up_name = NAME_BY_POS[raw_to_pos(u)]
        print(f"  {up_name:>5} {DIZHI_NAMES[H1]:>3}→{DIZHI_NAMES[H2]:<3} {lp1:>7} {lp2:>7} │ {9:>6} {ke_ke_count:>9} │ {'YES ✗' if exists else 'NO  ✓':>7}")

print(f"\n  Undirected 克-克 pairs: {directed_possible}")
print(f"  Of those, with ≥1 克体-克体 assignment: {directed_violations}")
if directed_possible > 0:
    print(f"  Directed GMS violation rate (worst case): {directed_violations/directed_possible*100:.1f}% of 克-克 pairs")
print(f"  Directed GMS violation rate (overall): {directed_violations}/{total_pairs} = {directed_violations/total_pairs*100:.1f}%")
print(f"  Directed GMS HOLDS (worst case)? {'YES' if directed_violations == 0 else 'NO'}")

# Also: expected 克体-克体 probability (each hour independently 1/3 or 2/3 for each direction)
print(f"\n  EXPECTED 克体-克体 PROBABILITY for each undirected 克-克 pair:")
print(f"  {'upper':>5} {'H→H+1':>8} {'P(克体)₁':>9} {'P(克体)₂':>9} {'P(both)':>8}")
print(f"  " + "─" * 45)

expected_total = 0.0
for u in range(8):
    seq = all_undirected_seqs[u]
    options = all_directed_options[u]
    for i in range(11):
        if seq[i] != "克" or seq[i+1] != "克":
            continue
        H1, H2 = i + 1, i + 2
        _, _, _, dirs1 = options[i]
        _, _, _, dirs2 = options[i+1]

        p1 = sum(1 for d in dirs1 if d == "克体") / 3
        p2 = sum(1 for d in dirs2 if d == "克体") / 3
        p_both = p1 * p2

        up_name = NAME_BY_POS[raw_to_pos(u)]
        expected_total += p_both
        print(f"  {up_name:>5} {DIZHI_NAMES[H1]:>3}→{DIZHI_NAMES[H2]:<3} {p1:>9.3f} {p2:>9.3f} {p_both:>8.4f}")

print(f"\n  Expected total 克体-克体 events (sum of probabilities): {expected_total:.4f}")
print(f"  Expected per total pairs: {expected_total/total_pairs*100:.2f}%")

# ═══════════════════════════════════════════════════════════════════════════
# 5. VALVE TEST (克→生 suppression)
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 100)
print("5. VALVE TEST (克→生 should be suppressed)")
print("=" * 100)

print(f"\n  UNDIRECTED TRANSITION MATRIX (rows=from, cols=to):")
types = ["比和", "生", "克"]
print(f"  {'':>6}", end="")
for t in types:
    print(f" {TYPE_SHORT[t]:>6}", end="")
print(f" {'Total':>6}")
print(f"  " + "─" * 30)

for t1 in types:
    row_total = sum(trans_counts.get((t1, t2), 0) for t2 in types)
    print(f"  {TYPE_SHORT[t1]:>6}", end="")
    for t2 in types:
        c = trans_counts.get((t1, t2), 0)
        print(f" {c:>6}", end="")
    print(f" {row_total:>6}")

ke_sheng = trans_counts.get(("克", "生"), 0)
sheng_ke = trans_counts.get(("生", "克"), 0)
ke_total = sum(trans_counts.get(("克", t), 0) for t in types)
sheng_total = sum(trans_counts.get(("生", t), 0) for t in types)

print(f"\n  克→生 transitions: {ke_sheng} / {ke_total} ({ke_sheng/ke_total*100:.1f}% of 克-outgoing)" if ke_total > 0 else "")
print(f"  生→克 transitions: {sheng_ke} / {sheng_total} ({sheng_ke/sheng_total*100:.1f}% of 生-outgoing)" if sheng_total > 0 else "")
print(f"  VALVE HOLDS (克→生 = 0)? {'YES' if ke_sheng == 0 else 'NO'}")

# Per-upper valve detail
print(f"\n  PER-UPPER 克→生 DETAIL:")
for u in range(8):
    seq = all_undirected_seqs[u]
    ke_s = 0
    for i in range(11):
        if seq[i] == "克" and seq[i+1] == "生":
            ke_s += 1
    up_name = NAME_BY_POS[raw_to_pos(u)]
    print(f"    u={u} ({up_name}): 克→生 = {ke_s}")

# Null expectation for transition counts
print(f"\n  NULL EXPECTATION:")
print(f"  If types were drawn i.i.d. from ergodic distribution (比和≈17.7%, 生≈39.6%, 克≈42.7%):")
p_bi = 17.71 / 100
p_sheng = 39.58 / 100
p_ke = 42.71 / 100
null_ke_sheng = p_ke * p_sheng * total_pairs
null_ke_ke = p_ke * p_ke * total_pairs
print(f"    Expected 克→生: {null_ke_sheng:.1f}")
print(f"    Expected 克→克: {null_ke_ke:.1f}")
print(f"    Actual   克→生: {ke_sheng}")
print(f"    Actual   克→克: {total_ke_ke}")

# ═══════════════════════════════════════════════════════════════════════════
# 6. SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 100)
print("6. SUMMARY")
print("=" * 100)

print(f"""
  ╔═══════════════════════════════════════════════════════════════════════╗
  ║  TEST                                          RESULT               ║
  ╠═══════════════════════════════════════════════════════════════════════╣
  ║  GMS undirected (no consecutive 克):           {'PASS ✓' if total_ke_ke == 0 else f'FAIL ✗ ({total_ke_ke}/{total_pairs})':>20} ║
  ║  GMS directed worst-case (no 克体-克体):       {'PASS ✓' if directed_violations == 0 else f'FAIL ✗ ({directed_violations}/{total_pairs})':>20} ║
  ║  Valve (克→生 = 0):                            {'PASS ✓' if ke_sheng == 0 else f'FAIL ✗ ({ke_sheng}/{ke_total})':>20} ║
  ╚═══════════════════════════════════════════════════════════════════════╝
""")

if total_ke_ke == 0:
    print("  OUTCOME 1: GMS holds at undirected level.")
    print("  Grammar is visible at the coarsest level of the mod-8 hexagram formula.")
elif directed_violations == 0:
    print("  OUTCOME 2: GMS fails undirected, holds directed.")
    print("  The mod-6 体 assignment acts as grammatical filter;")
    print("  the moving line is the bridge between Z₈ and Q₃.")
else:
    print("  OUTCOME 3: GMS fails at both levels.")
    print("  Grammar does not survive the passage from Q₃ to Z₈ at hexagram level.")
    if directed_violations < total_ke_ke:
        print(f"  (But moving line reduces violations: {total_ke_ke} → {directed_violations})")

print(f"\n  Transition structure:")
print(f"    Total consecutive pairs: {total_pairs}")
print(f"    克→克 (undirected): {total_ke_ke} ({total_ke_ke/total_pairs*100:.1f}%)")
print(f"    克→生 (valve):      {ke_sheng} ({ke_sheng/total_pairs*100:.1f}%)")
print(f"    生→克:              {sheng_ke} ({sheng_ke/total_pairs*100:.1f}%)")

print("\n" + "=" * 100)
print("DONE")
print("=" * 100)
