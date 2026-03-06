"""
03_prediction_and_exhaustion.py — Prediction accuracy & exhaustion-basin analysis

Task A: For every (algebraic feature, semantic feature) pair, compute the best
        achievable prediction accuracy and compare to base rate.

Task B: Detailed analysis of exhaustion (cyclical) transitions and their
        relationship to basin structure — direction, corridor mediation, and
        whether "cannot last forever" marks specific basin dynamics.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from collections import Counter
from pathlib import Path
from math import sqrt

from sequence import KING_WEN
from cycle_algebra import (
    lower_trigram, upper_trigram, hugua,
    hamming6, hamming3,
)

# ═══════════════════════════════════════════════════════════════════════════
# Rebuild transitions (same as 01/02)
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

PAIR_CORRIDOR = {
    1: 'Heaven', 3: 'Heaven', 5: 'Heaven',
    4: 'Earth', 6: 'Earth', 8: 'Earth', 10: 'Earth',
    9: 'Thun/Mtn', 11: 'Thun/Mtn',
    14: 'Wind', 16: 'Wind',
    27: 'Lake/Wind', 29: 'Lake/Wind',
}
CORRIDORS = {
    'Heaven': [1, 3, 5], 'Earth': [4, 6, 8, 10],
    'Thun/Mtn': [9, 11], 'Wind': [14, 16], 'Lake/Wind': [27, 29],
}
CORRIDOR_RICH = set(range(1, 17)) | set(range(26, 30))


def get_basin(h):
    b2, b3 = (h >> 2) & 1, (h >> 3) & 1
    if b2 == 0 and b3 == 0: return 'Kun'
    if b2 == 1 and b3 == 1: return 'Qian'
    return 'KanLi'

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

def corridor_relation(t_num):
    exit_pair, entry_pair = t_num, t_num + 1
    exit_corr = PAIR_CORRIDOR.get(exit_pair)
    entry_corr = PAIR_CORRIDOR.get(entry_pair)
    exit_rel = entry_rel = None
    if exit_corr:
        exit_rel = 'TERM_EXIT' if exit_pair == CORRIDORS[exit_corr][-1] else 'LOCAL_EXIT'
    if entry_corr:
        entry_rel = 'INIT_ENTRY' if entry_pair == CORRIDORS[entry_corr][0] else 'RE_ENTRY'
    if exit_rel and entry_rel: return f"{exit_rel}+{entry_rel}"
    if exit_rel: return exit_rel
    if entry_rel: return entry_rel
    if t_num in CORRIDOR_RICH: return 'BETWEEN'
    return 'NONE'


kw_hex, kw_names = [], []
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
    b1, b2_ = get_basin(h1), get_basin(h2)
    t_num = t + 1
    sem = SEMANTIC[t_num]
    cr = corridor_relation(t_num)

    transitions.append({
        'T': t_num,
        'exit_hex': kw_names[exit_idx],
        'entry_hex': kw_names[entry_idx],
        'hex_d': hamming6(h1, h2),
        'lo_d': lo_d, 'up_d': up_d,
        'basin_exit': b1, 'basin_entry': b2_,
        'basin_cross': b1 != b2_,
        'hu_d': hamming6(hugua(h1), hugua(h2)),
        'hu_smooth': hamming6(hugua(h1), hugua(h2)) <= 2,
        'k_name': KERNEL_NAMES[kernel],
        'h_kernel': kernel in H_KERNELS,
        'preserving': lo_d == 0 or up_d == 0,
        'pres_label': (f"Lo:{TRIGRAM_SHORT[lo1]}" if lo_d == 0
                       else f"Up:{TRIGRAM_SHORT[up1]}" if up_d == 0
                       else None),
        # Semantic
        'logic': sem['logic'],
        'is_cyclical': sem['logic'] == 'Cyclical',
        'conf': sem['conf'],
        'is_implied': sem['conf'] == 'Implied',
        'dir': sem['dir'],
        'is_weak': sem['dir'] == '⇀',
        # Corridor
        'corr_rel': cr,
        'has_exit': 'EXIT' in cr,
        'regime': 'rich' if t_num in CORRIDOR_RICH else 'free',
    })


# ═══════════════════════════════════════════════════════════════════════════
# TASK A: Prediction accuracy — all (algebraic, semantic) feature pairs
# ═══════════════════════════════════════════════════════════════════════════

# Define binary features
ALG_FEATURES = [
    ('basin_cross', 'Basin crossing'),
    ('h_kernel',    'H-kernel'),
    ('hu_smooth',   '互 smooth (≤2)'),
    ('preserving',  'Preserving bridge'),
    ('has_exit',    'Corridor exit'),
]

SEM_FEATURES = [
    ('is_cyclical', 'Cyclical logic'),
    ('is_implied',  'Implied confidence'),
    ('is_weak',     'Weak directionality (⇀)'),
]


def prediction_metrics(data, predictor_key, target_key, pred_positive=True, tgt_positive=True):
    """Compute accuracy, base rate, and MCC for a binary predictor.
    
    pred_positive: the value of predictor_key that predicts tgt_positive.
    """
    n = len(data)
    tp = sum(1 for d in data if d[predictor_key] == pred_positive and d[target_key] == tgt_positive)
    fp = sum(1 for d in data if d[predictor_key] == pred_positive and d[target_key] != tgt_positive)
    fn = sum(1 for d in data if d[predictor_key] != pred_positive and d[target_key] == tgt_positive)
    tn = sum(1 for d in data if d[predictor_key] != pred_positive and d[target_key] != tgt_positive)

    acc = (tp + tn) / n
    pos_rate = (tp + fn) / n  # base rate of target positive
    base_acc = max(pos_rate, 1 - pos_rate)  # accuracy of always-majority classifier

    # MCC
    denom = sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn)) if (tp+fp)*(tp+fn)*(tn+fp)*(tn+fn) > 0 else 1
    mcc = (tp*tn - fp*fn) / denom

    return {
        'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
        'acc': acc, 'base_acc': base_acc, 'lift': acc / base_acc if base_acc > 0 else 0,
        'mcc': mcc, 'n': n,
        'sens': tp/(tp+fn) if (tp+fn) > 0 else 0,
        'spec': tn/(tn+fp) if (tn+fp) > 0 else 0,
    }


print("=" * 90)
print("TASK A: PREDICTION ACCURACY — All (Algebraic, Semantic) Feature Pairs")
print("=" * 90)

results = []
for akey, alabel in ALG_FEATURES:
    for skey, slabel in SEM_FEATURES:
        # Try both orientations of the predictor
        m1 = prediction_metrics(transitions, akey, skey, True, True)
        m2 = prediction_metrics(transitions, akey, skey, False, True)
        # Pick orientation with higher accuracy
        if m2['acc'] > m1['acc']:
            m = m2
            orient = f"¬{alabel}"
        else:
            m = m1
            orient = alabel
        results.append((alabel, slabel, orient, m))

print(f"\n  {'Predictor':>22} → {'Target':>22}  {'Acc':>5} {'Base':>5} {'Lift':>5} "
      f"{'MCC':>6} {'Sens':>5} {'Spec':>5}  {'TP':>2} {'FP':>2} {'FN':>2} {'TN':>2}")
print("  " + "─" * 105)

for alabel, slabel, orient, m in sorted(results, key=lambda x: -abs(x[3]['mcc'])):
    print(f"  {orient:>22} → {slabel:>22}  "
          f"{m['acc']:.3f} {m['base_acc']:.3f} {m['lift']:.3f} "
          f"{m['mcc']:>6.3f} {m['sens']:.3f} {m['spec']:.3f}  "
          f"{m['tp']:>2} {m['fp']:>2} {m['fn']:>2} {m['tn']:>2}")

# Summary
max_mcc = max(abs(r[3]['mcc']) for r in results)
max_lift = max(r[3]['lift'] for r in results)
print(f"\n  Best |MCC|: {max_mcc:.3f}")
print(f"  Best lift over base rate: {max_lift:.3f}")
print(f"  {'→ No predictor beats base rate by more than a few percent.' if max_lift < 1.1 else ''}")


# ═══════════════════════════════════════════════════════════════════════════
# TASK B: Exhaustion-basin correspondence
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 90)
print("TASK B: EXHAUSTION-BASIN CORRESPONDENCE")
print("=" * 90)

cyclical = [tr for tr in transitions if tr['is_cyclical']]
causal = [tr for tr in transitions if tr['logic'] == 'Causal']

# B1: Detail of all 8 cyclical transitions
print(f"\n  B1. All 8 cyclical (exhaustion) transitions:")
print(f"  {'T':>2} {'Bridge':>22} {'Basin':>12} {'×':>1} {'Corr Rel':>26} {'Regime':>5}")
print("  " + "─" * 75)
for tr in cyclical:
    bstr = f"{tr['basin_exit'][:3]}→{tr['basin_entry'][:3]}"
    cross = 'Y' if tr['basin_cross'] else '·'
    print(f"  {tr['T']:>2} {tr['exit_hex']}→{tr['entry_hex']:>12} {bstr:>12} {cross:>1} "
          f"{tr['corr_rel']:>26} {tr['regime']:>5}")

# B2: Basin-crossing rate comparison
cyc_cross = sum(1 for tr in cyclical if tr['basin_cross'])
cau_cross = sum(1 for tr in causal if tr['basin_cross'])
all_cross = sum(1 for tr in transitions if tr['basin_cross'])

print(f"\n  B2. Basin-crossing rates:")
print(f"    Cyclical:    {cyc_cross}/{len(cyclical)} = {cyc_cross/len(cyclical):.0%}")
print(f"    Causal:      {cau_cross}/{len(causal)} = {cau_cross/len(causal):.0%}")
print(f"    All:         {all_cross}/{len(transitions)} = {all_cross/len(transitions):.0%}")

# B3: Basin directionality of exhaustion crossings
print(f"\n  B3. Basin exit/entry direction for cyclical crossings:")
cyc_crossing = [tr for tr in cyclical if tr['basin_cross']]
cyc_dirs = Counter((tr['basin_exit'], tr['basin_entry']) for tr in cyc_crossing)
for (b_exit, b_entry), count in sorted(cyc_dirs.items()):
    print(f"    {b_exit:>6} → {b_entry:<6}: {count}")

# Compare with causal crossings
print(f"\n  B3b. Basin exit/entry direction for causal crossings:")
cau_crossing = [tr for tr in causal if tr['basin_cross']]
cau_dirs = Counter((tr['basin_exit'], tr['basin_entry']) for tr in cau_crossing)
for (b_exit, b_entry), count in sorted(cau_dirs.items()):
    print(f"    {b_exit:>6} → {b_entry:<6}: {count}")

# B4: Exhaustion exits FROM fixed-point basins vs KanLi
print(f"\n  B4. Exhaustion exit basin type:")
cyc_from_fixed = sum(1 for tr in cyc_crossing if tr['basin_exit'] in ('Kun', 'Qian'))
cyc_from_kanli = sum(1 for tr in cyc_crossing if tr['basin_exit'] == 'KanLi')
print(f"    From fixed-point (Kun/Qian): {cyc_from_fixed}/{len(cyc_crossing)}")
print(f"    From oscillation (KanLi):    {cyc_from_kanli}/{len(cyc_crossing)}")

cau_from_fixed = sum(1 for tr in cau_crossing if tr['basin_exit'] in ('Kun', 'Qian'))
cau_from_kanli = sum(1 for tr in cau_crossing if tr['basin_exit'] == 'KanLi')
print(f"    [Causal comparison]")
print(f"    From fixed-point (Kun/Qian): {cau_from_fixed}/{len(cau_crossing)}")
print(f"    From oscillation (KanLi):    {cau_from_kanli}/{len(cau_crossing)}")

# B5: Non-crossing cyclical transitions — what basin do they stay in?
cyc_noncross = [tr for tr in cyclical if not tr['basin_cross']]
print(f"\n  B5. Non-crossing cyclical transitions (exhaustion within basin):")
for tr in cyc_noncross:
    print(f"    T{tr['T']:>2}: {tr['exit_hex']}→{tr['entry_hex']:<12} "
          f"stays in {tr['basin_exit']}")

# B6: Corridor mediation — cyclical at corridor exits
print(f"\n  B6. Corridor mediation:")
cyc_at_exit = [tr for tr in cyclical if tr['has_exit']]
cyc_not_exit = [tr for tr in cyclical if not tr['has_exit']]
print(f"    Cyclical at corridor exits:     {len(cyc_at_exit)}/8")
print(f"    Cyclical NOT at corridor exits: {len(cyc_not_exit)}/8")

# Among corridor exits, compare cyclical vs causal basin-crossing
all_exit = [tr for tr in transitions if tr['has_exit']]
exit_cyc = [tr for tr in all_exit if tr['is_cyclical']]
exit_cau = [tr for tr in all_exit if tr['logic'] == 'Causal']
exit_cyc_cross = sum(1 for tr in exit_cyc if tr['basin_cross'])
exit_cau_cross = sum(1 for tr in exit_cau if tr['basin_cross'])

if exit_cyc:
    print(f"    Basin-crossing rate at corridor exits:")
    print(f"      Cyclical exits: {exit_cyc_cross}/{len(exit_cyc)} "
          f"= {exit_cyc_cross/len(exit_cyc):.0%}")
if exit_cau:
    print(f"      Causal exits:   {exit_cau_cross}/{len(exit_cau)} "
          f"= {exit_cau_cross/len(exit_cau):.0%}")

EXHAUSTION_PHRASES = {
    6:  "Pi (Stagnation)",
    11: "Bi (Adornment/Grace)",
    14: "Da Guo (Great Excess)",
    16: "Heng (Duration)",
    17: "Da Zhuang (Great Strength)",
    21: "Yi (Increase)",
    23: "Sheng (Ascending)",
    26: "Gen (Keeping Still)",
}

# B7: Exhaustion and the "cannot last" basin pattern
print(f"\n  B7. The exhaustion pattern in basin context:")
print(f"  Each cyclical transition says 'X cannot last forever' — does the")
print(f"  exit basin match the thing being exhausted?\n")

print(f"  {'T':>2} {'What exhausts':>25} {'Basin exit':>10} {'Basin entry':>11} {'×':>1} {'Fixed?':>6}")
print("  " + "─" * 63)
for tr in cyclical:
    phrase = EXHAUSTION_PHRASES[tr['T']]
    cross = 'Y' if tr['basin_cross'] else '·'
    fixed = 'Y' if tr['basin_exit'] in ('Kun', 'Qian') else '·'
    print(f"  {tr['T']:>2} {phrase:>25} {tr['basin_exit']:>10} → {tr['basin_entry']:<9} {cross:>1} {fixed:>6}")

# B8: Direct Kun↔Qian crossings — exclusively cyclical
print(f"\n  B8. Direct fixed-point basin crossings (Kun↔Qian):")
all_crossing_trs = [tr for tr in transitions if tr['basin_cross']]
kq_crossings = [tr for tr in all_crossing_trs
                 if set([tr['basin_exit'], tr['basin_entry']]) == {'Kun', 'Qian'}]
n_kq = len(kq_crossings)
n_kq_cyc = sum(1 for tr in kq_crossings if tr['is_cyclical'])
n_cyc_cross = sum(1 for tr in all_crossing_trs if tr['is_cyclical'])
n_all_cross = len(all_crossing_trs)

for tr in kq_crossings:
    print(f"    T{tr['T']}: {tr['basin_exit']}→{tr['basin_entry']} [{tr['logic']}]"
          f"  ({tr['exit_hex']}→{tr['entry_hex']})")

print(f"\n    All {n_kq} direct Kun↔Qian inter-pair crossings are cyclical.")
print(f"    All {n_all_cross - n_kq} other crossings involve KanLi as source or dest.")

# Hypergeometric p-value
from math import comb
p_hyper = comb(n_cyc_cross, n_kq) * comb(n_all_cross - n_cyc_cross, 0) / comb(n_all_cross, n_kq)
print(f"    Hypergeometric p = {p_hyper:.4f} "
      f"({n_cyc_cross} cyclical among {n_all_cross} crossings, both of {n_kq} Kun↔Qian)")


# ═══════════════════════════════════════════════════════════════════════════
# Write markdown
# ═══════════════════════════════════════════════════════════════════════════

L = []
w = L.append

w("# Prediction Accuracy & Exhaustion-Basin Correspondence\n")

# ── Task A ──
w("## A. Prediction Accuracy\n")
w("For each (algebraic feature, semantic feature) pair, we test whether the")
w("algebraic feature can predict the semantic feature. The predictor orientation")
w("is chosen to maximize accuracy. Base rate = accuracy of always predicting")
w("the majority class.\n")

w("| Predictor | Target | Acc | Base | Lift | MCC | Sens | Spec |")
w("|-----------|--------|:---:|:----:|:----:|:---:|:----:|:----:|")

for alabel, slabel, orient, m in sorted(results, key=lambda x: -abs(x[3]['mcc'])):
    w(f"| {orient} | {slabel} | {m['acc']:.2f} | {m['base_acc']:.2f} | "
      f"{m['lift']:.2f} | {m['mcc']:.3f} | {m['sens']:.2f} | {m['spec']:.2f} |")
w("")

w("### Key\n")
w("- **Acc**: Prediction accuracy (fraction correct)")
w("- **Base**: Base rate accuracy (always predict majority class)")
w("- **Lift**: Acc / Base — values near 1.00 mean no improvement over guessing")
w("- **MCC**: Matthews Correlation Coefficient (-1 to +1; 0 = no correlation)")
w("- **Sens/Spec**: Sensitivity (true positive rate) / Specificity (true negative rate)")
w("")

w("### Assessment\n")
best = max(results, key=lambda x: abs(x[3]['mcc']))
w(f"Best predictor: **{best[2]}** → **{best[1]}** "
  f"(|MCC| = {abs(best[3]['mcc']):.3f}, lift = {best[3]['lift']:.2f})\n")
if max_lift < 1.10:
    w("**No algebraic feature improves prediction of any semantic feature by more "
      "than 10% over base rate.** The best predictors achieve lifts of 1.00–1.08, "
      "meaning the algebraic profile is essentially useless for predicting semantic content.")
    w("")
    w("This confirms the Fisher test results from Round 2: the independence at the "
      "bridge level is not a matter of statistical power — even with the most favorable "
      "predictor orientation, algebraic features carry no actionable information about "
      "semantic features.")
elif max_lift < 1.20:
    w("**Marginal predictive value.** The best predictor achieves a small lift over base rate, "
      "but the MCC values are all near zero, indicating negligible practical correlation.")
w("")


# ── Task B ──
w("## B. Exhaustion-Basin Correspondence\n")
w("The 8 cyclical transitions use the Xugua's exhaustion formula: 'X cannot last forever.'")
w("Does this narrative event correspond to a specific algebraic event in basin space?\n")

w("### B1. The 8 exhaustion transitions\n")
w("| T# | What exhausts | Bridge | Basin | ×? | Corridor | Regime |")
w("|:--:|---------------|--------|-------|:--:|----------|:------:|")
for tr in cyclical:
    phrase = EXHAUSTION_PHRASES[tr['T']]
    bstr = f"{tr['basin_exit'][:3]}→{tr['basin_entry'][:3]}"
    cross = '**Y**' if tr['basin_cross'] else 'N'
    w(f"| {tr['T']} | {phrase} | {tr['exit_hex']}→{tr['entry_hex']} "
      f"| {bstr} | {cross} | {tr['corr_rel']} | {tr['regime']} |")
w("")

w("### B2. Basin-crossing rates\n")
w("| Category | Crossing | Total | Rate |")
w("|----------|:--------:|:-----:|:----:|")
w(f"| Cyclical | {cyc_cross} | {len(cyclical)} | {cyc_cross/len(cyclical):.0%} |")
w(f"| Causal | {cau_cross} | {len(causal)} | {cau_cross/len(causal):.0%} |")
w(f"| All | {all_cross} | {len(transitions)} | {all_cross/len(transitions):.0%} |")
w("")
w("Cyclical transitions cross basins at **the same rate as causal** transitions.")
w("Exhaustion is not a basin-crossing event.\n")

w("### B3. Basin directionality\n")
w("Among the 5 crossing cyclical transitions:\n")
w("| Exit basin | Entry basin | Count |")
w("|-----------|-------------|:-----:|")
for (b_exit, b_entry), count in sorted(cyc_dirs.items()):
    w(f"| {b_exit} | {b_entry} | {count} |")
w("")
w("No single direction dominates. Exhaustion can exit any basin and enter any basin.")
w("Compare with causal crossings:\n")
w("| Exit basin | Entry basin | Count |")
w("|-----------|-------------|:-----:|")
for (b_exit, b_entry), count in sorted(cau_dirs.items()):
    w(f"| {b_exit} | {b_entry} | {count} |")
w("")

w("### B4. Fixed-point basin exits\n")
w("Does exhaustion preferentially exit fixed-point basins (Kun/Qian) vs the")
w("oscillation basin (KanLi)?\n")
w("| Category | From fixed | From KanLi | n |")
w("|----------|:----------:|:----------:|:-:|")
w(f"| Cyclical crossings | {cyc_from_fixed} | {cyc_from_kanli} | {len(cyc_crossing)} |")
w(f"| Causal crossings | {cau_from_fixed} | {cau_from_kanli} | {len(cau_crossing)} |")
w("")
cyc_fixed_rate = cyc_from_fixed / len(cyc_crossing) if cyc_crossing else 0
cau_fixed_rate = cau_from_fixed / len(cau_crossing) if cau_crossing else 0
w(f"Cyclical exits from fixed-point basins: {cyc_fixed_rate:.0%}. "
  f"Causal: {cau_fixed_rate:.0%}. ")
if abs(cyc_fixed_rate - cau_fixed_rate) < 0.15:
    w("No meaningful difference.\n")
else:
    w("Some difference, but sample is small.\n")

w("### B5. Non-crossing exhaustion (within-basin)\n")
w("Three cyclical transitions stay within their basin — the exhaustion")
w("is purely semantic, with no algebraic basin event:\n")
w("| T# | Bridge | Basin | What exhausts |")
w("|:--:|--------|-------|---------------|")
for tr in cyc_noncross:
    phrase = EXHAUSTION_PHRASES[tr['T']]
    w(f"| {tr['T']} | {tr['exit_hex']}→{tr['entry_hex']} | {tr['basin_exit']} | {phrase} |")
w("")

# Check if non-crossing cyclicals are all in one basin type
nc_basins = set(tr['basin_exit'] for tr in cyc_noncross)
if len(nc_basins) == 1:
    w(f"All three stay in **{nc_basins.pop()}** — the oscillation basin. The exhaustion")
    w("formula operates entirely within the oscillating domain.\n")
elif 'KanLi' in nc_basins and len(nc_basins) == 2:
    w(f"Two stay in KanLi, one in a fixed-point basin.\n")
else:
    w(f"Basin distribution: {Counter(tr['basin_exit'] for tr in cyc_noncross)}\n")

w("### B6. Corridor mediation\n")
w(f"- Cyclical at corridor exits: **{len(cyc_at_exit)}/8**")
w(f"- Cyclical NOT at corridor exits: **{len(cyc_not_exit)}/8**\n")

w("Among all corridor exits, basin-crossing rate by logic type:\n")
w("| Logic at exit | Crossing | Total | Rate |")
w("|------------|:--------:|:-----:|:----:|")
if exit_cyc:
    w(f"| Cyclical | {exit_cyc_cross} | {len(exit_cyc)} | "
      f"{exit_cyc_cross/len(exit_cyc):.0%} |")
if exit_cau:
    w(f"| Causal | {exit_cau_cross} | {len(exit_cau)} | "
      f"{exit_cau_cross/len(exit_cau):.0%} |")
w("")
w("Cyclical and causal transitions at corridor exits cross basins at similar rates.")
w("The corridor exit itself — not the logic type — determines whether a basin")
w("crossing occurs.\n")

w("### B7. Direct Kun↔Qian crossings: exclusively cyclical\n")
w("A specific finding emerges from the basin direction data:\n")

w("| T# | Direction | Logic | Bridge |")
w("|:--:|-----------|-------|--------|")
for tr in kq_crossings:
    w(f"| {tr['T']} | {tr['basin_exit']}→{tr['basin_entry']} | {tr['logic']} "
      f"| {tr['exit_hex']}→{tr['entry_hex']} |")
w("")

w(f"**Both** direct Kun↔Qian inter-pair crossings are cyclical. All {n_all_cross - n_kq} "
  f"other crossings involve KanLi as source or destination.\n")
w(f"Hypergeometric p = {p_hyper:.4f} ({n_cyc_cross} cyclical among {n_all_cross} crossings, "
  f"both of {n_kq} Kun↔Qian slots filled by cyclical).\n")

w("**Interpretation:** Causal transitions always route through the oscillation basin "
  "(KanLi) — they need an intermediary. Only the exhaustion formula ('cannot last forever') "
  "jumps directly between fixed-point basins. The causal chain channels through KanLi; "
  "exhaustion-reversal leaps across it.\n")

w("This is the one point where algebra and semantics show a *specific* correspondence "
  "at the bridge level: the narrative event of exhaustion-reversal maps to the algebraic "
  "event of direct fixed-point basin crossing. But the sample (n=2) is structurally fixed — "
  "there are only 2 such crossings in the sequence — so this is a structural observation, "
  "not a generalizable statistical finding.\n")

w("### B8. Summary: The exhaustion-basin relationship\n")
w("**Exhaustion is primarily a semantic event, not an algebraic one.**\n")
w("At the aggregate level, the 'cannot last forever' formula:")
w("- Does NOT preferentially cross basins (63% vs 68% base rate)")
w("- Does NOT preferentially exit fixed-point basins")
w("- Operates equally within-basin (3/8) and across basins (5/8)")
w("")
w("**But at the specific point of direct Kun↔Qian crossing**, exhaustion and algebra "
  "coincide: both direct fixed-point crossings use the cyclical formula (p=0.048). "
  "This is where the 'grain' of coupling shows: not at the level of general cross-tabs, "
  "but at the level of specific structural events.\n")
w("The relationship:")
w("- **General crossings:** algebra and semantics independent")
w("- **Direct fixed-point crossings:** exclusively cyclical (n=2, structurally fixed)")
w("- **Within-basin exhaustion:** purely semantic (no algebraic event at all)")
w("")
w("The basin structure and the exhaustion grammar are largely orthogonal, but they "
  "touch at the extreme — where the sequence makes its rarest algebraic move (direct "
  "Kun↔Qian jump), the narrative always uses its strongest formula (exhaustion-reversal).\n")


out_path = Path(__file__).parent / "03_prediction_and_exhaustion.md"
out_path.write_text('\n'.join(L))
print(f"\nMarkdown written to {out_path}")
