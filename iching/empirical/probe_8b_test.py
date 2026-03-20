#!/usr/bin/env python3
"""
Probe 8b: Event classification + statistical tests on 皇極經世 vol 6.

Tests whether event character correlates with position in the 天干/五行 cycle.
Expected outcome: null. Informative either way.

Uses hjjs_events.json from probe_8b_parse.py.
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from itertools import permutations
import numpy as np
from scipy.stats import chi2_contingency, chi2

HERE = Path(__file__).resolve().parent

# ─── Constants ───────────────────────────────────────────────────────────────

TIANGAN = "甲乙丙丁戊己庚辛壬癸"
DIZHI = "子丑寅卯辰巳午未申酉戌亥"

# 天干 → 五行 (paired: 甲乙=木, 丙丁=火, 戊己=土, 庚辛=金, 壬癸=水)
TIANGAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

# 地支 → 五行
DIZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水",
}

ELEMENTS_ZH = ["木", "火", "土", "金", "水"]

# 五行 生 cycle: 木→火→土→金→水→木
SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}

# 五行 克 cycle: 木→土→水→火→金→木
KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

# ─── Verb keyword lists ──────────────────────────────────────────────────────

UNFAV_VERBS = list("伐敗殺弑陷滅亂寇叛篡誅攻破戰圍廢")
# 死 in context of violence (not natural death which uses 卒/崩)
UNFAV_VERBS.append("死")

FAVOR_VERBS = ["平", "封", "㑹", "會", "和", "冊", "朝", "降"]
FAVOR_PHRASES = ["稱帝", "稱王"]
# 立 when establishing rule (not in 立之 succession context — too ambiguous, exclude)

# Neutral succession markers (ignored for classification)
NEUTRAL_MARKERS = list("卒崩薨繼嗣")
NEUTRAL_PHRASES = ["踐位", "是謂", "改元"]

# ─── Classification function ─────────────────────────────────────────────────

def classify_event(text):
    """Classify event text as favorable/unfavorable/mixed/neutral.
    Returns (class_label, unfav_count, fav_count)."""
    if not text:
        return ("blank", 0, 0)

    unfav = sum(text.count(v) for v in UNFAV_VERBS)
    fav = sum(text.count(v) for v in FAVOR_VERBS)
    fav += sum(text.count(p) for p in FAVOR_PHRASES)

    if unfav > 0 and fav > 0:
        return ("mixed", unfav, fav)
    elif unfav > 0:
        return ("unfavorable", unfav, fav)
    elif fav > 0:
        return ("favorable", unfav, fav)
    else:
        return ("neutral", 0, 0)

# ─── Five-phase relation ─────────────────────────────────────────────────────

def wuxing_relation(stem_elem, branch_elem):
    """Return the 五行 relation between stem and branch elements."""
    if stem_elem == branch_elem:
        return "比和"
    elif SHENG[stem_elem] == branch_elem:
        return "干生支"
    elif SHENG[branch_elem] == stem_elem:
        return "支生干"
    elif KE[stem_elem] == branch_elem:
        return "干克支"
    elif KE[branch_elem] == stem_elem:
        return "支克干"
    else:
        raise ValueError(f"No relation between {stem_elem} and {branch_elem}")

# ─── Cramér's V with CI ──────────────────────────────────────────────────────

def cramers_v(chi2_val, n, r, c):
    """Compute Cramér's V and approximate 95% CI."""
    k = min(r - 1, c - 1)
    v = np.sqrt(chi2_val / (n * k)) if n * k > 0 else 0
    # Bias-corrected V (for small samples)
    v_bc = max(0, np.sqrt(max(0, chi2_val / n - (r - 1) * (c - 1) / (n - 1)) / k))
    # Approximate SE via delta method: SE(V) ≈ 1/sqrt(n * k) for large n
    se = 1 / np.sqrt(n * k) if n * k > 0 else 0
    ci_lo = max(0, v - 1.96 * se)
    ci_hi = v + 1.96 * se
    return v, v_bc, ci_lo, ci_hi

