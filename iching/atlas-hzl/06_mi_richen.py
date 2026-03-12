#!/usr/bin/env python3
"""
§III.4: MI(日辰 activation, 互 chain)

Tests whether 日辰 and 互 access independent information:
  MI(日辰 signature, 互 chain) — expected near-zero (shell ⊥ core)
  MI(日辰 signature, palace)  — expected nonzero (both shell-derived)
  MI(日辰 signature, basin)   — expected lower (basin is core-derived)
"""

import sys
import json
import math
from pathlib import Path
from collections import Counter, defaultdict
import importlib.util

HERE = Path(__file__).resolve().parent
PHASE4 = HERE.parent / "opposition-theory" / "phase4"
HZL = HERE.parent / "huozhulin"

sys.path.insert(0, str(PHASE4))
from cycle_algebra import (NUM_HEX, hugua, lower_trigram, upper_trigram,
                           TRIGRAM_ELEMENT, bit)

def _load(name, filepath):
    s = importlib.util.spec_from_file_location(name, filepath)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

p2 = _load("p2", HZL / "02_palace_kernel.py")
basin_fn = p2.basin

# ─── Constants ─────────────────────────────────────────────────────────────

BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
BRANCH_IDX = {b: i for i, b in enumerate(BRANCHES)}
BRANCH_ELEMENT = {
    "子": "Water", "丑": "Earth", "寅": "Wood", "卯": "Wood",
    "辰": "Earth", "巳": "Fire",  "午": "Fire",  "未": "Earth",
    "申": "Metal", "酉": "Metal", "戌": "Earth", "亥": "Water",
}

CHONG = {}
for i in range(6):
    CHONG[i] = i + 6
    CHONG[i + 6] = i

HE = {0: 1, 1: 0, 2: 11, 11: 2, 3: 10, 10: 3, 4: 9, 9: 4, 5: 8, 8: 5, 6: 7, 7: 6}

MU_BRANCH = {"Fire": 10, "Water": 4, "Wood": 7, "Metal": 1, "Earth": 4}


# ─── Feature extraction ───────────────────────────────────────────────────

def richen_signature(profile):
    """12-element tuple: for each 日辰 branch, frozenset of activated line positions.
    
    Activation = 沖 or 合 or 墓 between 日辰 branch and line branch.
    """
    branches = [BRANCH_IDX[l["branch"]] for l in profile["lines"]]
    elements = [l["element"] for l in profile["lines"]]

    sig = []
    for ri in range(12):
        activated = frozenset(
            pos + 1 for pos in range(6)
            if (CHONG.get(ri) == branches[pos]
                or HE.get(ri) == branches[pos]
                or MU_BRANCH[elements[pos]] == ri)
        )
        sig.append(activated)
    return tuple(sig)


def hu_chain(h):
    """互卦 element pair as categorical variable."""
    hu = hugua(h)
    lo_e = TRIGRAM_ELEMENT[lower_trigram(hu)]
    up_e = TRIGRAM_ELEMENT[upper_trigram(hu)]
    return (lo_e, up_e)


# ─── MI computation ──────────────────────────────────────────────────────

def mutual_information(xs, ys):
    """Compute MI(X, Y) in bits from two equal-length sequences of categorical values."""
    n = len(xs)
    assert n == len(ys)

    joint = Counter(zip(xs, ys))
    px = Counter(xs)
    py = Counter(ys)

    mi = 0.0
    for (x, y), nxy in joint.items():
        pxy = nxy / n
        mi += pxy * math.log2(pxy / (px[x] / n * py[y] / n))
    return mi


def entropy(xs):
    """Shannon entropy in bits."""
    n = len(xs)
    px = Counter(xs)
    return -sum((c / n) * math.log2(c / n) for c in px.values())


def normalized_mi(xs, ys):
    """MI / min(H(X), H(Y))."""
    mi = mutual_information(xs, ys)
    hx = entropy(xs)
    hy = entropy(ys)
    denom = min(hx, hy)
    return mi / denom if denom > 0 else 0.0


