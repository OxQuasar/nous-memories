#!/usr/bin/env python3
"""
Probe 3: 用神 Projection — Where Meaning Enters

The 用神 mapping assigns each worldly question domain to a primary 六親 type.
This probe investigates how that mapping interacts with the structural
incompleteness of palaces, the seasonal system, and the diagnostic triad
(用神, auxiliary, 忌神).
"""

import sys
from pathlib import Path
from collections import Counter, defaultdict
import importlib.util

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "opposition-theory" / "phase4"))
from cycle_algebra import (
    NUM_HEX, TRIGRAM_NAMES, TRIGRAM_ELEMENT, ELEMENTS,
    SHENG_MAP, KE_MAP, lower_trigram,
)

def _load(name, filename):
    s = importlib.util.spec_from_file_location(
        name, Path(__file__).resolve().parent.parent / "huozhulin" / filename)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m

p1 = _load('p1', '01_najia_map.py')
p2 = _load('p2', '02_palace_kernel.py')
p3 = _load('p3', '03_liuqin.py')
p6 = _load('p6', '06_seasonal.py')

liuqin_word = p3.liuqin_word
LIUQIN_NAMES = p3.LIUQIN_NAMES
LIUQIN_SHORT = p3.LIUQIN_SHORT
short_word = p3.short_word
generate_palaces = p2.generate_palaces
SEASON_NAMES = p6.SEASON_NAMES
elem_strength = p6.elem_strength
type_to_elem = p6.type_to_elem
STRONG = p6.STRONG

BRANCH_ELEMENT = p1.BRANCH_ELEMENT

# ─── 用神 Mapping ──────────────────────────────────────────────────────────

YONGSHEN_MAP = {
    "illness": "官鬼", "ghosts": "官鬼", "thieves": "官鬼",
    "lawsuits": "官鬼", "examinations": "官鬼", "seeking_husband": "官鬼",
    "meeting_nobles": "官鬼", "enemies_war": "官鬼",
    "seeking_wealth": "妻財", "trade": "妻財", "seeking_wife": "妻財",
    "travel": "妻財", "lost_items": "妻財", "farming": "妻財", "household": "妻財",
    "gambling": "子孫", "medicine": "子孫", "our_army": "子孫", "livestock": "子孫",
    "documents": "父母", "housing": "父母", "graves_structure": "父母",
}

DOMAIN_COUNT = {"官鬼": 8, "妻財": 7, "子孫": 4, "父母": 3, "兄弟": 0}

# ─── 六親 Cycle (on 生 cycle) ──────────────────────────────────────────────
# The 六親 follow the 生 cycle: 父母→兄弟→子孫→妻財→官鬼→父母
# Because each type's element is derived from the 生/克 relation to palace element.

LIUQIN_SHENG = {
    "父母": "兄弟", "兄弟": "子孫", "子孫": "妻財",
    "妻財": "官鬼", "官鬼": "父母",
}
LIUQIN_KE = {
    "父母": "妻財", "妻財": "子孫", "子孫": "官鬼",
    "官鬼": "兄弟", "兄弟": "父母",
}

def auxiliary(yongshen):
    """σ⁻¹(用神): what generates the 用神 on the 六親 cycle."""
    for k, v in LIUQIN_SHENG.items():
        if v == yongshen:
            return k
    raise ValueError(yongshen)

def jishen(yongshen):
    """忌神: what 克s the 用神 on the 六親 cycle."""
    for k, v in LIUQIN_KE.items():
        if v == yongshen:
            return k
    raise ValueError(yongshen)


# ═══════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════

def build_data():
    _, hex_info = generate_palaces()
    records = []
    for h in range(NUM_HEX):
        info = hex_info[h]
        pe = info['palace_elem']
        word = liuqin_word(h, pe)
        present = set(word)
        missing = set(LIUQIN_NAMES) - present
        t2e = type_to_elem(pe)
        records.append({
            'hex': h, 'palace': info['palace'], 'palace_elem': pe,
            'rank': info['rank'], 'word': word,
            'present': present, 'missing': missing,
            'type_to_elem': t2e,
        })
    return records, hex_info


