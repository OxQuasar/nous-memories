#!/usr/bin/env python3
"""
Q5 — 彖傳 anomaly detection

Prediction: In the 彖傳, the Kun basin (mostly yin hexagrams) has the
highest 剛/柔 ratio (2.14) — it comments on what's unusual.
Prediction: Qian basin (mostly yang) should have the LOWEST 剛/柔 ratio.

Also report Cycle basin ratio for completeness.
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path("/home/quasar/nous/memories/iching")
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
TEXTS_PATH = ROOT.parent / "texts" / "iching"

# ═══════════════════════════════════════════════════════════════
# Load data
# ═══════════════════════════════════════════════════════════════

print("=" * 72)
print("Q5: 彖傳 ANOMALY DETECTION — 剛/柔 RATIO BY BASIN")
print("=" * 72)

# Load atlas
with open(ATLAS_PATH) as f:
    atlas = json.load(f)

# Load 彖傳 text
tuan_path = TEXTS_PATH / "tuan.json"
if not tuan_path.exists():
    # Try alternative paths
    alt_paths = [
        ROOT / "semantic-map" / "data" / "tuanzhuan_structure.json",
    ]
    for p in alt_paths:
        if p.exists():
            tuan_path = p
            break

print(f"Loading 彖傳 from: {tuan_path}")

if tuan_path.name == "tuan.json":
    with open(tuan_path) as f:
        tuan_data = json.load(f)
    tuan_entries = tuan_data["entries"]
    # Map from KW number to text
    kw_to_text = {e["number"]: e["text"] for e in tuan_entries}
    kw_to_name = {e["number"]: e["name"] for e in tuan_entries}
elif tuan_path.name == "tuanzhuan_structure.json":
    with open(tuan_path) as f:
        tuan_data = json.load(f)
    tuan_entries = tuan_data["entries"]
    kw_to_text = {}
    kw_to_name = {}
    for e in tuan_entries:
        kw = e["kw_number"]
        kw_to_text[kw] = e["text"]
        kw_to_name[kw] = e["name"]

# Build hexval → basin mapping
hexval_to_basin = {}
hexval_to_kw = {}
kw_to_hexval = {}
for hv_str, h in atlas.items():
    hv = int(hv_str)
    hexval_to_basin[hv] = h["basin"]
    hexval_to_kw[hv] = h["kw_number"]
    kw_to_hexval[h["kw_number"]] = hv

# ═══════════════════════════════════════════════════════════════
# Count 剛 and 柔 per hexagram, group by basin
# ═══════════════════════════════════════════════════════════════

print(f"\nCounting 剛 and 柔 in each hexagram's 彖傳...")

basin_gang = defaultdict(int)
basin_rou = defaultdict(int)
basin_hexcount = defaultdict(int)
hex_details = []

for kw in sorted(kw_to_text.keys()):
    text = kw_to_text[kw]
    hv = kw_to_hexval[kw]
    basin = hexval_to_basin[hv]
    
    gang = text.count("剛")
    rou = text.count("柔")
    
    basin_gang[basin] += gang
    basin_rou[basin] += rou
    basin_hexcount[basin] += 1
    
    if gang > 0 or rou > 0:
        hex_details.append({
            'kw': kw,
            'name': kw_to_name.get(kw, '?'),
            'basin': basin,
            'gang': gang,
            'rou': rou,
            'binary': atlas[str(hv)]["binary"],
        })

# ═══════════════════════════════════════════════════════════════
# Report by basin
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"剛/柔 COUNTS AND RATIOS BY BASIN")
print(f"{'='*60}")

total_gang = sum(basin_gang.values())
total_rou = sum(basin_rou.values())

print(f"\n{'Basin':<12s} {'n_hex':>6s} {'剛':>6s} {'柔':>6s} {'ratio':>8s} {'prediction':>12s}")
print(f"{'─'*12:<12s} {'─'*6:>6s} {'─'*6:>6s} {'─'*6:>6s} {'─'*8:>8s} {'─'*12:>12s}")

basin_order = sorted(basin_gang.keys())
ratios = {}
for basin in basin_order:
    g = basin_gang[basin]
    r = basin_rou[basin]
    ratio = g / r if r > 0 else float('inf')
    ratios[basin] = ratio
    
    if "坤" in basin.lower() or "kun" in basin.lower() or basin == "坤坤":
        pred = "HIGHEST"
    elif "乾" in basin.lower() or "qian" in basin.lower() or basin == "乾乾":
        pred = "LOWEST?"
    else:
        pred = ""
    
    print(f"{basin:<12s} {basin_hexcount[basin]:6d} {g:6d} {r:6d} {ratio:8.2f} {pred:>12s}")

print(f"\n{'Total':<12s} {sum(basin_hexcount.values()):6d} {total_gang:6d} {total_rou:6d} {total_gang/total_rou if total_rou>0 else 0:8.2f}")

# ═══════════════════════════════════════════════════════════════
# Test the prediction
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"PREDICTION TEST")
print(f"{'='*60}")

# Find which basin has highest and lowest ratio
if ratios:
    max_basin = max(ratios, key=ratios.get)
    min_basin = min(ratios, key=ratios.get)
    
    print(f"\n  Highest 剛/柔 ratio: {max_basin} ({ratios[max_basin]:.2f})")
    print(f"  Lowest 剛/柔 ratio:  {min_basin} ({ratios[min_basin]:.2f})")
    
    # Check prediction: Kun should be highest (established)
    # Qian should be lowest (prediction)
    kun_basins = [b for b in ratios if "坤" in b or "kun" in b.lower()]
    qian_basins = [b for b in ratios if "乾" in b or "qian" in b.lower()]
    
    if kun_basins:
        kun_is_highest = max_basin in kun_basins
        print(f"\n  Kun basin is highest? {'✓ YES' if kun_is_highest else '✗ NO'} ({max_basin}={ratios[max_basin]:.2f})")
    
    if qian_basins:
        qian_is_lowest = min_basin in qian_basins
        print(f"  Qian basin is lowest? {'✓ YES' if qian_is_lowest else '✗ NO'} ({min_basin}={ratios[min_basin]:.2f})")
        if qian_basins:
            qian_ratio = ratios[qian_basins[0]]
            print(f"  Qian ratio: {qian_ratio:.2f}")
    
    # Interpretation
    print(f"\n{'='*60}")
    print(f"INTERPRETATION")
    print(f"{'='*60}")
    
    if kun_basins and qian_basins:
        kun_r = ratios[kun_basins[0]]
        qian_r = ratios[qian_basins[0]]
        cycle_basins = [b for b in ratios if b not in kun_basins and b not in qian_basins]
        
        if cycle_basins:
            cycle_r = sum(ratios[b] * basin_hexcount[b] for b in cycle_basins) / sum(basin_hexcount[b] for b in cycle_basins)
            print(f"\n  Kun (mostly yin):   剛/柔 = {kun_r:.2f} — comments heavily on yang (unusual)")
            print(f"  Cycle (mixed):      剛/柔 ≈ {cycle_r:.2f} — balanced commentary")
            print(f"  Qian (mostly yang): 剛/柔 = {qian_r:.2f} — comments heavily on yin (unusual)")
            
            if kun_r > cycle_r > qian_r:
                print(f"\n  ✓ PERFECT MONOTONIC: Kun > Cycle > Qian")
                print(f"    The 彖傳 systematically comments on what's UNUSUAL in each basin.")
                print(f"    This is consistent with 彖傳 as 'anomaly detector'.")
            elif kun_r > qian_r:
                print(f"\n  ✓ CORRECT DIRECTION: Kun > Qian")
                print(f"    The 彖傳 comments more on yang in yin-heavy hexagrams,")
                print(f"    and more on yin in yang-heavy hexagrams.")
            else:
                print(f"\n  ✗ PREDICTION FAILS: Kun ({kun_r:.2f}) ≤ Qian ({qian_r:.2f})")

# ═══════════════════════════════════════════════════════════════
# Detailed: per-hexagram breakdown for top contributors
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*60}")
print(f"TOP CONTRIBUTORS (hexagrams with most 剛+柔 mentions)")
print(f"{'='*60}")

hex_details.sort(key=lambda x: x['gang'] + x['rou'], reverse=True)
print(f"\n{'KW':>4s} {'Name':<6s} {'Basin':<12s} {'Binary':<8s} {'剛':>4s} {'柔':>4s} {'Yang%':>6s}")
for h in hex_details[:20]:
    binary = h['binary']
    yang_pct = sum(int(b) for b in binary) / 6 * 100
    print(f"{h['kw']:4d} {h['name']:<6s} {h['basin']:<12s} {binary:<8s} {h['gang']:4d} {h['rou']:4d} {yang_pct:5.0f}%")

# Cross-check: yang percentage by basin
print(f"\n  Mean yang line percentage by basin:")
for basin in basin_order:
    yang_pcts = []
    for kw in kw_to_text:
        hv = kw_to_hexval[kw]
        if hexval_to_basin[hv] == basin:
            binary = atlas[str(hv)]["binary"]
            yang_pcts.append(sum(int(b) for b in binary) / 6)
    if yang_pcts:
        mean_yang = sum(yang_pcts) / len(yang_pcts) * 100
        print(f"    {basin}: {mean_yang:.1f}% yang lines")

print(f"\nDone.")
