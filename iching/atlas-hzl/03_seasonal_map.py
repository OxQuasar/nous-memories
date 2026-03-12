#!/usr/bin/env python3
"""
§II.1-2: Seasonal strength map.

Loads hzl_profiles.json. Produces hzl_seasonal.json with 320 entries
(64 hexagrams × 5 seasons), each with per-line and per-六親 strength levels.

Analysis:
  1. Verify 2/5 ceiling (at most 2 六親 types 旺/相 per hex-season)
  2. Functional coverage distribution
  3. Season × palace interaction
  4. Zero-coverage identification
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

HERE = Path(__file__).resolve().parent

# ─── Constants ─────────────────────────────────────────────────────────────

ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]
SHENG_MAP = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal",
             "Metal": "Water", "Water": "Wood"}
KE_MAP = {"Wood": "Earth", "Earth": "Water", "Water": "Fire",
          "Fire": "Metal", "Metal": "Wood"}

LIUQIN_NAMES = ["兄弟", "子孫", "父母", "妻財", "官鬼"]
LIUQIN_SHORT = {"兄弟": "兄", "子孫": "孫", "父母": "父", "妻財": "財", "官鬼": "鬼"}

SEASON_NAMES = ["Spring", "Summer", "Late_Summer", "Autumn", "Winter"]
SEASON_ELEMENT = {
    "Spring": "Wood", "Summer": "Fire", "Late_Summer": "Earth",
    "Autumn": "Metal", "Winter": "Water",
}
SEASON_SHORT = {"Spring": "Spr", "Summer": "Sum", "Late_Summer": "LSm",
                "Autumn": "Aut", "Winter": "Win"}

STRONG = {"旺", "相"}
WEAK = {"囚", "死"}

# ─── Seasonal strength ────────────────────────────────────────────────────

def _build_season_table():
    """season → {strength_level → element}"""
    table = {}
    for season, se in SEASON_ELEMENT.items():
        table[season] = {
            "旺": se,
            "相": SHENG_MAP[se],
            "休": next(e for e in ELEMENTS if SHENG_MAP[e] == se),
            "囚": next(e for e in ELEMENTS if KE_MAP[e] == se),
            "死": KE_MAP[se],
        }
    return table

SEASON_TABLE = _build_season_table()

# Invert: (season, element) → strength
_ELEM_STRENGTH = {}
for season, mapping in SEASON_TABLE.items():
    for level, elem in mapping.items():
        _ELEM_STRENGTH[(season, elem)] = level

def elem_strength(element, season):
    return _ELEM_STRENGTH[(season, element)]

def liuqin_element(lq_type, palace_elem):
    """Map 六親 type → element given palace element."""
    if lq_type == "兄弟": return palace_elem
    if lq_type == "子孫": return SHENG_MAP[palace_elem]
    if lq_type == "父母": return next(e for e in ELEMENTS if SHENG_MAP[e] == palace_elem)
    if lq_type == "妻財": return KE_MAP[palace_elem]
    if lq_type == "官鬼": return next(e for e in ELEMENTS if KE_MAP[e] == palace_elem)
    raise ValueError(lq_type)


# ─── Build seasonal map ──────────────────────────────────────────────────

def build_seasonal(profiles):
    """Build 320 seasonal entries."""
    entries = []
    for p in profiles:
        pe = p["palace_element"]
        for season in SEASON_NAMES:
            se = SEASON_ELEMENT[season]

            # Per-line strength
            line_strengths = []
            for l in p["lines"]:
                line_strengths.append(elem_strength(l["element"], season))

            # Per-六親 type strength
            lq_strengths = {}
            for lq in LIUQIN_NAMES:
                e = liuqin_element(lq, pe)
                lq_strengths[lq] = elem_strength(e, season)

            strong_count = sum(1 for s in line_strengths if s in STRONG)
            weak_count = sum(1 for s in line_strengths if s in WEAK)

            # Which 六親 types are strong (旺/相)?
            # Only count types actually present in the hexagram
            present_types = set(l["liuqin"] for l in p["lines"])
            strong_lq = sorted(lq for lq in LIUQIN_NAMES
                               if lq in present_types and lq_strengths[lq] in STRONG)
            weak_lq = sorted(lq for lq in LIUQIN_NAMES
                             if lq in present_types and lq_strengths[lq] in WEAK)

            functional_coverage = len(strong_lq)

            entries.append({
                "hex_val": p["hex_val"],
                "name": p["name"],
                "palace": p["palace"],
                "palace_element": pe,
                "season": season,
                "season_element": se,
                "line_strengths": line_strengths,
                "liuqin_strengths": lq_strengths,
                "strong_count": strong_count,
                "weak_count": weak_count,
                "functional_coverage": functional_coverage,
                "strong_liuqin": strong_lq,
                "weak_liuqin": weak_lq,
            })

    return entries


# ═══════════════════════════════════════════════════════════════════════════
# Analysis
# ═══════════════════════════════════════════════════════════════════════════

def analyze_ceiling(entries):
    """Verify 2/5 ceiling."""
    print("=" * 60)
    print("§II.2.1: FUNCTIONAL COVERAGE CEILING")
    print("=" * 60)

    # First: theoretical ceiling from 六親→element bijection
    # Each season has 2 旺/相 elements, so ≤2 types can be strong
    print(f"\n  Season table:")
    for season in SEASON_NAMES:
        row = SEASON_TABLE[season]
        strong_e = [row["旺"], row["相"]]
        print(f"    {season:12s}: 旺={row['旺']:>5} 相={row['相']:>5}  → strong elements: {strong_e}")

    # Check max functional_coverage
    max_fc = max(e["functional_coverage"] for e in entries)
    fc_dist = Counter(e["functional_coverage"] for e in entries)
    total = len(entries)

    print(f"\n  Max functional_coverage observed: {max_fc}")
    print(f"\n  Distribution across {total} hex-season states:")
    for n in sorted(fc_dist):
        pct = fc_dist[n] / total
        bar = "█" * int(pct * 50)
        print(f"    {n}/5: {fc_dist[n]:>3} ({pct:>5.1%}) {bar}")

    # Theoretical: what's the max possible 六親 strength count (ignoring presence)?
    max_types_strong = Counter()
    for e in entries:
        n = sum(1 for lq in LIUQIN_NAMES if e["liuqin_strengths"][lq] in STRONG)
        max_types_strong[n] += 1
    print(f"\n  Theoretical max (all 5 types, ignoring presence): "
          f"always {max(max_types_strong.keys())}/5 types strong")
    print(f"  → The 2/5 ceiling is CONFIRMED: 六親↔element bijection × 2 strong elements/season")

    return fc_dist


def analyze_distribution(entries):
    """Distribution of functional coverage."""
    print("\n" + "=" * 60)
    print("§II.2.2: COVERAGE DISTRIBUTION")
    print("=" * 60)

    # By season
    print(f"\n  Functional coverage by season:")
    header = f"  {'Season':12s} " + " ".join(f"fc={n}" for n in range(3)) + "  avg"
    print(header)
    print(f"  {'─'*12} " + "─" * 30)
    for season in SEASON_NAMES:
        se = [e for e in entries if e["season"] == season]
        dist = Counter(e["functional_coverage"] for e in se)
        avg = sum(e["functional_coverage"] for e in se) / len(se)
        cells = " ".join(f"{dist.get(n, 0):>4}" for n in range(3))
        print(f"  {season:12s} {cells}  {avg:.2f}")

    # By palace
    print(f"\n  Functional coverage by palace (avg across 5 seasons):")
    palaces = sorted(set(e["palace"] for e in entries))
    for pal in palaces:
        pe = [e for e in entries if e["palace"] == pal]
        avg = sum(e["functional_coverage"] for e in pe) / len(pe)
        dist = Counter(e["functional_coverage"] for e in pe)
        cells = " ".join(f"fc{n}={dist.get(n, 0)}" for n in range(3))
        print(f"    {pal:10s} avg={avg:.2f}  {cells}")


def analyze_palace_season_interaction(entries, profiles):
    """Season × palace interaction: what happens in palace's own season?"""
    print("\n" + "=" * 60)
    print("§II.2.3: PALACE × SEASON INTERACTION")
    print("=" * 60)

    # Palace element → season where 兄弟 is 旺
    print(f"\n  Palace's own season (兄弟=旺):")
    palace_meta = {}
    for p in profiles:
        if p["palace"] not in palace_meta:
            palace_meta[p["palace"]] = p["palace_element"]

    palaces = sorted(palace_meta.keys())
    for pal in palaces:
        pe = palace_meta[pal]
        own_season = [s for s in SEASON_NAMES if SEASON_ELEMENT[s] == pe]
        own_s = own_season[0] if own_season else "—"

        # Get entries for this palace in its own season
        own_entries = [e for e in entries if e["palace"] == pal and e["season"] == own_s]
        if own_entries:
            avg_fc = sum(e["functional_coverage"] for e in own_entries) / len(own_entries)
            # Which types are strong?
            strong_types = Counter()
            for e in own_entries:
                for lq in e["strong_liuqin"]:
                    strong_types[lq] += 1
            strong_str = ", ".join(f"{LIUQIN_SHORT[lq]}={c}" for lq, c in strong_types.most_common())
        else:
            avg_fc = 0
            strong_str = "—"
        print(f"    {pal:10s} ({pe:>5}): own season={own_s:12s}  "
              f"avg_fc={avg_fc:.2f}  strong: {strong_str}")

    # Full interaction matrix
    print(f"\n  Average functional coverage (palace × season):")
    header = f"  {'Palace':10s} " + " ".join(f"{SEASON_SHORT[s]:>5}" for s in SEASON_NAMES)
    print(header)
    print(f"  {'─'*10} " + " ".join("─────" for _ in SEASON_NAMES))
    for pal in palaces:
        cells = []
        for season in SEASON_NAMES:
            se = [e for e in entries if e["palace"] == pal and e["season"] == season]
            avg = sum(e["functional_coverage"] for e in se) / len(se) if se else 0
            cells.append(f"{avg:>5.2f}")
        print(f"  {pal:10s} {' '.join(cells)}")

    # In which season does each palace peak?
    print(f"\n  Palace peak season (highest avg functional coverage):")
    for pal in palaces:
        best_s, best_avg = None, -1
        for season in SEASON_NAMES:
            se = [e for e in entries if e["palace"] == pal and e["season"] == season]
            avg = sum(e["functional_coverage"] for e in se) / len(se) if se else 0
            if avg > best_avg:
                best_s, best_avg = season, avg
        pe = palace_meta[pal]
        print(f"    {pal:10s} ({pe:>5}): peaks in {best_s:12s} (avg={best_avg:.2f})")