# ═══════════════════════════════════════════════════════════════════════════
# A. The Querrent's Position
# ═══════════════════════════════════════════════════════════════════════════

def section_a():
    lines = []
    w = lines.append

    w("## A. The Querrent's Position on the 六親 Cycle\n")

    # Show the full 六親 cycle
    w("### The 六親 生 cycle\n")
    w("```")
    w("父母 →生→ 兄弟 →生→ 子孫 →生→ 妻財 →生→ 官鬼 →生→ 父母")
    w("```\n")

    w("### The triad for each 用神 type\n")
    w("| 用神 | Domains | Auxiliary (σ⁻¹) | 忌神 (what 克s 用) |")
    w("|------|---------|-----------------|------------------|")
    for lq in LIUQIN_NAMES:
        aux = auxiliary(lq)
        ji = jishen(lq)
        dc = DOMAIN_COUNT[lq]
        w(f"| {lq} | {dc} | {aux} | {ji} |")
    w("")

    # Querrent's position
    w("### 兄弟 (self) on the 克 cycle\n")
    w("```")
    w("克 cycle: 官鬼 →克→ 兄弟 →克→ 父母 →克→ 妻財 →克→ 子孫 →克→ 官鬼")
    w("```\n")
    w("The querrent (兄弟) is:")
    w("- **克ed by 官鬼** (external authority constrains the self)")
    w("- **克s 父母** (self disrupts structure? — note: this is less intuitive)")
    w("- **克s 妻財** (self depletes resources — '破財之人')\n")

    # The structural exclusion
    w("### Why 兄弟 is never 用神\n")
    w("兄弟 has 0 domains. The text says: '破財之人，不為主、不為輔'")
    w("('The one who depletes wealth is neither master nor support').\n")
    w("The querrent (兄弟 = same element as palace) is the **reference frame**,")
    w("not the object of inquiry. You don't divine about yourself; you divine about")
    w("what acts on you (官鬼), what you seek (妻財), what you tend (子孫),")
    w("what shelters you (父母).\n")

    w("### Geometric claim: 兄弟 sits between the two heaviest 用神\n")
    w("On the 克 cycle: 官鬼 →克→ **兄弟** →克→ … →克→ 妻財")
    w("")
    # Check: what is the 克-distance from 官鬼 to 兄弟 and 兄弟 to 妻財?
    ke_cycle = ["官鬼", "兄弟", "父母", "妻財", "子孫"]
    w("克 cycle order: " + " → ".join(ke_cycle))
    idx_guan = ke_cycle.index("官鬼")
    idx_xiong = ke_cycle.index("兄弟")
    idx_cai = ke_cycle.index("妻財")
    w(f"- 官鬼 to 兄弟: {(idx_xiong - idx_guan) % 5} step(s) on 克 cycle")
    w(f"- 兄弟 to 妻財: {(idx_cai - idx_xiong) % 5} step(s) on 克 cycle")
    w(f"- 官鬼 ({DOMAIN_COUNT['官鬼']} domains) + 妻財 ({DOMAIN_COUNT['妻財']} domains) "
      f"= {DOMAIN_COUNT['官鬼'] + DOMAIN_COUNT['妻財']} of {sum(DOMAIN_COUNT.values())} total domains")
    w("")
    w("**兄弟 is one 克-step from the heaviest node (官鬼, 8 domains) and two steps")
    w("from the second heaviest (妻財, 7 domains).** Together, 官 and 財 account for")
    w(f"{DOMAIN_COUNT['官鬼'] + DOMAIN_COUNT['妻財']}/{sum(DOMAIN_COUNT.values())} "
      f"= {(DOMAIN_COUNT['官鬼'] + DOMAIN_COUNT['妻財'])/sum(DOMAIN_COUNT.values()):.0%} of all domains.\n")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# B. Signal/Noise Statistics per Palace
# ═══════════════════════════════════════════════════════════════════════════

