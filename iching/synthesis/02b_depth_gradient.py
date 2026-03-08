#!/usr/bin/env python3
"""
Verify depth gradient of 凶 within I=0 basin.
Quick diagnostic — output to stdout.
"""

import sys
import json
import importlib.util
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent.parent
ICHING = ROOT / "iching"
TEXTS_DIR = ROOT / "texts" / "iching"

sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))
sys.path.insert(0, str(ICHING / "kingwen"))

from cycle_algebra import NUM_HEX, bit, fmt6
from sequence import KING_WEN

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

p2 = _load("palace", ICHING / "huozhulin" / "02_palace_kernel.py")

# ─── Build lookups ────────────────────────────────────────────────────────

bin_to_kw, kw_to_bin, kw_to_name = {}, {}, {}
for _, (kw_num, name, bits_str) in enumerate(KING_WEN):
    b = [int(c) for c in bits_str]
    h = sum(b[j] << j for j in range(6))
    bin_to_kw[h] = kw_num
    kw_to_bin[kw_num] = h
    kw_to_name[kw_num] = name

_, hex_info = p2.generate_palaces()

with open(TEXTS_DIR / "yaoci.json") as f:
    yaoci_data = json.load(f)
yaoci = {}
for e in yaoci_data['entries']:
    yaoci[e['number']] = [line['text'] for line in e['lines']]

# ─── Classify hexagrams ──────────────────────────────────────────────────

I_comp = lambda h: bit(h, 2) ^ bit(h, 3)

def category(h):
    """Returns (category_label, sort_key)."""
    if I_comp(h) == 1:
        return "Cycle", 3
    return f"I=0 depth {p2.depth(h)}", p2.depth(h)

# ═════════════════════════════════════════════════════════════════════════
# 1. 凶 rate by depth category
# ═════════════════════════════════════════════════════════════════════════

print("=" * 60)
print("DEPTH GRADIENT: 凶 rate by convergence depth")
print("=" * 60)

cat_counts = defaultdict(lambda: [0, 0])  # [total_lines, xiong_count]
for h in range(64):
    cat, _ = category(h)
    kw = bin_to_kw[h]
    for text in yaoci[kw]:
        cat_counts[cat][0] += 1
        if "凶" in text:
            cat_counts[cat][1] += 1

order = ["I=0 depth 0", "I=0 depth 1", "I=0 depth 2", "Cycle"]
print(f"\n  {'Category':<16s} | {'Total':>5s} | {'凶':>4s} | {'Rate':>7s} | Hexagrams")
print(f"  {'─'*16}─┼─{'─'*5}─┼─{'─'*4}─┼─{'─'*7}─┼─{'─'*20}")
for cat in order:
    total, xiong = cat_counts[cat]
    rate = xiong / total if total else 0
    # Count hexagrams in category
    hexes = [h for h in range(64) if category(h)[0] == cat]
    print(f"  {cat:<16s} | {total:>5d} | {xiong:>4d} |  {rate:.4f} | {len(hexes)}")

# ═════════════════════════════════════════════════════════════════════════
# 2. Verify Qian/Kun zero-凶
# ═════════════════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print("VERIFY: KW#1 (乾) and KW#2 (坤) 爻辭")
print("=" * 60)

for kw in [1, 2]:
    h = kw_to_bin[kw]
    name = kw_to_name[kw]
    print(f"\n  KW#{kw} {name} ({fmt6(h)}):")
    has_xiong = False
    for i, text in enumerate(yaoci[kw]):
        marker = " ← 凶!" if "凶" in text else ""
        print(f"    Line {i+1}: {text}{marker}")
        if "凶" in text:
            has_xiong = True
    print(f"  → {'HAS 凶' if has_xiong else 'Zero 凶'} ✓" if not has_xiong else f"  → HAS 凶 ✗")

# ═════════════════════════════════════════════════════════════════════════
# 3. Depth-1 hexagrams with 凶 counts
# ═════════════════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print("DEPTH-1 I=0 HEXAGRAMS: 凶 counts")
print("=" * 60)

depth1 = [(h, bin_to_kw[h]) for h in range(64) if I_comp(h) == 0 and p2.depth(h) == 1]
depth1.sort(key=lambda x: x[1])  # sort by KW number