# ─── Load data ───────────────────────────────────────────────────────────────

data = json.load(open(HERE / "hjjs_events.json"))
print(f"Loaded {len(data)} entries ({sum(1 for e in data if e['text'])} with text)\n")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 1: Event Classification
# ═══════════════════════════════════════════════════════════════════════════════

print("=" * 70)
print("PART 1: EVENT CLASSIFICATION")
print("=" * 70)

classified = []
for e in data:
    label, uc, fc = classify_event(e["text"])
    classified.append({
        **e,
        "class": label,
        "unfav_count": uc,
        "fav_count": fc,
        "stem_elem": TIANGAN_WUXING[e["tiangan"]],
        "branch_elem": DIZHI_WUXING[e["dizhi"]],
    })

class_dist = Counter(c["class"] for c in classified)
print("\nClass distribution:")
for cls in ["unfavorable", "favorable", "mixed", "neutral", "blank"]:
    n = class_dist.get(cls, 0)
    pct = n / len(classified) * 100
    print(f"  {cls:12s}: {n:4d}  ({pct:5.1f}%)")
print(f"  {'TOTAL':12s}: {len(classified):4d}")

# Examples from each class
for cls in ["unfavorable", "favorable", "mixed", "neutral"]:
    examples = [c for c in classified if c["class"] == cls][:3]
    print(f"\n  Examples of '{cls}':")
    for ex in examples:
        gz = ex["tiangan"] + ex["dizhi"]
        print(f"    {gz} L{ex['line']:4d} [{ex['unfav_count']}U/{ex['fav_count']}F] {ex['text'][:65]}")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 2: Sexagenary pairs + stem-branch 五行 relations
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("PART 2: SEXAGENARY PAIR 五行 RELATIONS")
print("=" * 70)

# Generate all 60 pairs
ganzhi_60 = [(TIANGAN[i % 10], DIZHI[i % 12]) for i in range(60)]

print("\n60 sexagenary pairs with 五行 relations:")
rel_dist = Counter()
for i, (tg, dz) in enumerate(ganzhi_60):
    se = TIANGAN_WUXING[tg]
    be = DIZHI_WUXING[dz]
    rel = wuxing_relation(se, be)
    rel_dist[rel] += 1
    if i < 10 or i >= 50:  # show first/last 10
        print(f"  {tg}{dz}  {se}×{be} = {rel}")
    elif i == 10:
        print(f"  ... (40 more) ...")

print(f"\nRelation distribution across 60 pairs:")
for rel in ["比和", "干生支", "支生干", "干克支", "支克干"]:
    print(f"  {rel}: {rel_dist[rel]:2d}/60")

# Confound check: do relation types cluster by decade?
print(f"\nConfound check — relation by decade of 60-year cycle:")
print(f"  {'Decade':>8s}  比和 干生支 支生干 干克支 支克干")
for decade in range(6):
    row = Counter()
    for i in range(decade * 10, (decade + 1) * 10):
        tg, dz = ganzhi_60[i]
        rel = wuxing_relation(TIANGAN_WUXING[tg], DIZHI_WUXING[dz])
        row[rel] += 1
    cells = [row.get(r, 0) for r in ["比和", "干生支", "支生干", "干克支", "支克干"]]
    label = f"{ganzhi_60[decade*10][0]}{ganzhi_60[decade*10][1]}–{ganzhi_60[decade*10+9][0]}{ganzhi_60[decade*10+9][1]}"
    print(f"  {label:>8s}  {cells[0]:3d}  {cells[1]:5d}  {cells[2]:5d}  {cells[3]:5d}  {cells[4]:5d}")

# ═══════════════════════════════════════════════════════════════════════════════
# Filter to testable entries (favorable + unfavorable only)
# ═══════════════════════════════════════════════════════════════════════════════