def section_b(records):
    lines = []
    w = lines.append

    w("## B. Signal/Noise Statistics per Palace\n")

    # Group records by palace
    by_palace = defaultdict(list)
    for r in records:
        by_palace[r['palace']].append(r)

    palace_order = []
    for root in p2.PALACE_ROOTS:
        trig = lower_trigram(root)
        palace_order.append(TRIGRAM_NAMES[trig])

    # For each 用神 type, compute stats across all hexagrams
    w("### Per-palace signal lines for each 用神 type\n")

    for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
        aux_type = auxiliary(ys_type)
        ji_type = jishen(ys_type)
        w(f"#### 用神 = {ys_type} (auxiliary={aux_type}, 忌神={ji_type})\n")
        w("| Palace | Element | Signal | Support | Threat | 用神 missing? |")
        w("|--------|---------|--------|---------|--------|--------------|")
        for palace in palace_order:
            recs = by_palace[palace]
            pe = recs[0]['palace_elem']
            # Average across 8 hexagrams in palace
            signal_total = sum(r['word'].count(ys_type) for r in recs)
            support_total = sum(r['word'].count(aux_type) for r in recs)
            threat_total = sum(r['word'].count(ji_type) for r in recs)
            n_missing = sum(1 for r in recs if ys_type in r['missing'])
            w(f"| {palace} | {pe} | {signal_total/8:.1f} | {support_total/8:.1f} | "
              f"{threat_total/8:.1f} | {n_missing}/8 |")
        w("")

    # Coverage: fraction of 64 hexagrams with at least 1 signal line
    w("### Coverage: fraction of hexagrams with ≥1 signal line\n")
    w("| 用神 type | Hexagrams with ≥1 | Hexagrams with 0 (blind) | Coverage |")
    w("|----------|-------------------|--------------------------|----------|")
    for ys_type in LIUQIN_NAMES:
        has_signal = sum(1 for r in records if ys_type in r['present'])
        blind = 64 - has_signal
        w(f"| {ys_type} | {has_signal} | {blind} | {has_signal/64:.1%} |")
    w("")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# C. Interaction with Incompleteness
# ═══════════════════════════════════════════════════════════════════════════