def shuffled_mi(xs, ys, trials=1000):
    """Shuffled baseline MI distribution."""
    import random
    ys_list = list(ys)
    mis = []
    for _ in range(trials):
        random.shuffle(ys_list)
        mis.append(mutual_information(xs, ys_list))
    return sum(mis) / len(mis), max(mis)


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    import random
    random.seed(42)

    profiles = json.loads((HERE / "hzl_profiles.json").read_text())
    print(f"Loaded {len(profiles)} profiles\n")

    # Build feature vectors for all 64 hexagrams
    sigs = []       # 日辰 activation signatures (categorical)
    hus = []        # 互 chain (categorical)
    palaces = []    # palace (categorical)
    basins = []     # basin (categorical)

    for p in profiles:
        h = p["hex_val"]
        sigs.append(richen_signature(p))
        hus.append(hu_chain(h))
        palaces.append(p["palace"])
        basins.append(basin_fn(h))

    # Entropies
    h_sig = entropy(sigs)
    h_hu = entropy(hus)
    h_pal = entropy(palaces)
    h_bas = entropy(basins)

    print("=" * 60)
    print("§III.4: MUTUAL INFORMATION ANALYSIS")
    print("=" * 60)

    print(f"\n  Feature entropies (bits):")
    print(f"    H(日辰 signature) = {h_sig:.3f}  ({len(set(sigs))} distinct values)")
    print(f"    H(互 chain)       = {h_hu:.3f}  ({len(set(hus))} distinct values)")
    print(f"    H(palace)         = {h_pal:.3f}  ({len(set(palaces))} distinct values)")
    print(f"    H(basin)          = {h_bas:.3f}  ({len(set(basins))} distinct values)")

    # Core computation: MI(sig, hu)
    mi_sig_hu = mutual_information(sigs, hus)
    nmi_sig_hu = normalized_mi(sigs, hus)
    avg_shuf, max_shuf = shuffled_mi(sigs, hus)

    print(f"\n  MI(日辰 sig, 互 chain):")
    print(f"    MI = {mi_sig_hu:.4f} bits")
    print(f"    NMI = {nmi_sig_hu:.4f}")
    print(f"    Shuffled baseline: avg={avg_shuf:.4f}, max={max_shuf:.4f}")
    sig_str = "NEAR-ZERO" if mi_sig_hu < max_shuf * 1.5 else "SIGNIFICANT"
    print(f"    → {sig_str} (shell ⊥ core {'confirmed' if sig_str == 'NEAR-ZERO' else 'NOT confirmed'})")

    # MI(sig, palace)
    mi_sig_pal = mutual_information(sigs, palaces)
    nmi_sig_pal = normalized_mi(sigs, palaces)
    avg_shuf_pal, max_shuf_pal = shuffled_mi(sigs, palaces)

    print(f"\n  MI(日辰 sig, palace):")
    print(f"    MI = {mi_sig_pal:.4f} bits")
    print(f"    NMI = {nmi_sig_pal:.4f}")
    print(f"    Shuffled baseline: avg={avg_shuf_pal:.4f}, max={max_shuf_pal:.4f}")
    sig_str2 = "SIGNIFICANT" if mi_sig_pal > max_shuf_pal * 1.5 else "NEAR-ZERO"
    print(f"    → {sig_str2}")

    # MI(sig, basin)
    mi_sig_bas = mutual_information(sigs, basins)
    nmi_sig_bas = normalized_mi(sigs, basins)
    avg_shuf_bas, max_shuf_bas = shuffled_mi(sigs, basins)

    print(f"\n  MI(日辰 sig, basin):")
    print(f"    MI = {mi_sig_bas:.4f} bits")
    print(f"    NMI = {nmi_sig_bas:.4f}")
    print(f"    Shuffled baseline: avg={avg_shuf_bas:.4f}, max={max_shuf_bas:.4f}")

    # Additional: MI(palace, hu) and MI(palace, basin) for reference
    mi_pal_hu = mutual_information(palaces, hus)
    mi_pal_bas = mutual_information(palaces, basins)
    mi_hu_bas = mutual_information(hus, basins)

    print(f"\n  Reference MI values:")
    print(f"    MI(palace, 互)    = {mi_pal_hu:.4f} bits")
    print(f"    MI(palace, basin) = {mi_pal_bas:.4f} bits")
    print(f"    MI(互, basin)     = {mi_hu_bas:.4f} bits")

    # Summary table
    print(f"\n  Summary:")
    print(f"  {'Pair':30s}  {'MI':>8}  {'NMI':>8}")
    print(f"  {'─'*30}  {'─'*8}  {'─'*8}")
    pairs = [
        ("日辰 sig × 互 chain", mi_sig_hu, nmi_sig_hu),
        ("日辰 sig × palace", mi_sig_pal, nmi_sig_pal),
        ("日辰 sig × basin", mi_sig_bas, nmi_sig_bas),
        ("palace × 互 chain", mi_pal_hu, normalized_mi(palaces, hus)),
        ("palace × basin", mi_pal_bas, normalized_mi(palaces, basins)),
        ("互 chain × basin", mi_hu_bas, normalized_mi(hus, basins)),
    ]
    for name, mi, nmi in pairs:
        print(f"  {name:30s}  {mi:>8.4f}  {nmi:>8.4f}")

    # Signature sharing analysis
    sig_groups = defaultdict(list)
    for i, s in enumerate(sigs):
        sig_groups[s].append(profiles[i]["hex_val"])
    shared = {k: v for k, v in sig_groups.items() if len(v) > 1}
    print(f"\n  日辰 signature sharing:")
    print(f"    Distinct signatures: {len(sig_groups)}/64")
    print(f"    Shared signatures: {len(shared)} groups")
    if shared:
        for sig, hexes in sorted(shared.items(), key=lambda x: -len(x[1]))[:5]:
            names = [p["name"] for p in profiles if p["hex_val"] in hexes]
            print(f"      {len(hexes)} hexagrams: {', '.join(names)}")


if __name__ == "__main__":
    main()