testable = [c for c in classified if c["class"] in ("favorable", "unfavorable")]
n_test = len(testable)
n_unfav = sum(1 for c in testable if c["class"] == "unfavorable")
n_fav = sum(1 for c in testable if c["class"] == "favorable")
print(f"\n{'─'*70}")
print(f"Testable entries (favorable + unfavorable): {n_test}")
print(f"  Unfavorable: {n_unfav} ({n_unfav/n_test*100:.1f}%)")
print(f"  Favorable:   {n_fav} ({n_fav/n_test*100:.1f}%)")
print(f"  Excluded: {len(classified) - n_test} (mixed/neutral/blank)")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 3: Statistical Tests
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("PART 3: STATISTICAL TESTS")
print("=" * 70)

# ─── Test 1: event_character × 5 elements (天干→五行) ────────────────────────

print("\n" + "─" * 70)
print("TEST 1: event_character × 5 elements (天干→五行)")
print("─" * 70)

# Build 5×2 contingency table
elem_order = ELEMENTS_ZH
table1 = np.zeros((5, 2), dtype=int)
for c in testable:
    row = elem_order.index(c["stem_elem"])
    col = 0 if c["class"] == "unfavorable" else 1
    table1[row, col] += 1

print(f"\n{'Element':>8s}  {'Unfav':>6s}  {'Fav':>6s}  {'Total':>6s}  {'%Unfav':>7s}")
for i, elem in enumerate(elem_order):
    total = table1[i].sum()
    pct = table1[i, 0] / total * 100 if total > 0 else 0
    print(f"{elem:>8s}  {table1[i,0]:6d}  {table1[i,1]:6d}  {total:6d}  {pct:6.1f}%")
totals = table1.sum(axis=0)
print(f"{'Total':>8s}  {totals[0]:6d}  {totals[1]:6d}  {totals.sum():6d}  {totals[0]/totals.sum()*100:6.1f}%")

chi2_1, p1, dof1, expected1 = chi2_contingency(table1)
v1, v1_bc, v1_lo, v1_hi = cramers_v(chi2_1, n_test, 5, 2)
print(f"\nχ² = {chi2_1:.3f}, df = {dof1}, p = {p1:.4f}")
print(f"Cramér's V = {v1:.4f} (bias-corrected: {v1_bc:.4f})")
print(f"95% CI for V: [{v1_lo:.4f}, {v1_hi:.4f}]")

# ─── Test 2: event_character × 10 stems ──────────────────────────────────────

print("\n" + "─" * 70)
print("TEST 2: event_character × 10 stems (天干)")
print("─" * 70)

table2 = np.zeros((10, 2), dtype=int)
for c in testable:
    row = TIANGAN.index(c["tiangan"])
    col = 0 if c["class"] == "unfavorable" else 1
    table2[row, col] += 1

print(f"\n{'Stem':>6s}  {'Elem':>4s}  {'Unfav':>6s}  {'Fav':>6s}  {'Total':>6s}  {'%Unfav':>7s}")
for i, tg in enumerate(TIANGAN):
    total = table2[i].sum()
    pct = table2[i, 0] / total * 100 if total > 0 else 0
    print(f"{tg:>6s}  {TIANGAN_WUXING[tg]:>4s}  {table2[i,0]:6d}  {table2[i,1]:6d}  {total:6d}  {pct:6.1f}%")

chi2_2, p2, dof2, expected2 = chi2_contingency(table2)
v2, v2_bc, v2_lo, v2_hi = cramers_v(chi2_2, n_test, 10, 2)
print(f"\nχ² = {chi2_2:.3f}, df = {dof2}, p = {p2:.4f}")
print(f"Cramér's V = {v2:.4f} (bias-corrected: {v2_bc:.4f})")
print(f"95% CI for V: [{v2_lo:.4f}, {v2_hi:.4f}]")

# ─── Test 3: 120-permutation control ─────────────────────────────────────────

print("\n" + "─" * 70)
print("TEST 3: 120-permutation control")
print("  (Is the canonical 五行 ordering special among all assignments?)")
print("─" * 70)