def section_c(records):
    lines = []
    w = lines.append

    w("## C. Interaction with Incompleteness\n")

    # Palace-level missing types (from root hexagram, rank 0)
    palace_missing = {}
    for r in records:
        if r['rank'] == 0:
            if r['missing']:
                palace_missing[r['palace']] = r['missing']

    w("### Missing types by palace (root hexagram)\n")
    w("| Palace | Element | Missing types | Domains affected |")
    w("|--------|---------|---------------|------------------|")
    total_darkness = {}
    for root in p2.PALACE_ROOTS:
        trig = lower_trigram(root)
        palace = TRIGRAM_NAMES[trig]
        pe = TRIGRAM_ELEMENT[trig]
        missing = palace_missing.get(palace, set())
        dark = sum(DOMAIN_COUNT[m] for m in missing)
        total_darkness[palace] = dark
        miss_str = ", ".join(sorted(missing)) if missing else "—"
        w(f"| {palace} | {pe} | {miss_str} | {dark} |")
    w("")

    # Structural darkness per palace
    w("### Structural darkness (domains structurally unreadable)\n")
    w("| Palace | Missing types | Domain count | Fraction of 22 |")
    w("|--------|---------------|-------------|----------------|")
    total_domains = sum(DOMAIN_COUNT.values())
    for root in p2.PALACE_ROOTS:
        trig = lower_trigram(root)
        palace = TRIGRAM_NAMES[trig]
        missing = palace_missing.get(palace, set())
        dark = total_darkness[palace]
        miss_str = ", ".join(f"{m}({DOMAIN_COUNT[m]})" for m in sorted(missing)) if missing else "—"
        w(f"| {palace} | {miss_str} | {dark}/{total_domains} | "
          f"{dark/total_domains:.0%} |")
    w("")

    # Is 兄弟's absence benign?
    w("### Is 兄弟's absence benign?\n")
    xiong_missing_palaces = [p for p, m in palace_missing.items() if "兄弟" in m]
    w(f"兄弟 is missing in {len(xiong_missing_palaces)} palaces: "
      f"{', '.join(xiong_missing_palaces)}")
    w(f"But DOMAIN_COUNT['兄弟'] = 0, so its absence adds 0 to structural darkness.\n")
    w("**兄弟's absence is structurally benign.** It is the only type whose absence")
    w("never blocks a question domain. When paired with a non-benign type,")
    w("the palace has darkness from only the other missing type.\n")

    # When 兄弟 is one of two missing: what's the other?
    w("### Paired missing types\n")
    w("| Palace | Missing pair | Darkness from pair |")
    w("|--------|-------------|-------------------|")
    for root in p2.PALACE_ROOTS:
        trig = lower_trigram(root)
        palace = TRIGRAM_NAMES[trig]
        missing = palace_missing.get(palace, set())
        if len(missing) == 2:
            pair = sorted(missing)
            dark = sum(DOMAIN_COUNT[m] for m in missing)
            w(f"| {palace} | {pair[0]} + {pair[1]} | {dark} |")
    w("")

    # Cross-hexagram: actual incompleteness (not just root)
    w("### Across all hexagrams: missing type × domain impact\n")
    type_miss_count = Counter()
    for r in records:
        for m in r['missing']:
            type_miss_count[m] += 1

    w("| Missing type | Hexagrams missing it | Domain weight | Weighted impact |")
    w("|-------------|---------------------|---------------|-----------------|")
    for lq in LIUQIN_NAMES:
        n = type_miss_count[lq]
        dc = DOMAIN_COUNT[lq]
        w(f"| {lq} | {n}/64 | {dc} | {n * dc} |")
    w("")
    w("Weighted impact = (hexagrams missing) × (domains affected). Higher = more")
    w("question-domain-hexagram combinations that are structurally blind.\n")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# D. The Practitioner's Navigation Space
# ═══════════════════════════════════════════════════════════════════════════

def section_d(records):
    lines = []
    w = lines.append

    w("## D. The Practitioner's Navigation Space (Readability Matrix)\n")

    w("### Global readability: 用神 type × season\n")
    w("For each (用神 type, season): is the 用神's element 旺 or 相?\n")
    w("This depends on the palace (which determines 六親→element mapping).\n")

    # Per-palace readability matrices
    palace_order = []
    for root in p2.PALACE_ROOTS:
        trig = lower_trigram(root)
        palace_order.append((TRIGRAM_NAMES[trig], TRIGRAM_ELEMENT[trig]))

    # Aggregate: for each (用神_type, season), count how many palaces have it 旺/相
    w("### Aggregate: palaces where 用神's element is 旺/相\n")
    w("| 用神 type | " + " | ".join(SEASON_NAMES) + " |")
    w("|----------|----|----|----|----|----|")
    for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
        row = []
        for season in SEASON_NAMES:
            count = 0
            for palace, pe in palace_order:
                t2e = type_to_elem(pe)
                elem = t2e[ys_type]
                s = elem_strength(elem, season)
                if s in STRONG:
                    count += 1
            row.append(f"{count}/8")
        w(f"| {ys_type} | " + " | ".join(row) + " |")
    w("")

    # Per-palace detail: peak and dead seasons
    w("### Per-palace: peak and dead seasons for each 用神\n")
    w("| Palace | Element | 用神 | Peak seasons (旺/相) | Dead seasons (囚/死) |")
    w("|--------|---------|------|---------------------|---------------------|")
    for palace, pe in palace_order:
        t2e = type_to_elem(pe)
        for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
            elem = t2e[ys_type]
            peaks = [s for s in SEASON_NAMES if elem_strength(elem, s) in STRONG]
            deads = [s for s in SEASON_NAMES if elem_strength(elem, s) in {'囚', '死'}]
            w(f"| {palace} | {pe} | {ys_type}({elem}) | "
              f"{', '.join(peaks)} | {', '.join(deads)} |")
    w("")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# E. Shadow Hit Probability