print(f"\n  {'KW#':>4s} {'Name':<6s} {'Binary':>8s} {'Basin':<6s} | {'凶 count':>8s} {'/ 6':>4s} {'Rate':>7s}")
print(f"  {'─'*4} {'─'*6} {'─'*8} {'─'*6}─┼─{'─'*8} {'─'*4} {'─'*7}")
total_xiong_d1, total_lines_d1 = 0, 0
for h, kw in depth1:
    name = kw_to_name[kw]
    basin = hex_info[h]['basin']
    xiong = sum(1 for t in yaoci[kw] if "凶" in t)
    total_xiong_d1 += xiong
    total_lines_d1 += 6
    print(f"  {kw:>4d} {name:<6s} {fmt6(h):>8s} {basin:<6s} | {xiong:>8d}   /6  {xiong/6:.4f}")

print(f"\n  Total: {total_xiong_d1} 凶 in {total_lines_d1} lines = {total_xiong_d1/total_lines_d1:.4f}")

# ═════════════════════════════════════════════════════════════════════════
# 4. Statistical test: depth gradient within I=0
# ═════════════════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print("STATISTICAL TEST: Depth gradient within I=0")
print("=" * 60)

# Build contingency: rows = depth 0/1/2, cols = [凶, not-凶]
contingency = []
depth_labels = []
for d in [0, 1, 2]:
    cat = f"I=0 depth {d}"
    total, xiong = cat_counts[cat]
    contingency.append([xiong, total - xiong])
    depth_labels.append(d)

contingency = np.array(contingency)
print(f"\n  Contingency table (depth × 凶):")
print(f"  {'Depth':>6s} | {'凶':>4s} | {'¬凶':>5s} | {'Total':>5s} | {'Rate':>7s}")
for i, d in enumerate(depth_labels):
    total = contingency[i].sum()
    print(f"  {d:>6d} | {contingency[i,0]:>4d} | {contingency[i,1]:>5d} | {total:>5d} | {contingency[i,0]/total:.4f}")

# χ² test
chi2, p, dof, expected = stats.chi2_contingency(contingency)
print(f"\n  χ² = {chi2:.4f}, dof = {dof}, p = {p:.6f}")
print(f"  {'SIGNIFICANT' if p < 0.05 else 'NOT significant'} at α=0.05")

# Cochran-Armitage trend test (manual implementation)
# H0: no linear trend in proportions across ordered depth levels
n = contingency.sum(axis=1)  # total per depth
x = contingency[:, 0]        # 凶 counts
scores = np.array([0, 1, 2])  # depth as scores
N = n.sum()
p_hat = x.sum() / N
numer = np.sum(scores * x) - (np.sum(scores * n) * x.sum() / N)
denom_sq = p_hat * (1 - p_hat) * (np.sum(scores**2 * n) - (np.sum(scores * n))**2 / N)
Z_ca = numer / np.sqrt(denom_sq)
p_ca = 2 * (1 - stats.norm.cdf(abs(Z_ca)))
print(f"\n  Cochran-Armitage trend test:")
print(f"  Z = {Z_ca:.4f}, p = {p_ca:.6f}")
print(f"  {'SIGNIFICANT' if p_ca < 0.05 else 'NOT significant'} at α=0.05")
print(f"  Direction: {'increasing' if Z_ca > 0 else 'decreasing'} 凶 with depth")

# ═════════════════════════════════════════════════════════════════════════
# Summary
# ═════════════════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print("SUMMARY")
print("=" * 60)
d0_rate = cat_counts["I=0 depth 0"][1] / cat_counts["I=0 depth 0"][0]
d1_rate = cat_counts["I=0 depth 1"][1] / cat_counts["I=0 depth 1"][0]
d2_rate = cat_counts["I=0 depth 2"][1] / cat_counts["I=0 depth 2"][0]
cy_rate = cat_counts["Cycle"][1] / cat_counts["Cycle"][0]
print(f"\n  Depth 0 (attractors):  {d0_rate:.4f}")
print(f"  Depth 1 (penultimate): {d1_rate:.4f}")
print(f"  Depth 2 (deep):       {d2_rate:.4f}")
print(f"  Cycle:                 {cy_rate:.4f}")

predicted_gradient = (d0_rate < d1_rate) or (d0_rate == 0 and d1_rate > d2_rate)
print(f"\n  Predicted gradient (0 → peak at 1 → lower at 2):")
print(f"    d0 < d1: {d0_rate:.4f} < {d1_rate:.4f} → {d0_rate < d1_rate}")
print(f"    d1 > d2: {d1_rate:.4f} > {d2_rate:.4f} → {d1_rate > d2_rate}")
print(f"    d0 = 0:  {d0_rate == 0}")