# The canonical assignment: pair 0 (甲乙)=木, pair 1 (丙丁)=火, pair 2 (戊己)=土,
# pair 3 (庚辛)=金, pair 4 (壬癸)=水
# For each of 120 permutations of 5 elements, reassign elements and recompute χ²

# Precompute: for each testable entry, which stem-pair (0-4) does it belong to?
stem_pairs = []
for c in testable:
    pair_idx = TIANGAN.index(c["tiangan"]) // 2  # 0-4
    stem_pairs.append((pair_idx, 0 if c["class"] == "unfavorable" else 1))

canonical_elems = tuple(ELEMENTS_ZH)  # (木, 火, 土, 金, 水)

# The χ² statistic is invariant to row permutation: permuting which pair maps
# to which element just reorders rows in the contingency table, leaving
# ∑(O-E)²/E unchanged (each (O[i,j], R[i]) pair moves together).
# So all 120 permutations give identical χ². This is a structural property,
# not a data issue.
#
# Alternative test: compare canonical pair unfavorable-rate variance against
# random 5-group partitions of the testable entries. This tests whether the
# 天干 pair structure captures more variance than random groupings.

pair_rates = []
for pair_idx in range(5):
    pair_entries = [(p, c) for p, c in stem_pairs if p == pair_idx]
    n_p = len(pair_entries)
    n_unfav_p = sum(1 for _, c in pair_entries if c == 0)
    rate = n_unfav_p / n_p if n_p > 0 else 0
    pair_rates.append(rate)

canonical_var = np.var(pair_rates)

# Monte Carlo: 10000 random 5-group partitions
rng = np.random.default_rng(42)
n_mc = 10000
labels = np.array([c for _, c in stem_pairs])  # 0=unfav, 1=fav
sizes = [sum(1 for p, _ in stem_pairs if p == i) for i in range(5)]
mc_vars = []
for _ in range(n_mc):
    shuffled = rng.permutation(labels)
    rates = []
    offset = 0
    for s in sizes:
        chunk = shuffled[offset:offset + s]
        rates.append(chunk.mean() if len(chunk) > 0 else 0)
        offset += s
    # Note: mean of 0/1 = proportion of 1 = favorable rate
    # We want unfavorable rate = 1 - favorable rate
    mc_vars.append(np.var([1 - r for r in rates]))

mc_vars = np.array(mc_vars)
perm_rank = (mc_vars >= canonical_var).sum()
perm_p = perm_rank / n_mc

print(f"\nNote: χ² is invariant to row permutation (all 120 give {chi2_1:.3f}).")
print(f"Using Monte Carlo variance test instead (10,000 random groupings).")
print(f"\nCanonical pair unfav-rate variance: {canonical_var:.6f}")
print(f"  Pair rates: {', '.join(f'{r:.3f}' for r in pair_rates)}")
print(f"Monte Carlo null distribution:")
print(f"  Mean: {mc_vars.mean():.6f}, Median: {np.median(mc_vars):.6f}")
print(f"  95th percentile: {np.percentile(mc_vars, 95):.6f}")
print(f"  Rank of canonical: {perm_rank}/{n_mc} (p = {perm_p:.4f})")
print(f"Significant at α=0.05? {'YES' if perm_p < 0.05 else 'NO'}")

# ─── Test 4: stem-branch relational test ─────────────────────────────────────

print("\n" + "─" * 70)
print("TEST 4: event_character × stem-branch 五行 relation")
print("  ⚠ This tests 八字 year-pillar interpretation, not 梅花 date formula")
print("─" * 70)

# Classify each testable entry by its stem-branch relation
rel_types = ["比和", "干生支", "支生干", "干克支", "支克干"]
table4 = np.zeros((5, 2), dtype=int)
for c in testable:
    rel = wuxing_relation(c["stem_elem"], c["branch_elem"])
    row = rel_types.index(rel)
    col = 0 if c["class"] == "unfavorable" else 1
    table4[row, col] += 1