# ═══════════════════════════════════════════════════════════════════════════

def section_e(records):
    lines = []
    w = lines.append

    w("## E. Shadow Hit Probability\n")
    w("The seasonal system assigns 5 strength levels to 5 elements.")
    w("In each season, exactly 1 element is 囚 and 1 is 死 — two 'suppressed' elements.")
    w("If the 用神's element happens to be 囚 or 死, the reading is temporally disadvantaged.\n")

    # For each (用神, palace, season): is the 用神 element suppressed (囚/死)?
    WEAK = {'囚', '死'}
    shadow_hits = Counter()  # (ys_type) → count of (palace, season) where suppressed
    total_contexts = 0

    palace_order = []
    for root in p2.PALACE_ROOTS:
        trig = lower_trigram(root)
        palace_order.append((TRIGRAM_NAMES[trig], TRIGRAM_ELEMENT[trig]))

    for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
        for palace, pe in palace_order:
            t2e = type_to_elem(pe)
            elem = t2e[ys_type]
            for season in SEASON_NAMES:
                total_contexts += 1
                s = elem_strength(elem, season)
                if s in WEAK:
                    shadow_hits[ys_type] += 1

    total_per_type = len(palace_order) * len(SEASON_NAMES)

    w("### Suppression rate by 用神 type\n")
    w("| 用神 type | Suppressed contexts | Total contexts | Rate |")
    w("|----------|--------------------:|:--------------:|------|")
    for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
        n = shadow_hits[ys_type]
        w(f"| {ys_type} | {n} | {total_per_type} | {n/total_per_type:.0%} |")
    w("")

    w("Each element is 囚 in one season and 死 in one season → suppressed in 2/5 seasons.")
    w("Since 六親→element is a bijection per palace, each 用神 type is suppressed in exactly")
    w(f"2/5 = 40% of season-contexts. The rate is **uniform across 用神 types and palaces.**\n")

    # Day-branch shadow: does the day branch's element happen to 克 the 用神's element?
    w("### Day-branch shadow (克 from daily element)\n")
    w("For each (用神, palace, day-element): does the day element 克 the 用神's element?\n")

    day_ke_hits = Counter()
    day_total = 0
    for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
        for palace, pe in palace_order:
            t2e = type_to_elem(pe)
            ys_elem = t2e[ys_type]
            for day_elem in ELEMENTS:
                day_total += 1
                if KE_MAP[day_elem] == ys_elem:
                    day_ke_hits[ys_type] += 1

    day_total_per_type = len(palace_order) * len(ELEMENTS)
    w("| 用神 type | Day-克 contexts | Total | Rate |")
    w("|----------|:--------------:|:-----:|------|")
    for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
        n = day_ke_hits[ys_type]
        w(f"| {ys_type} | {n} | {day_total_per_type} | {n/day_total_per_type:.0%} |")
    w("")
    w("Each element is 克ed by exactly 1 of 5 elements → 1/5 = 20% of day-element contexts.")
    w("Again **uniform.** The 五行 cycle's symmetry ensures no 用神 type is systematically")
    w("more vulnerable to temporal suppression than any other.\n")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# F. The Triad as Diagnostic Unit
# ═══════════════════════════════════════════════════════════════════════════