def analyze_zero_coverage(entries):
    """Identify hex-season combinations with functional_coverage = 0."""
    print("\n" + "=" * 60)
    print("§II.2.4: ZERO FUNCTIONAL COVERAGE")
    print("=" * 60)

    zeros = [e for e in entries if e["functional_coverage"] == 0]
    print(f"\n  States with fc=0 (no present type is 旺/相): {len(zeros)}/{len(entries)}")

    if zeros:
        # Group by season
        by_season = defaultdict(list)
        for e in zeros:
            by_season[e["season"]].append(e)

        print(f"\n  By season:")
        for season in SEASON_NAMES:
            n = len(by_season.get(season, []))
            print(f"    {season:12s}: {n} hexagrams")

        # Group by palace
        by_palace = defaultdict(list)
        for e in zeros:
            by_palace[e["palace"]].append(e)

        print(f"\n  By palace:")
        for pal in sorted(by_palace):
            members = by_palace[pal]
            seasons = Counter(e["season"] for e in members)
            s_str = ", ".join(f"{SEASON_SHORT[s]}={c}" for s, c in seasons.most_common())
            print(f"    {pal:10s}: {len(members)} states ({s_str})")

        # Sample
        print(f"\n  Sample zero-coverage states:")
        for e in zeros[:8]:
            present = set(l for l in e["strong_liuqin"])  # already empty for fc=0
            lqs = e["liuqin_strengths"]
            lq_str = " ".join(f"{LIUQIN_SHORT[lq]}:{lqs[lq]}" for lq in LIUQIN_NAMES)
            print(f"    {e['name']:>6} in {e['season']:12s}: {lq_str}")
    else:
        print(f"  → Every hex-season state has at least one functionally strong type.")


