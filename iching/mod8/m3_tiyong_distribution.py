#!/usr/bin/env python3
"""Probe M3: Per-hour 體用 五行 distribution in 梅花易數 date formula.

Date formula (verified in probe_8a):
  upper = (Y+M+D) mod 8        → 先天 position (0→8)
  lower = (Y+M+D+H) mod 8      → 先天 position (0→8)
  moving_line = (Y+M+D+H) mod 6 → line number (0→6)

Key: lower_raw = (upper_raw + H) mod 8, so hour determines cyclic shift S_h.
"""

from collections import Counter, defaultdict

# ─── Definitions (from m1) ───────────────────────────────────────────────

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

# Generation cycle: Metal(0)→Water(1)→Wood(2)→Fire(3)→Earth(4)→Metal(0)
# a 生 b iff (b-a) mod 5 == 1
# a 克 b iff (b-a) mod 5 == 2

def wuxing_type(a, b):
    """Undirected 五行 relation: 比和/生/克."""
    d = abs(a - b); d = min(d, 5 - d)
    return {0: "比和", 1: "生", 2: "克"}[d]

def directed_rel(ti_wx, yong_wx):
    """Directed relation from 体's perspective.
    diff = (用-体) mod 5:
      0 → 比和, 1 → 体生用(drain), 2 → 体克用(dominate),
      3 → 克体(attacked), 4 → 生体(nourished)
    """
    return {0: "比和", 1: "体生用", 2: "体克用", 3: "克体", 4: "生体"}[(yong_wx - ti_wx) % 5]

def raw_to_pos(r):
    """Mod-8 raw value (0-7) to 先天 position (1-8). 0 → 8."""
    return 8 if r == 0 else r

# 地支 hours: number → name
DIZHI = [
    (1, "子"), (2, "丑"), (3, "寅"), (4, "卯"), (5, "辰"), (6, "巳"),
    (7, "午"), (8, "未"), (9, "申"), (10, "酉"), (11, "戌"), (12, "亥"),
]

# Hour → shift mapping
SHIFT_HOURS = defaultdict(list)
for h_num, h_name in DIZHI:
    SHIFT_HOURS[h_num % 8].append((h_num, h_name))

# ═══════════════════════════════════════════════════════════════════════════
# 1. PER-SHIFT 體用 DISTRIBUTION
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 95)
print("1. PER-SHIFT 體用 DISTRIBUTION")
print("=" * 95)
print("For each shift h ∈ {0..7}: 8 (upper,lower) pairs where lower = S_h(upper) on 先天 cycle.")

shift_data = {}  # h → [(up, lp, uw, lw, utype), ...]

for h in range(8):
    pairs = []
    for u in range(8):
        l = (u + h) % 8
        up, lp = raw_to_pos(u), raw_to_pos(l)
        uw, lw = WUXING_MAP[VEC[up]], WUXING_MAP[VEC[lp]]
        pairs.append((up, lp, uw, lw, wuxing_type(uw, lw)))
    shift_data[h] = pairs

for h in range(8):
    pairs = shift_data[h]
    counts = Counter(p[4] for p in pairs)

    print(f"\n  Shift h={h}:")
    print(f"  {'Upper':>8} {'Lower':>8} {'U-WX':>7} {'L-WX':>7} {'Type':>4}  {'If U=体':>8}  {'If L=体':>8}")
    print(f"  " + "─" * 70)

    for up, lp, uw, lw, ut in pairs:
        dr_uti = directed_rel(uw, lw)  # upper=体, lower=用
        dr_lti = directed_rel(lw, uw)  # lower=体, upper=用
        print(f"  {NAME_BY_POS[up]:>4}({up}) {NAME_BY_POS[lp]:>4}({lp})"
              f" {Z5_NAMES[uw]:>7} {Z5_NAMES[lw]:>7} {ut:>4}"
              f"  {dr_uti:>8}  {dr_lti:>8}")

    print(f"  Counts: 比和={counts.get('比和',0)}, 生={counts.get('生',0)}, 克={counts.get('克',0)}")

# Summary table
print(f"\n  ╔═══════════════════════════════════════╗")
print(f"  ║       SHIFT SUMMARY TABLE             ║")
print(f"  ╠═══════╦══════╦══════╦══════╦══════════╣")
print(f"  ║ Shift ║  比和 ║   生  ║   克  ║ 克 frac  ║")
print(f"  ╠═══════╬══════╬══════╬══════╬══════════╣")
for h in range(8):
    c = Counter(p[4] for p in shift_data[h])
    bh, sh, kh = c.get('比和', 0), c.get('生', 0), c.get('克', 0)
    print(f"  ║   {h}   ║  {bh:>2}  ║  {sh:>2}  ║  {kh:>2}  ║  {kh/8*100:>4.1f}%  ║")