def section_f(records):
    lines = []
    w = lines.append

    w("## F. The Triad as Diagnostic Unit\n")
    w("For each hexagram and each 用神 type, classify the diagnostic environment:\n")
    w("- **Full**: signal + support + 忌神 all present → complete reading")
    w("- **Blind**: signal (用神) missing → structural impossibility")
    w("- **Unsupported**: signal present but support (auxiliary) missing → partial")
    w("- **Unguarded**: signal present but 忌神 missing → can't assess threats")
    w("- **Exposed**: signal present, 忌神 present, but support missing → vulnerable\n")

    # Classify every (hexagram, 用神) pair
    categories = Counter()
    by_type = defaultdict(Counter)
    by_palace = defaultdict(Counter)

    for r in records:
        for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
            aux_type = auxiliary(ys_type)
            ji_type = jishen(ys_type)

            has_signal = ys_type in r['present']
            has_support = aux_type in r['present']
            has_threat = ji_type in r['present']

            if not has_signal:
                cat = "Blind"
            elif has_support and has_threat:
                cat = "Full"
            elif not has_support and has_threat:
                cat = "Exposed"
            elif has_support and not has_threat:
                cat = "Unguarded"
            else:  # signal only, no support no threat
                cat = "Isolated"

            categories[cat] += 1
            by_type[ys_type][cat] += 1
            by_palace[r['palace']][cat] += 1

    total = sum(categories.values())  # 64 hex × 4 用神 types = 256

    w("### Distribution across (hexagram × 用神 type) space\n")
    w(f"Total diagnostic contexts: {total} (64 hexagrams × 4 用神 types)\n")
    cat_order = ["Full", "Exposed", "Unguarded", "Isolated", "Blind"]
    w("| Category | Count | Fraction | Interpretation |")
    w("|----------|------:|----------|----------------|")
    interp = {
        "Full": "Complete diagnostic — all three triad members present",
        "Exposed": "Vulnerable — threat present but no support",
        "Unguarded": "Partial — support present but threat invisible",
        "Isolated": "Signal only — no context for interpretation",
        "Blind": "Structural impossibility — cannot read this question",
    }
    for cat in cat_order:
        n = categories.get(cat, 0)
        w(f"| {cat} | {n} | {n/total:.1%} | {interp[cat]} |")
    w("")

    w("### By 用神 type\n")
    w("| 用神 | " + " | ".join(cat_order) + " |")
    w("|------|----|---------|-----------|----------|-------|")
    for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
        row = [str(by_type[ys_type].get(cat, 0)) for cat in cat_order]
        w(f"| {ys_type} | " + " | ".join(row) + " |")
    w("")

    w("### By palace\n")
    palace_order = []
    for root in p2.PALACE_ROOTS:
        trig = lower_trigram(root)
        palace_order.append(TRIGRAM_NAMES[trig])

    w("| Palace | " + " | ".join(cat_order) + " |")
    w("|--------|----|---------|-----------|----------|-------|")
    for palace in palace_order:
        row = [str(by_palace[palace].get(cat, 0)) for cat in cat_order]
        w(f"| {palace} | " + " | ".join(row) + " |")
    w("")

    # Weighted by domain count
    w("### Domain-weighted blindness\n")
    w("Weight each Blind context by its 用神's domain count.\n")
    w("| 用神 | Blind hexagrams | Domain weight | Weighted blindness |")
    w("|------|:--------------:|:-------------:|:-----------------:|")
    total_weighted = 0
    for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
        n_blind = by_type[ys_type].get("Blind", 0)
        dc = DOMAIN_COUNT[ys_type]
        weighted = n_blind * dc
        total_weighted += weighted
        w(f"| {ys_type} | {n_blind} | {dc} | {weighted} |")
    max_weighted = 64 * sum(DOMAIN_COUNT[t] for t in ["官鬼", "妻財", "子孫", "父母"])
    w(f"\nTotal weighted blindness: {total_weighted} / {max_weighted} possible "
      f"= {total_weighted/max_weighted:.1%}\n")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# Synthesis
# ═══════════════════════════════════════════════════════════════════════════