print(f"\n{'Relation':>8s}  {'Unfav':>6s}  {'Fav':>6s}  {'Total':>6s}  {'%Unfav':>7s}")
for i, rel in enumerate(rel_types):
    total = table4[i].sum()
    pct = table4[i, 0] / total * 100 if total > 0 else 0
    print(f"{rel:>8s}  {table4[i,0]:6d}  {table4[i,1]:6d}  {total:6d}  {pct:6.1f}%")

chi2_4, p4, dof4, expected4 = chi2_contingency(table4)
v4, v4_bc, v4_lo, v4_hi = cramers_v(chi2_4, n_test, 5, 2)
print(f"\nχ² = {chi2_4:.3f}, df = {dof4}, p = {p4:.4f}")
print(f"Cramér's V = {v4:.4f} (bias-corrected: {v4_bc:.4f})")
print(f"95% CI for V: [{v4_lo:.4f}, {v4_hi:.4f}]")

# ─── Test 5: Effect size bounds ──────────────────────────────────────────────

print("\n" + "─" * 70)
print("TEST 5: Effect size bounds (Test 1)")
print("─" * 70)

# Compute unfavorable rate per element with 95% CI (Wilson score interval)
def wilson_ci(k, n, z=1.96):
    """Wilson score interval for binomial proportion."""
    if n == 0:
        return 0, 0, 0
    p_hat = k / n
    denom = 1 + z**2 / n
    center = (p_hat + z**2 / (2*n)) / denom
    half = z * np.sqrt(p_hat * (1 - p_hat) / n + z**2 / (4*n**2)) / denom
    return p_hat, max(0, center - half), min(1, center + half)

print(f"\nUnfavorable rate per element (with 95% Wilson CI):")
rates = {}
for i, elem in enumerate(elem_order):
    k = table1[i, 0]
    n = table1[i].sum()
    p_hat, ci_lo, ci_hi = wilson_ci(k, n)
    rates[elem] = (p_hat, ci_lo, ci_hi, n)
    print(f"  {elem}: {p_hat:.3f} [{ci_lo:.3f}, {ci_hi:.3f}]  (n={n})")

# Max pairwise difference
max_diff = 0
max_pair = ("", "")
for i, e1 in enumerate(elem_order):
    for j, e2 in enumerate(elem_order):
        if i < j:
            diff = abs(rates[e1][0] - rates[e2][0])
            if diff > max_diff:
                max_diff = diff
                max_pair = (e1, e2)

# 95% CI for max difference (conservative: use individual CIs)
r1 = rates[max_pair[0]]
r2 = rates[max_pair[1]]
# Approximate SE of difference
se_diff = np.sqrt(r1[0]*(1-r1[0])/r1[3] + r2[0]*(1-r2[0])/r2[3])
diff_ci_hi = max_diff + 1.96 * se_diff

print(f"\nLargest pairwise difference:")
print(f"  {max_pair[0]} vs {max_pair[1]}: Δ = {max_diff:.3f}")
print(f"  95% CI upper bound: {diff_ci_hi:.3f}")
print(f"\n  → With N={n_test}, if an effect of element on event character exists,")
print(f"    it is smaller than {diff_ci_hi:.1%} difference in unfavorable rate.")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 4: Transition analysis (from exploration-log.md)
# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 70)
print("PART 4: TRANSITION ANALYSIS")
print("  (Consecutive-year 五行 relations from 天干 cycle)")
print("=" * 70)

def classify_transition(e1_elem, e2_elem):
    if e1_elem == e2_elem:
        return "比和"
    elif SHENG[e1_elem] == e2_elem:
        return "生"
    elif KE[e1_elem] == e2_elem:
        return "克"
    elif SHENG[e2_elem] == e1_elem:
        return "逆生"
    elif KE[e2_elem] == e1_elem:
        return "逆克"
    return "?"