print(f"  ╚═══════╩══════╩══════╩══════╩══════════╝")

# ═══════════════════════════════════════════════════════════════════════════
# 2. HOUR → SHIFT MAPPING
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 95)
print("2. HOUR → SHIFT MAPPING")
print("=" * 95)
print("12 地支 hours map to shifts via H mod 8:")

print(f"\n  {'Shift':>5} {'Weight':>6} {'Hours (地支)':>40}")
print(f"  " + "─" * 55)
for h in range(8):
    hours = SHIFT_HOURS[h]
    hour_str = ", ".join(f"{name}(H={num})" for num, name in hours)
    print(f"  {h:>5} {len(hours):>6} {hour_str}")

print(f"\n  Doubly-represented: shifts 1,2,3,4 (hours wrap: H and H+8)")
print(f"  Singly-represented: shifts 0,5,6,7")
print(f"  Weight distribution: [1, 2, 2, 2, 2, 1, 1, 1] (total=12)")

# ═══════════════════════════════════════════════════════════════════════════
# 3. ERGODIC AVERAGE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 95)
print("3. ERGODIC AVERAGE (all uppers × all hours equally likely)")
print("=" * 95)

# Weighted by hour count per shift
total_counts = Counter()
for h in range(8):
    w = len(SHIFT_HOURS[h])
    for _, _, _, _, ut in shift_data[h]:
        total_counts[ut] += w

total = sum(total_counts.values())  # should be 96
print(f"\n  Total (upper_raw, hour) combinations: {total} (= 8 uppers × 12 hours)")
print(f"\n  ACTUAL distribution:")
for t in ["比和", "生", "克"]:
    v = total_counts[t]
    print(f"    {t}: {v:>3} / {total} = {v/total*100:.2f}%")

# Null: uniform random ORDERED pairs (upper, lower independent)
print(f"\n  NULL expectation (independent uniform ordered pairs, 8×8=64):")
null_counts = Counter()
for u in range(8):
    for l in range(8):
        uw = WUXING_MAP[VEC[raw_to_pos(u)]]
        lw = WUXING_MAP[VEC[raw_to_pos(l)]]
        null_counts[wuxing_type(uw, lw)] += 1

null_total = sum(null_counts.values())
for t in ["比和", "生", "克"]:
    v = null_counts[t]
    print(f"    {t}: {v:>3} / {null_total} = {v/null_total*100:.2f}%")

print(f"\n  DEVIATION from null:")
for t in ["比和", "生", "克"]:
    actual_pct = total_counts[t] / total * 100
    null_pct = null_counts[t] / null_total * 100
    print(f"    {t}: {actual_pct:.2f}% vs null {null_pct:.2f}%  (Δ = {actual_pct - null_pct:+.2f}%)")

# Also show unweighted (uniform over shifts)
print(f"\n  UNWEIGHTED average (uniform over 8 shifts, ignoring hour multiplicity):")
uw_counts = Counter()
for h in range(8):
    for _, _, _, _, ut in shift_data[h]:
        uw_counts[ut] += 1

uw_total = sum(uw_counts.values())  # 64
for t in ["比和", "生", "克"]:
    v = uw_counts[t]
    print(f"    {t}: {v:>3} / {uw_total} = {v/uw_total*100:.2f}%")

# ═══════════════════════════════════════════════════════════════════════════
# 4. SPECIAL STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 95)
print("4. SPECIAL STRUCTURE")
print("=" * 95)

# 克-enrichment analysis
print(f"\n  4a. 克-ENRICHMENT BY SHIFT:")
ke_per_shift = {}
for h in range(8):
    ke_per_shift[h] = Counter(p[4] for p in shift_data[h]).get('克', 0)

avg_ke = sum(ke_per_shift.values()) / 8
print(f"  Average 克 per shift: {avg_ke:.1f} / 8 = {avg_ke/8*100:.1f}%")

for h in range(8):
    ke = ke_per_shift[h]
    if ke > avg_ke:
        label = "ENRICHED"
    elif ke < avg_ke:
        label = "DEPLETED"
    else:
        label = "average"
    print(f"    Shift {h}: 克 = {ke}/8 ({ke/8*100:.0f}%)  {label}")