def synthesis(records):
    lines = []
    w = lines.append

    w("## Synthesis\n")

    w("### The asymmetry is in the question space, not the structural space\n")
    w("The 五行 cycle's symmetry ensures uniform temporal treatment: every 用神 type is")
    w("suppressed in exactly 2/5 of seasonal contexts, 克ed by 1/5 of daily elements.")
    w("The structural incompleteness (6/8 palaces lack 2 六親 types) is also symmetric")
    w("at the type level — each type is missing from roughly the same number of hexagrams.\n")
    w("The asymmetry enters through the 用神 mapping: 官鬼 covers 8 domains, 妻財 covers 7,")
    w("while 子孫 covers 4 and 父母 only 3. This means the *practical impact* of structural")
    w("blindness is concentrated: when 官鬼 is missing from a hexagram, 8 question domains")
    w("cannot be read; when 父母 is missing, only 3.\n")

    w("### The domain-weighted blindness reveals practical asymmetry\n")
    # Compute
    type_miss = Counter()
    for r in records:
        for m in r['missing']:
            type_miss[m] += 1
    w("| 用神 | Missing rate | Domains | Impact = miss × domains |")
    w("|------|:-----------:|:-------:|:----------------------:|")
    for ys_type in ["官鬼", "妻財", "子孫", "父母"]:
        n = type_miss[ys_type]
        dc = DOMAIN_COUNT[ys_type]
        w(f"| {ys_type} | {n}/64 | {dc} | {n*dc} |")
    w("")
    w("官鬼's high domain count means its structural absences have disproportionate impact.")
    w("妻財 is close behind. Together, the two heaviest types (官鬼+妻財, 15/22 domains)")
    w("account for the majority of practical blindness.\n")

    w("### 兄弟's structural role: benign absence, information-theoretic gain\n")
    w("兄弟 has 0 domains — its absence from a hexagram costs nothing in question coverage.")
    w("When 兄弟 is one of the two missing types in a palace, the *effective* darkness is")
    w("determined entirely by the other missing type. This means the structural incompleteness")
    w("is less severe than it appears: about half the time, one of the two missing types is")
    w("the zero-weight 兄弟.\n")

    w("### The triad structure creates diagnostic gradients\n")
    w("Only a fraction of hexagram-用神 contexts provide full diagnostic information")
    w("(signal + support + threat all present). The remainder are degraded in specific ways:")
    w("Blind (can't read), Exposed (can read but vulnerable), Unguarded (can read but")
    w("can't see threats), Isolated (signal only, no context).")
    w("This gradient is the mechanism through which structure constrains meaning —")
    w("not by preventing readings entirely, but by controlling how much diagnostic")
    w("context is available for each question type.\n")

    w("### Connection to the central thread\n")
    w("The 用神 mapping is Layer 3 of the I Ching's interpretive system:")
    w("1. **Structure** (Z₂⁶ algebra, trigram decomposition) → the space")
    w("2. **Incompleteness** (missing 六親 types) → curvature of the space")
    w("3. **用神 projection** (question → 六親 type) → meaning enters the curved space\n")
    w("The key finding: the structural space is symmetric (五行 cycle treats all types")
    w("equally), but the 用神 projection is asymmetric (8 domains for 官鬼, 0 for 兄弟).")
    w("It is this projection — not the algebra — that creates the practical asymmetries")
    w("practitioners navigate. The question doesn't just enter a space; it enters a space")
    w("that is uniformly curved but non-uniformly illuminated by the question's own category.\n")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PROBE 3: 用神 PROJECTION — WHERE MEANING ENTERS")
    print("=" * 70)

    records, hex_info = build_data()

    sections = []
    sections.append("# Probe 3: 用神 Projection — Where Meaning Enters\n")

    print("\n── A. Querrent's Position ──")
    sections.append(section_a())

    print("\n── B. Signal/Noise per Palace ──")
    sections.append(section_b(records))

    print("\n── C. Incompleteness Interaction ──")
    sections.append(section_c(records))

    print("\n── D. Readability Matrix ──")
    sections.append(section_d(records))

    print("\n── E. Shadow Hit Probability ──")
    sections.append(section_e(records))

    print("\n── F. Triad Diagnostics ──")
    sections.append(section_f(records))

    print("\n── Synthesis ──")
    sections.append(synthesis(records))

    # Write
    out = Path(__file__).parent / "probe3_results.md"
    out.write_text('\n'.join(sections))
    print(f"\nResults written to {out}")


if __name__ == '__main__':
    main()