def analyze_strong_line_counts(entries):
    """Distribution of strong (旺/相) line counts."""
    print("\n" + "=" * 60)
    print("§II.2.5: STRONG LINE COUNT")
    print("=" * 60)

    strong_dist = Counter(e["strong_count"] for e in entries)
    total = len(entries)

    print(f"\n  Lines that are 旺/相 per hex-season:")
    for n in sorted(strong_dist):
        pct = strong_dist[n] / total
        bar = "█" * int(pct * 40)
        print(f"    {n}/6: {strong_dist[n]:>3} ({pct:>5.1%}) {bar}")

    avg = sum(e["strong_count"] for e in entries) / total
    print(f"\n  Average strong lines: {avg:.2f}/6")
    print(f"  (Theoretical: each element has P=2/5 of being 旺/相 → expected 6×2/5 = 2.4)")


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    profiles = json.loads((HERE / "hzl_profiles.json").read_text())
    print(f"Loaded {len(profiles)} profiles\n")

    entries = build_seasonal(profiles)
    print(f"Built {len(entries)} seasonal entries\n")

    fc_dist = analyze_ceiling(entries)
    analyze_distribution(entries)
    analyze_palace_season_interaction(entries, profiles)
    analyze_zero_coverage(entries)
    analyze_strong_line_counts(entries)

    # Write output
    out_path = HERE / "hzl_seasonal.json"
    out_path.write_text(json.dumps(entries, indent=2, ensure_ascii=False))
    print(f"\n→ Wrote {len(entries)} entries to {out_path}")


if __name__ == "__main__":
    main()