# Analysis A: consecutive-year transitions (adjacent entries, both with text)
trans_consec = Counter()
for i in range(len(data) - 1):
    if data[i]["text"] and data[i+1]["text"]:
        rel = classify_transition(
            TIANGAN_WUXING[data[i]["tiangan"]],
            TIANGAN_WUXING[data[i+1]["tiangan"]])
        trans_consec[rel] += 1

n_consec = sum(trans_consec.values())
print(f"\nA) Consecutive-year transitions (N={n_consec}):")
for rel in ["比和", "生", "克", "逆生", "逆克"]:
    n = trans_consec.get(rel, 0)
    pct = n / n_consec * 100 if n_consec > 0 else 0
    print(f"  {rel:>4s}: {n:4d} ({pct:5.1f}%)")

# Analysis B: event-to-event transitions (skip blank years)
event_indices = [i for i, e in enumerate(data) if e["text"]]
events_only = [data[i] for i in event_indices]
trans_event = Counter()
gap_sizes = Counter()
for j in range(len(events_only) - 1):
    e1, e2 = events_only[j], events_only[j+1]
    gap = event_indices[j+1] - event_indices[j]
    gap_sizes[gap] += 1
    rel = classify_transition(
        TIANGAN_WUXING[e1["tiangan"]],
        TIANGAN_WUXING[e2["tiangan"]])
    trans_event[rel] += 1

n_event = sum(trans_event.values())
print(f"\nB) Event-to-event transitions, skipping blanks (N={n_event}):")
for rel in ["比和", "生", "克", "逆生", "逆克"]:
    n = trans_event.get(rel, 0)
    pct = n / n_event * 100 if n_event > 0 else 0
    print(f"  {rel:>4s}: {n:4d} ({pct:5.1f}%)")

n_ke = trans_event.get("克", 0)
print(f"\n  Year-gap distribution for event-to-event pairs:")
for g in sorted(gap_sizes.keys())[:8]:
    print(f"    gap={g}: {gap_sizes[g]:4d} ({gap_sizes[g]/n_event*100:.1f}%)")
if max(gap_sizes.keys()) > 8:
    remaining = sum(v for k, v in gap_sizes.items() if k > 8)
    print(f"    gap>8: {remaining:4d} ({remaining/n_event*100:.1f}%)")

print(f"\n  Design note: consecutive 天干 produce only 比和 and 生.")
print(f"  克 requires gap ≥ 3. With {n_ke} 克 transitions total,")
print(f"  E2 (克→克 suppression) and E3 (valve: 克→生=0) are")
print(f"  structurally untestable — zero statistical power.")

# ═══════════════════════════════════════════════════════════════════════════════
# PART 5: Save results
# ═══════════════════════════════════════════════════════════════════════════════

results_md = f"""# Probe 8b Test Results

> Statistical tests on 皇極經世 vol 6 event data.
> Tests whether event character correlates with 天干/五行 cycle position.

---

## Data Summary

- Source: 皇極經世書 vol 6 (四庫全書 edition)
- Entries: {len(data)} total, {sum(1 for e in data if e['text'])} with text
- Period: ~44 × 30-year blocks (Warring States through Five Dynasties)

## Event Classification

| Class | Count | % |
|-------|------:|---:|
| Unfavorable | {class_dist.get('unfavorable',0)} | {class_dist.get('unfavorable',0)/len(classified)*100:.1f}% |
| Favorable | {class_dist.get('favorable',0)} | {class_dist.get('favorable',0)/len(classified)*100:.1f}% |
| Mixed | {class_dist.get('mixed',0)} | {class_dist.get('mixed',0)/len(classified)*100:.1f}% |
| Neutral | {class_dist.get('neutral',0)} | {class_dist.get('neutral',0)/len(classified)*100:.1f}% |
| Blank | {class_dist.get('blank',0)} | {class_dist.get('blank',0)/len(classified)*100:.1f}% |

Testable (favorable + unfavorable): **{n_test}** entries.

## Test Results

### Test 1: event_character × 5 elements (天干→五行)

χ² = {chi2_1:.3f}, df = {dof1}, **p = {p1:.4f}**
Cramér's V = {v1:.4f} [{v1_lo:.4f}, {v1_hi:.4f}]

| Element | Unfav | Fav | Total | %Unfav |
|---------|------:|----:|------:|-------:|"""