ke_free = [h for h in range(8) if ke_per_shift[h] == 0]
ke_all  = [h for h in range(8) if ke_per_shift[h] == 8]
print(f"\n  克-free shifts: {ke_free if ke_free else 'NONE'}")
print(f"  All-克 shifts:  {ke_all if ke_all else 'NONE'}")

# 比和-enrichment
print(f"\n  4b. 比和-ENRICHMENT BY SHIFT:")
for h in range(8):
    bh = Counter(p[4] for p in shift_data[h]).get('比和', 0)
    print(f"    Shift {h}: 比和 = {bh}/8 ({bh/8*100:.0f}%)")

# S_4 analysis
print(f"\n  4c. S_4 ANALYSIS:")
print(f"  Captain hypothesis: 'S_4 maps each trigram to its complement'")
print(f"  Testing S_4 against F₂³ complement (XOR with 111):")
s4_is_comp = True
for u in range(8):
    up = raw_to_pos(u)
    lp = raw_to_pos((u + 4) % 8)
    uv, lv = VEC[up], VEC[lp]
    comp_uv = tuple(1 - b for b in uv)
    match = "✓" if lv == comp_uv else "✗"
    if lv != comp_uv:
        s4_is_comp = False
    print(f"    {NAME_BY_POS[up]}({uv}) →S₄→ {NAME_BY_POS[lp]}({lv})"
          f"  complement={comp_uv}({NAMES[comp_uv]})  {match}")

print(f"\n  RESULT: S_4 IS complement map? {s4_is_comp}")
if not s4_is_comp:
    print(f"  Complement = reversal p↦(9-p), NOT a cyclic shift on 先天 positions.")
    print(f"  Complement pairs: ", end="")
    pairs = []
    for u in range(4):
        up = raw_to_pos(u)
        cv = tuple(1-b for b in VEC[up])
        cp = POS[cv]
        pairs.append(f"{NAME_BY_POS[up]}({up})↔{NAME_BY_POS[cp]}({cp})")
    print(", ".join(pairs))

# What does S_4 actually do in terms of 五行?
print(f"\n  S_4 五行 mapping (what S_4 actually does):")
s4_wx = {}
for u in range(8):
    up = raw_to_pos(u)
    lp = raw_to_pos((u + 4) % 8)
    s4_wx[Z5_NAMES[WUXING_MAP[VEC[up]]]] = Z5_NAMES[WUXING_MAP[VEC[lp]]]
    print(f"    {NAME_BY_POS[up]}({Z5_NAMES[WUXING_MAP[VEC[up]]]:>5})"
          f" → {NAME_BY_POS[lp]}({Z5_NAMES[WUXING_MAP[VEC[lp]]]:>5})")

# ═══════════════════════════════════════════════════════════════════════════
# 5. MOVING LINE INTERACTION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 95)
print("5. MOVING LINE INTERACTION")
print("=" * 95)
print("moving_line = (Y+M+D+H) mod 6 (0→6). Lines 1-3: upper=体. Lines 4-6: lower=体.")
print("Key: S = Y+M+D+H. Given S mod 8 = lower_raw, S mod 6 is constrained.")

# Structural constraint
print(f"\n  5a. STRUCTURAL CONSTRAINT:")
print(f"  S mod 8 = r  ⟹  S mod 6 ∈ {{r%6, (r+2)%6, (r+4)%6}}  (3 values, equally likely)")
print(f"\n  {'lower_raw':>10} {'parity':>6} {'S mod 6':>12} {'lines':>10} {'P(U=体)':>8}")
print(f"  " + "─" * 52)
for r in range(8):
    mod6_vals = sorted(set((r + 2 * k) % 6 for k in range(3)))
    lines = sorted(6 if v == 0 else v for v in mod6_vals)
    upper_ti = sum(1 for l in lines if l <= 3)
    parity = "even" if r % 2 == 0 else "odd"
    print(f"  {r:>10} {parity:>6} {str(mod6_vals):>12} {str(lines):>10} {upper_ti}/3={upper_ti/3:.3f}")

print(f"\n  PATTERN:")
print(f"    even lower_raw → lines {{2,4,6}} → P(upper=体) = 1/3, P(lower=体) = 2/3")
print(f"    odd  lower_raw → lines {{1,3,5}} → P(upper=体) = 2/3, P(lower=体) = 1/3")
print(f"    lower_raw parity = (upper_raw + shift) mod 2")
print(f"    ⟹ For ANY shift, 4 uppers give even lower_raw, 4 give odd → avg P(U=体) = 1/2")

