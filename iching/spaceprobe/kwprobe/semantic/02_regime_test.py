"""
02_regime_test.py — Corridor-free zone algebra×semantics analysis

Tests whether the corridor-free zone (T17–T26) shows any correlation
between algebraic and semantic features, and compares against the
corridor-rich zone.

Also: preserving bridge analysis and non-preserving 互 smoothness.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter
from pathlib import Path

from sequence import KING_WEN
from cycle_algebra import (
    lower_trigram, upper_trigram, hugua,
    hamming6, hamming3,
)

# ═══════════════════════════════════════════════════════════════════════════
# Rebuild transitions (reusing 01_unified_table.py infrastructure)
# ═══════════════════════════════════════════════════════════════════════════

KERNEL_NAMES = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI',
}
H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}

TRIGRAM_SHORT = {
    0b000: "Earth", 0b001: "Thndr", 0b010: "Water", 0b011: "Lake",
    0b100: "Mtn",   0b101: "Fire",  0b110: "Wind",  0b111: "Heaven",
}

SEMANTIC = {
    1:  {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    2:  {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    3:  {'logic': 'Causal',      'conf': 'Direct',  'dir': '⇀'},
    4:  {'logic': 'Causal',      'conf': 'Implied', 'dir': '⇀'},
    5:  {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    6:  {'logic': 'Cyclical',    'conf': 'Direct',  'dir': '⇀'},
    7:  {'logic': 'Contrastive', 'conf': 'Direct',  'dir': '→'},
    8:  {'logic': 'Causal',      'conf': 'Implied', 'dir': '⇀'},
    9:  {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    10: {'logic': 'Causal',      'conf': 'Implied', 'dir': '⇀'},
    11: {'logic': 'Cyclical',    'conf': 'Direct',  'dir': '→'},
    12: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    13: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    14: {'logic': 'Cyclical',    'conf': 'Implied', 'dir': '⇀'},
    15: {'logic': 'Temporal',    'conf': 'Direct',  'dir': '→'},
    16: {'logic': 'Cyclical',    'conf': 'Implied', 'dir': '⇀'},
    17: {'logic': 'Cyclical',    'conf': 'Implied', 'dir': '⇀'},
    18: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    19: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    20: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    21: {'logic': 'Cyclical',    'conf': 'Direct',  'dir': '→'},
    22: {'logic': 'Causal',      'conf': 'Direct',  'dir': '⇀'},
    23: {'logic': 'Cyclical',    'conf': 'Direct',  'dir': '→'},
    24: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    25: {'logic': 'Analogical',  'conf': 'Direct',  'dir': '⇀'},
    26: {'logic': 'Cyclical',    'conf': 'Implied', 'dir': '⇀'},
    27: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    28: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    29: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    30: {'logic': 'Causal',      'conf': 'Direct',  'dir': '→'},
    31: {'logic': 'Causal',      'conf': 'Implied', 'dir': '⇀'},
}

# Xugua reasons for preserving bridges (compact paraphrase)
PRESERVING_REASONS = {
    3:  "Contention → masses rise → Army (conflict escalates to mobilization)",
    6:  "Stagnation cannot last → Fellowship (exhaustion-reversal)",
    11: "Adornment carried to limit → exhausted → Splitting Apart",
    12: "Return to root → no falsehood → Innocence (purification)",
    13: "Accumulation → nourishment possible → Nourishment",
    18: "Injured abroad → return to household → Family",
    26: "Stillness cannot last → gradual advance → Development",
    27: "Found a home → become great → Abundance (settlement→prosperity)",
    30: "Limitation → trust → Inner Truth (boundaries create faithfulness)",
}


def get_basin(h):
    b2, b3 = (h >> 2) & 1, (h >> 3) & 1
    if b2 == 0 and b3 == 0: return 'Kun'
    if b2 == 1 and b3 == 1: return 'Qian'
    return 'KanLi'


def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])


kw_hex = []
kw_names = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    kw_hex.append(sum(b[j] << j for j in range(6)))
    kw_names.append(KING_WEN[i][1])

transitions = []
for t in range(31):
    exit_idx, entry_idx = 2 * t + 1, 2 * t + 2
    h1, h2 = kw_hex[exit_idx], kw_hex[entry_idx]
    kernel = mirror_kernel(h1 ^ h2)
    lo1, up1 = lower_trigram(h1), upper_trigram(h1)
    lo2, up2 = lower_trigram(h2), upper_trigram(h2)
    lo_d, up_d = hamming3(lo1, lo2), hamming3(up1, up2)

    if lo_d == 0:
        preserving = f"Lo:{TRIGRAM_SHORT[lo1]}"
        pres_pos = 'lower'
    elif up_d == 0:
        preserving = f"Up:{TRIGRAM_SHORT[up1]}"
        pres_pos = 'upper'
    else:
        preserving = None
        pres_pos = None

    t_num = t + 1
    sem = SEMANTIC[t_num]
    transitions.append({
        'T': t_num,
        'exit_hex': kw_names[exit_idx],
        'entry_hex': kw_names[entry_idx],
        'hex_d': hamming6(h1, h2),
        'lo_d': lo_d, 'up_d': up_d,
        'basin_exit': get_basin(h1), 'basin_entry': get_basin(h2),
        'basin_cross': get_basin(h1) != get_basin(h2),
        'hu_d': hamming6(hugua(h1), hugua(h2)),
        'k_name': KERNEL_NAMES[kernel],
        'h_kernel': kernel in H_KERNELS,
        'preserving': preserving,
        'pres_pos': pres_pos,
        'logic': sem['logic'],
        'conf': sem['conf'],
        'dir': sem['dir'],
    })


# ═══════════════════════════════════════════════════════════════════════════
# Zone definitions
# ═══════════════════════════════════════════════════════════════════════════

FREE_ZONE = set(range(17, 27))   # T17–T26 (10 transitions)
RICH_ZONE = set(range(1, 17)) | set(range(27, 32))  # T1–T16 + T27–T31 (21)

free = [tr for tr in transitions if tr['T'] in FREE_ZONE]
rich = [tr for tr in transitions if tr['T'] in RICH_ZONE]


# ═══════════════════════════════════════════════════════════════════════════
# Utilities
# ═══════════════════════════════════════════════════════════════════════════

def fisher_2x2(a, b, c, d):
    """Fisher exact test for 2x2 table [[a,b],[c,d]].
    Returns two-sided p-value. Uses scipy if available, else manual."""
    try:
        from scipy.stats import fisher_exact
        _, p = fisher_exact([[a, b], [c, d]])
        return p
    except ImportError:
        from math import comb, factorial
        n = a + b + c + d
        r1, r2, c1, c2 = a + b, c + d, a + c, b + d
        def hyper_p(x):
            return comb(r1, x) * comb(r2, c1 - x) / comb(n, c1)
        p_obs = hyper_p(a)
        p = sum(hyper_p(x) for x in range(max(0, c1 - r2), min(r1, c1) + 1)
                if hyper_p(x) <= p_obs + 1e-12)
        return p


def xtab_2x2(data, key1, val1_true, key2, val2_true):
    """Build a 2×2 table: key1∈{true,false} × key2∈{true,false}."""
    a = sum(1 for d in data if d[key1] == val1_true and d[key2] == val2_true)
    b = sum(1 for d in data if d[key1] == val1_true and d[key2] != val2_true)
    c = sum(1 for d in data if d[key1] != val1_true and d[key2] == val2_true)
    d_ = sum(1 for d in data if d[key1] != val1_true and d[key2] != val2_true)
    return a, b, c, d_


def print_2x2(label, r1_name, r2_name, c1_name, c2_name, a, b, c, d):
    """Print a 2×2 table with Fisher p-value."""
    p = fisher_2x2(a, b, c, d)
    n = a + b + c + d
    print(f"\n  {label}  (n={n}, Fisher p={p:.3f})")
    print(f"  {'':>15} {c1_name:>8} {c2_name:>8}  Total")
    print(f"  {'─'*45}")
    print(f"  {r1_name:>15} {a:>8} {b:>8}  {a+b:>5}")
    print(f"  {r2_name:>15} {c:>8} {d:>8}  {c+d:>5}")
    print(f"  {'Total':>15} {a+c:>8} {b+d:>8}  {n:>5}")
    return p


def md_2x2(w, label, r1_name, r2_name, c1_name, c2_name, a, b, c, d):
    """Write a 2×2 table in markdown."""
    p = fisher_2x2(a, b, c, d)
    n = a + b + c + d
    w(f"**{label}** (n={n}, Fisher p={p:.3f})\n")
    w(f"| | {c1_name} | {c2_name} | Total |")
    w(f"|---|:---:|:---:|:---:|")
    w(f"| **{r1_name}** | {a} | {b} | {a+b} |")
    w(f"| **{r2_name}** | {c} | {d} | {c+d} |")
    w(f"| **Total** | {a+c} | {b+d} | {n} |")
    w("")
    return p


# ═══════════════════════════════════════════════════════════════════════════
# TASK 1: Cross-tabulations for corridor-free zone (T17–T26)
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 80)
print("TASK 1: CORRIDOR-FREE ZONE CROSS-TABS (T17–T26, n=10)")
print("=" * 80)

# Filter to Causal+Cyclical only for H-kernel × Logic
free_cc = [d for d in free if d['logic'] in ('Causal', 'Cyclical')]
rich_cc = [d for d in rich if d['logic'] in ('Causal', 'Cyclical')]

# 1a. H-kernel × Logic (Causal vs Cyclical)
a, b, c, d_ = xtab_2x2(free_cc, 'h_kernel', True, 'logic', 'Cyclical')
p1a = print_2x2("FREE: H-kernel × Logic (Causal/Cyclical only)",
                 "H-kernel", "non-H", "Cyclical", "Causal", a, b, c, d_)

# Note non-Causal/Cyclical types in free zone
other_free = [d for d in free if d['logic'] not in ('Causal', 'Cyclical')]
if other_free:
    excl = ', '.join(f"T{d['T']}={d['logic']}" for d in other_free)
    print(f"\n  (Excluded from Causal/Cyclical table: {excl})")

# 1b. 互 distance × Confidence
# Bin: hu_d ≤ 2 = smooth, > 2 = rough
for d in free:
    d['hu_smooth'] = d['hu_d'] <= 2
a, b, c, d_ = xtab_2x2(free, 'hu_smooth', True, 'conf', 'Implied')
p1b = print_2x2("FREE: 互 smooth (≤2) × Confidence",
                 "互≤2", "互>2", "Implied", "Direct", a, b, c, d_)

# 1c. Basin-crossing × Directionality
a, b, c, d_ = xtab_2x2(free, 'basin_cross', True, 'dir', '⇀')
p1c = print_2x2("FREE: Basin-crossing × Directionality",
                 "Crossing", "Same-basin", "⇀ weak", "→ strong", a, b, c, d_)


# ═══════════════════════════════════════════════════════════════════════════
# TASK 2: Compare free vs rich zone distributions
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("TASK 2: FREE vs RICH ZONE COMPARISON")
print("=" * 80)

# Mark smooth on all
for d in transitions:
    d['hu_smooth'] = d['hu_d'] <= 2

# 2a. H-kernel × Logic (Causal/Cyclical)
print("\n  ── H-kernel × Logic (Causal vs Cyclical) ──")
a, b, c, d_ = xtab_2x2(rich_cc, 'h_kernel', True, 'logic', 'Cyclical')
p2a_r = print_2x2("RICH: H-kernel × Logic",
                   "H-kernel", "non-H", "Cyclical", "Causal", a, b, c, d_)
a, b, c, d_ = xtab_2x2(free_cc, 'h_kernel', True, 'logic', 'Cyclical')
p2a_f = print_2x2("FREE: H-kernel × Logic",
                   "H-kernel", "non-H", "Cyclical", "Causal", a, b, c, d_)

# 2b. 互 smooth × Confidence
print("\n  ── 互 smooth (≤2) × Confidence ──")
a, b, c, d_ = xtab_2x2(rich, 'hu_smooth', True, 'conf', 'Implied')
p2b_r = print_2x2("RICH: 互 smooth × Confidence",
                   "互≤2", "互>2", "Implied", "Direct", a, b, c, d_)
a, b, c, d_ = xtab_2x2(free, 'hu_smooth', True, 'conf', 'Implied')
p2b_f = print_2x2("FREE: 互 smooth × Confidence",
                   "互≤2", "互>2", "Implied", "Direct", a, b, c, d_)

# 2c. Basin-crossing × Directionality
print("\n  ── Basin-crossing × Directionality ──")
a, b, c, d_ = xtab_2x2(rich, 'basin_cross', True, 'dir', '⇀')
p2c_r = print_2x2("RICH: Basin-crossing × Directionality",
                   "Crossing", "Same-basin", "⇀ weak", "→ strong", a, b, c, d_)
a, b, c, d_ = xtab_2x2(free, 'basin_cross', True, 'dir', '⇀')
p2c_f = print_2x2("FREE: Basin-crossing × Directionality",
                   "Crossing", "Same-basin", "⇀ weak", "→ strong", a, b, c, d_)

# Summary table
print("\n  ── Summary: Fisher p-values by zone ──")
print(f"  {'Cross-tab':>35} {'Rich p':>8} {'Free p':>8}")
print(f"  {'─'*55}")
print(f"  {'H-kernel × Logic':>35} {p2a_r:>8.3f} {p2a_f:>8.3f}")
print(f"  {'互 smooth × Confidence':>35} {p2b_r:>8.3f} {p2b_f:>8.3f}")
print(f"  {'Basin-cross × Direction':>35} {p2c_r:>8.3f} {p2c_f:>8.3f}")


# ═══════════════════════════════════════════════════════════════════════════
# TASK 3: Preserving bridge analysis
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("TASK 3: PRESERVING BRIDGE ANALYSIS (9 bridges)")
print("=" * 80)

pres_bridges = [tr for tr in transitions if tr['preserving'] is not None]

print(f"\n  {'T':>2} {'Bridge':>22} {'Preserved':>12} {'Pos':>5} "
      f"{'Logic':>11} {'Conf':>7} {'Xugua Reason'}")
print(f"  {'─'*110}")

for tr in pres_bridges:
    bridge = f"{tr['exit_hex']}→{tr['entry_hex']}"
    reason = PRESERVING_REASONS.get(tr['T'], '?')
    print(f"  {tr['T']:>2} {bridge:>22} {tr['preserving']:>12} {tr['pres_pos']:>5} "
          f"{tr['logic']:>11} {tr['conf']:>7}  {reason}")

# Count: position × logic
lo_causal = sum(1 for tr in pres_bridges if tr['pres_pos'] == 'lower' and tr['logic'] == 'Causal')
lo_cyclical = sum(1 for tr in pres_bridges if tr['pres_pos'] == 'lower' and tr['logic'] == 'Cyclical')
up_causal = sum(1 for tr in pres_bridges if tr['pres_pos'] == 'upper' and tr['logic'] == 'Causal')
up_cyclical = sum(1 for tr in pres_bridges if tr['pres_pos'] == 'upper' and tr['logic'] == 'Cyclical')

print(f"\n  Position × Logic:")
print(f"  {'':>10} {'Causal':>8} {'Cyclical':>8}  Total")
print(f"  {'─'*35}")
print(f"  {'Lower':>10} {lo_causal:>8} {lo_cyclical:>8}  {lo_causal+lo_cyclical:>5}")
print(f"  {'Upper':>10} {up_causal:>8} {up_cyclical:>8}  {up_causal+up_cyclical:>5}")
print(f"  {'Total':>10} {lo_causal+up_causal:>8} {lo_cyclical+up_cyclical:>8}  {len(pres_bridges):>5}")

p3 = fisher_2x2(lo_causal, lo_cyclical, up_causal, up_cyclical)
print(f"\n  Fisher p = {p3:.3f}")
print(f"  Lower preserving: {lo_causal}/{lo_causal+lo_cyclical} Causal "
      f"({100*lo_causal/(lo_causal+lo_cyclical):.0f}%)")
print(f"  Upper preserving: {up_cyclical}/{up_causal+up_cyclical} Cyclical "
      f"({100*up_cyclical/(up_causal+up_cyclical):.0f}%)")


# ═══════════════════════════════════════════════════════════════════════════
# TASK 4: Non-preserving bridges — 互 smoothness × Confidence
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("TASK 4: NON-PRESERVING BRIDGES — 互 SMOOTHNESS × CONFIDENCE (22 bridges)")
print("=" * 80)

non_pres = [tr for tr in transitions if tr['preserving'] is None]
print(f"\n  Total non-preserving: {len(non_pres)}")

smooth = [tr for tr in non_pres if tr['hu_d'] <= 2]
rough = [tr for tr in non_pres if tr['hu_d'] > 2]
print(f"  互d ≤ 2 (smooth): {len(smooth)}")
print(f"  互d > 2 (rough):  {len(rough)}")

# Detail
print(f"\n  {'T':>2} {'Bridge':>22} {'互d':>3} {'Smooth':>6} {'Conf':>7} {'Logic':>11}")
print(f"  {'─'*65}")
for tr in sorted(non_pres, key=lambda x: x['hu_d']):
    bridge = f"{tr['exit_hex']}→{tr['entry_hex']}"
    sm = '≤2' if tr['hu_d'] <= 2 else '>2'
    print(f"  {tr['T']:>2} {bridge:>22} {tr['hu_d']:>3} {sm:>6} {tr['conf']:>7} {tr['logic']:>11}")

# 2×2: smooth × confidence
sm_implied = sum(1 for tr in smooth if tr['conf'] == 'Implied')
sm_direct = sum(1 for tr in smooth if tr['conf'] == 'Direct')
ro_implied = sum(1 for tr in rough if tr['conf'] == 'Implied')
ro_direct = sum(1 for tr in rough if tr['conf'] == 'Direct')

p4 = print_2x2("Non-preserving: 互 smooth × Confidence",
                "互≤2 (smooth)", "互>2 (rough)", "Implied", "Direct",
                sm_implied, sm_direct, ro_implied, ro_direct)


# ═══════════════════════════════════════════════════════════════════════════
# Write markdown
# ═══════════════════════════════════════════════════════════════════════════

L = []
w = L.append

w("# Regime Test: Algebra × Semantics in Corridor-Free vs Rich Zones\n")

# ── Task 1 ──
w("## 1. Corridor-Free Zone Cross-Tabs (T17–T26, n=10)\n")
w("The corridor-free zone spans pairs P17–P26 — the longest stretch without")
w("corridor structure. These 10 transitions are where pair ordering is least")
w("constrained by trigram persistence.\n")

# List the 10 transitions
w("| T# | Bridge | H? | 互d | ×? | Logic | Conf | Dir |")
w("|:--:|--------|:--:|:---:|:--:|-------|------|:---:|")
for tr in free:
    hk = '**Y**' if tr['h_kernel'] else 'N'
    cross = '**Y**' if tr['basin_cross'] else 'N'
    logic = f"**{tr['logic']}**" if tr['logic'] != 'Causal' else tr['logic']
    w(f"| {tr['T']} | {tr['exit_hex']}→{tr['entry_hex']} | {hk} | {tr['hu_d']} "
      f"| {cross} | {logic} | {tr['conf']} | {tr['dir']} |")
w("")

# 1a
a, b, c, d_ = xtab_2x2(free_cc, 'h_kernel', True, 'logic', 'Cyclical')
md_2x2(w, "1a. H-kernel × Logic (Causal/Cyclical only, n=9)",
        "H-kernel", "non-H", "Cyclical", "Causal", a, b, c, d_)
if other_free:
    excl_md = ', '.join(f"T{d['T']}={d['logic']}" for d in other_free)
    w(f"*Excluded: {excl_md}*\n")

# 1b
a, b, c, d_ = xtab_2x2(free, 'hu_smooth', True, 'conf', 'Implied')
md_2x2(w, "1b. 互 smooth (≤2) × Confidence (n=10)",
        "互≤2", "互>2", "Implied", "Direct", a, b, c, d_)

# 1c
a, b, c, d_ = xtab_2x2(free, 'basin_cross', True, 'dir', '⇀')
md_2x2(w, "1c. Basin-crossing × Directionality (n=10)",
        "Crossing", "Same-basin", "⇀ weak", "→ strong", a, b, c, d_)


# ── Task 2 ──
w("## 2. Free Zone vs Rich Zone Comparison\n")
w("Corridor-rich zone: T1–T16 + T27–T31 (n=21)")
w("Corridor-free zone: T17–T26 (n=10)\n")

w("### 2a. H-kernel × Logic (Causal vs Cyclical)\n")

a, b, c, d_ = xtab_2x2(rich_cc, 'h_kernel', True, 'logic', 'Cyclical')
p_r = md_2x2(w, "RICH (n=19 after excluding Contrastive+Temporal)",
              "H-kernel", "non-H", "Cyclical", "Causal", a, b, c, d_)
a, b, c, d_ = xtab_2x2(free_cc, 'h_kernel', True, 'logic', 'Cyclical')
p_f = md_2x2(w, "FREE (n=9 after excluding Analogical)",
              "H-kernel", "non-H", "Cyclical", "Causal", a, b, c, d_)

w("### 2b. 互 smooth (≤2) × Confidence\n")
a, b, c, d_ = xtab_2x2(rich, 'hu_smooth', True, 'conf', 'Implied')
p_r = md_2x2(w, "RICH (n=21)", "互≤2", "互>2", "Implied", "Direct", a, b, c, d_)
a, b, c, d_ = xtab_2x2(free, 'hu_smooth', True, 'conf', 'Implied')
p_f = md_2x2(w, "FREE (n=10)", "互≤2", "互>2", "Implied", "Direct", a, b, c, d_)

w("### 2c. Basin-crossing × Directionality\n")
a, b, c, d_ = xtab_2x2(rich, 'basin_cross', True, 'dir', '⇀')
p_r = md_2x2(w, "RICH (n=21)", "Crossing", "Same-basin", "⇀ weak", "→ strong",
              a, b, c, d_)
a, b, c, d_ = xtab_2x2(free, 'basin_cross', True, 'dir', '⇀')
p_f = md_2x2(w, "FREE (n=10)", "Crossing", "Same-basin", "⇀ weak", "→ strong",
              a, b, c, d_)

# Summary
w("### Summary: Fisher p-values\n")
# Recompute all p-values for summary
tests = []
for label, data_set, n_label in [
    ("H-kern × Logic", rich_cc, "RICH"),
    ("H-kern × Logic", free_cc, "FREE"),
    ("互smooth × Conf", rich, "RICH"),
    ("互smooth × Conf", free, "FREE"),
    ("Basin× × Dir", rich, "RICH"),
    ("Basin× × Dir", free, "FREE"),
]:
    if "H-kern" in label:
        a, b, c, d_ = xtab_2x2(data_set, 'h_kernel', True, 'logic', 'Cyclical')
    elif "互smooth" in label:
        a, b, c, d_ = xtab_2x2(data_set, 'hu_smooth', True, 'conf', 'Implied')
    else:
        a, b, c, d_ = xtab_2x2(data_set, 'basin_cross', True, 'dir', '⇀')
    p = fisher_2x2(a, b, c, d_)
    tests.append((label, n_label, len(data_set), p))

w("| Cross-tab | Zone | n | Fisher p |")
w("|-----------|:----:|:-:|:--------:|")
for label, zone, n, p in tests:
    w(f"| {label} | {zone} | {n} | {p:.3f} |")
w("")

# Assessment
all_free_p = [p for _, z, _, p in tests if z == "FREE"]
all_rich_p = [p for _, z, _, p in tests if z == "RICH"]
w("**Assessment:** ", )
if all(p > 0.3 for p in all_free_p) and all(p > 0.3 for p in all_rich_p):
    w("No significant algebra-semantics correlations in either zone.")
    w("Both zones show essentially independent algebra and semantics.\n")
elif all(p > 0.3 for p in all_free_p):
    w("The corridor-free zone shows no significant algebra-semantics correlations.")
    w("The corridor-rich zone shows possible structure in at least one cross-tab.\n")
else:
    w("Mixed results — some cross-tabs show structure, others don't.\n")


# ── Task 3 ──
w("## 3. Preserving Bridge Analysis (9 bridges)\n")
w("Each preserving bridge maintains one trigram across the inter-pair boundary.")
w("The sage's hypothesis: **Causal → lower preserved, Cyclical → upper preserved.**\n")

w("| T# | Bridge | Preserved | Pos | Logic | Conf | Xugua Reason |")
w("|:--:|--------|-----------|:---:|-------|------|--------------|")
for tr in pres_bridges:
    bridge = f"{tr['exit_hex']}→{tr['entry_hex']}"
    reason = PRESERVING_REASONS.get(tr['T'], '?')
    logic = f"**{tr['logic']}**" if tr['logic'] == 'Cyclical' else tr['logic']
    w(f"| {tr['T']} | {bridge} | {tr['preserving']} | {tr['pres_pos']} "
      f"| {logic} | {tr['conf']} | {reason} |")
w("")

w("### Position × Logic cross-tab\n")
md_2x2(w, "Preserving position × Logic type (n=9)",
        "Lower", "Upper", "Causal", "Cyclical",
        lo_causal, lo_cyclical, up_causal, up_cyclical)

lo_tot = lo_causal + lo_cyclical
up_tot = up_causal + up_cyclical
w(f"- **Lower preserving:** {lo_causal}/{lo_tot} Causal ({100*lo_causal/lo_tot:.0f}%)")
w(f"- **Upper preserving:** {up_cyclical}/{up_tot} Cyclical ({100*up_cyclical/up_tot:.0f}%)")
w(f"- **Pattern direction:** Causal→lower {lo_causal}/{lo_causal+up_causal} "
  f"({100*lo_causal/(lo_causal+up_causal):.0f}%), "
  f"Cyclical→upper {up_cyclical}/{lo_cyclical+up_cyclical} "
  f"({100*up_cyclical/(lo_cyclical+up_cyclical):.0f}%)")
w("")

w("### Reading the pattern\n")
w("**Lower-preserved bridges** (trigram anchors the bottom):")
w("")
for tr in pres_bridges:
    if tr['pres_pos'] == 'lower':
        w(f"- T{tr['T']} {tr['preserving']}: {tr['logic']} — "
          f"{PRESERVING_REASONS[tr['T']]}")
w("")
w("**Upper-preserved bridges** (trigram anchors the top):")
w("")
for tr in pres_bridges:
    if tr['pres_pos'] == 'upper':
        w(f"- T{tr['T']} {tr['preserving']}: {tr['logic']} — "
          f"{PRESERVING_REASONS[tr['T']]}")
w("")


# ── Task 4 ──
w("## 4. Non-Preserving Bridges — 互 Smoothness × Confidence (22 bridges)\n")
w("For the 22 transitions where no trigram is preserved, does the hidden (互)")
w("transition smoothness correlate with the Xugua's narrative confidence?\n")

w(f"- **互d ≤ 2 (smooth hidden transition):** {len(smooth)}/22")
w(f"- **互d > 2 (rough hidden transition):** {len(rough)}/22\n")

md_2x2(w, "互 smoothness × Confidence (non-preserving only, n=22)",
        "互≤2 (smooth)", "互>2 (rough)", "Implied", "Direct",
        sm_implied, sm_direct, ro_implied, ro_direct)

# Detail by smoothness
w("### Detail: smooth hidden transitions (互d ≤ 2)\n")
w("| T# | Bridge | 互d | Conf | Logic |")
w("|:--:|--------|:---:|------|-------|")
for tr in sorted(smooth, key=lambda x: x['hu_d']):
    w(f"| {tr['T']} | {tr['exit_hex']}→{tr['entry_hex']} | {tr['hu_d']} "
      f"| {tr['conf']} | {tr['logic']} |")
w("")

w("### Detail: rough hidden transitions (互d > 2)\n")
w("| T# | Bridge | 互d | Conf | Logic |")
w("|:--:|--------|:---:|------|-------|")
for tr in sorted(rough, key=lambda x: x['hu_d']):
    w(f"| {tr['T']} | {tr['exit_hex']}→{tr['entry_hex']} | {tr['hu_d']} "
      f"| {tr['conf']} | {tr['logic']} |")
w("")

# Implied rate by smoothness
sm_imp_rate = sm_implied / len(smooth) if smooth else 0
ro_imp_rate = ro_implied / len(rough) if rough else 0
w(f"- Implied rate among smooth: {sm_implied}/{len(smooth)} = {sm_imp_rate:.0%}")
w(f"- Implied rate among rough: {ro_implied}/{len(rough)} = {ro_imp_rate:.0%}")
w("")

out_path = Path(__file__).parent / "02_regime_test.md"
out_path.write_text('\n'.join(L))
print(f"\nMarkdown written to {out_path}")