for i, elem in enumerate(elem_order):
    total = table1[i].sum()
    pct = table1[i, 0] / total * 100 if total > 0 else 0
    results_md += f"\n| {elem} | {table1[i,0]} | {table1[i,1]} | {total} | {pct:.1f}% |"

results_md += f"""

**Result: {'NULL — no significant association' if p1 > 0.05 else 'SIGNIFICANT association detected'}.**

### Test 2: event_character × 10 stems

χ² = {chi2_2:.3f}, df = {dof2}, **p = {p2:.4f}**
Cramér's V = {v2:.4f} [{v2_lo:.4f}, {v2_hi:.4f}]

**Result: {'NULL' if p2 > 0.05 else 'SIGNIFICANT'}.**

### Test 3: Permutation control

χ² is invariant to row permutation — all 120 element assignments give
identical χ² = {chi2_1:.3f}. This is a structural property: permuting
which stem-pair maps to which element just reorders rows in the table.

Monte Carlo variance test (10,000 random 5-group partitions):
- Canonical pair-rate variance: {canonical_var:.6f}
- Monte Carlo p = {perm_p:.4f}

**Result: canonical 五行 ordering {'IS' if perm_p < 0.05 else 'is NOT'} special among random groupings.**

### Test 4: event_character × stem-branch 五行 relation

⚠ Tests 八字 year-pillar interpretation, not 梅花 date formula.

χ² = {chi2_4:.3f}, df = {dof4}, **p = {p4:.4f}**
Cramér's V = {v4:.4f} [{v4_lo:.4f}, {v4_hi:.4f}]

**Result: {'NULL' if p4 > 0.05 else 'SIGNIFICANT'}.**

### Test 5: Effect size bounds

With N={n_test}, if an effect exists, the maximum difference in unfavorable
rate between any two elements is bounded by **{diff_ci_hi:.1%}** (95% CI).

Largest observed difference: {max_pair[0]} vs {max_pair[1]} = {max_diff:.3f}

## Transition Analysis

Consecutive-year transitions (N={n_consec}):
- 比和: {trans_consec.get('比和',0)} ({trans_consec.get('比和',0)/n_consec*100:.1f}%)
- 生: {trans_consec.get('生',0)} ({trans_consec.get('生',0)/n_consec*100:.1f}%)
- 克: {trans_consec.get('克',0)} ({trans_consec.get('克',0)/n_consec*100:.1f}%)

Event-to-event transitions, skipping blanks (N={n_event}):
- 比和: {trans_event.get('比和',0)} ({trans_event.get('比和',0)/n_event*100:.1f}%)
- 生: {trans_event.get('生',0)} ({trans_event.get('生',0)/n_event*100:.1f}%)
- 克: {trans_event.get('克',0)} ({trans_event.get('克',0)/n_event*100:.1f}%)

The 天干 cycle structurally forbids 克 at the year-to-year level.
Even with gaps, only {trans_event.get('克',0)} 克 transitions exist.
E2 (克→克 suppression) and E3 (valve: 克→生=0) are **structurally untestable**.

## Synthesis

{'All tests return null. No detectable association between 天干/五行 cycle position and event character at the year level. This bounds the grammar resolution: the 梅花 date formula requires finer temporal input (full date+hour) to generate relational predictions. A single years 天干 label does not carry predictive information about historical event character.' if p1 > 0.05 and p2 > 0.05 and p4 > 0.05 else 'Significant results detected — see individual tests above for details.'}
"""

out_path = HERE / "probe_8b_test_results.md"
with open(out_path, 'w') as f:
    f.write(results_md)

print(f"\n{'='*70}")
print(f"Results saved to {out_path}")
print(f"{'='*70}")