# 5b. Per-shift directed distribution
print(f"\n  5b. PER-SHIFT DIRECTED DISTRIBUTION (weighted by P(体) from moving line):")
print(f"  {'Shift':>5} {'比和':>6} {'生体':>6} {'体生用':>6} {'体克用':>6} {'克体':>6} │ {'Fav':>6} {'Unfav':>6}")
print(f"  " + "─" * 63)

all_shift_directed = {}
for h in range(8):
    dc = Counter()
    for u in range(8):
        lr = (u + h) % 8
        up, lp = raw_to_pos(u), raw_to_pos(lr)
        uw, lw = WUXING_MAP[VEC[up]], WUXING_MAP[VEC[lp]]

        p_upper_ti = 1 / 3 if lr % 2 == 0 else 2 / 3

        dc[directed_rel(uw, lw)] += p_upper_ti       # upper=体
        dc[directed_rel(lw, uw)] += (1 - p_upper_ti)  # lower=体

    all_shift_directed[h] = dc
    fav = dc.get("比和", 0) + dc.get("生体", 0) + dc.get("体克用", 0)
    unfav = dc.get("体生用", 0) + dc.get("克体", 0)
    total_h = sum(dc.values())  # should be 8

    types = ["比和", "生体", "体生用", "体克用", "克体"]
    vals = " ".join(f"{dc.get(t,0):>6.2f}" for t in types)
    print(f"  {h:>5} {vals} │ {fav:>6.2f} {unfav:>6.2f}")

# 5c. Ergodic directed average
print(f"\n  5c. ERGODIC DIRECTED AVERAGE (hour-weighted):")
erg_dc = Counter()
for h in range(8):
    w = len(SHIFT_HOURS[h])
    for t, v in all_shift_directed[h].items():
        erg_dc[t] += w * v

erg_total = sum(erg_dc.values())  # should be 96
print(f"  Total weighted: {erg_total:.1f}")
for t in ["比和", "生体", "体生用", "体克用", "克体"]:
    v = erg_dc.get(t, 0)
    print(f"    {t:>6}: {v:>8.2f} / {erg_total:.0f} = {v/erg_total*100:.2f}%")

fav = erg_dc.get("比和", 0) + erg_dc.get("生体", 0) + erg_dc.get("体克用", 0)
unfav = erg_dc.get("体生用", 0) + erg_dc.get("克体", 0)
print(f"\n  FAVORABILITY:")
print(f"    Favorable (比和 + 生体 + 体克用):  {fav:>8.2f} / {erg_total:.0f} = {fav/erg_total*100:.2f}%")
print(f"    Unfavorable (体生用 + 克体):       {unfav:>8.2f} / {erg_total:.0f} = {unfav/erg_total*100:.2f}%")

# 5d. Null directed expectation
print(f"\n  5d. NULL DIRECTED EXPECTATION (independent pairs, P(U=体)=1/2):")
null_dc = Counter()
for u in range(8):
    for l in range(8):
        uw = WUXING_MAP[VEC[raw_to_pos(u)]]
        lw = WUXING_MAP[VEC[raw_to_pos(l)]]
        null_dc[directed_rel(uw, lw)] += 0.5  # upper=体
        null_dc[directed_rel(lw, uw)] += 0.5  # lower=体

null_d_total = sum(null_dc.values())
for t in ["比和", "生体", "体生用", "体克用", "克体"]:
    v = null_dc.get(t, 0)
    print(f"    {t:>6}: {v:>8.2f} / {null_d_total:.0f} = {v/null_d_total*100:.2f}%")

null_fav = null_dc.get("比和", 0) + null_dc.get("生体", 0) + null_dc.get("体克用", 0)
null_unfav = null_dc.get("体生用", 0) + null_dc.get("克体", 0)
print(f"    Favorable: {null_fav:.2f}/{null_d_total:.0f} = {null_fav/null_d_total*100:.2f}%")
print(f"    Unfavorable: {null_unfav:.2f}/{null_d_total:.0f} = {null_unfav/null_d_total*100:.2f}%")

print(f"\n  DEVIATION from null:")
for t in ["比和", "生体", "体生用", "体克用", "克体"]:
    a = erg_dc.get(t, 0) / erg_total * 100
    n = null_dc.get(t, 0) / null_d_total * 100
    print(f"    {t:>6}: {a:.2f}% vs null {n:.2f}%  (Δ = {a-n:+.2f}%)")

a_fav = fav / erg_total * 100
n_fav = null_fav / null_d_total * 100
print(f"    {'Fav':>6}: {a_fav:.2f}% vs null {n_fav:.2f}%  (Δ = {a_fav-n_fav:+.2f}%)")

print("\n" + "=" * 95)
print("DONE")
print("=" * 95)
