#!/usr/bin/env python3
"""
Probe 8b: Parse historical events from 皇極經世 vol 6.

Extracts (天干, 地支, event_text) tuples from the annalistic entries.
Handles multi-year lines, continuation lines, inline section headers,
and corrupted ganzhi markers (e.g. 申寅 for 甲寅 on line 577).

Approach: concatenate all body text (stripping structural headers), then
scan sequentially for the 60-year 天干地支 cycle with lookahead to handle
corrupted/missing markers.
"""

import json
import re
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent

# ─── Constants ───────────────────────────────────────────────────────────────

TIANGAN = "甲乙丙丁戊己庚辛壬癸"
DIZHI = "子丑寅卯辰巳午未申酉戌亥"

# Full 60-year sexagenary cycle
GANZHI_CYCLE = [TIANGAN[i % 10] + DIZHI[i % 12] for i in range(60)]

# Chinese numeral character class (for header matching)
NUM = "[零一二三四五六七八九十百千萬]+"
GZ_ALL = TIANGAN + DIZHI + "已"  # 已 is common variant of 巳

# Structural header patterns to strip from body text
HEADER_PATTERNS = [
    re.compile(r'皇極經世書卷六[上中下]宋邵雍撰'),
    re.compile(r'皇極經世書卷六[上中下]'),
    re.compile(rf'觀物篇{NUM}以運經世{NUM}'),
    re.compile(rf'經世之[{GZ_ALL}]{NUM}'),
    re.compile(rf'經元之[{GZ_ALL}]{NUM}'),
    re.compile(rf'經㑹之[{GZ_ALL}]{NUM}'),
    re.compile(rf'經運之[{GZ_ALL}]{NUM}'),
    re.compile(r'欽定四庫全書'),
]

# Lookahead window for corrupted marker recovery
LOOKAHEAD = 10

# ─── Read source ─────────────────────────────────────────────────────────────

src = HERE.parent.parent / "texts" / "huangjijingshi" / "6-hj.txt"
lines = src.read_text().splitlines()

# ─── Phase 1: Build body text with char→line mapping ────────────────────────
# Only include indented lines (starting with full-width space 　).
# Strip full-width spaces, then remove structural headers.

body_chars = []  # (char, original_line_number)

for lineno, line in enumerate(lines, 1):
    if not line.startswith('\u3000'):
        continue
    content = line.replace('\u3000', '')  # strip all full-width spaces
    for pat in HEADER_PATTERNS:
        content = pat.sub('', content)
    content = content.strip()
    if not content:
        continue
    for ch in content:
        body_chars.append((ch, lineno))

body = ''.join(ch for ch, _ in body_chars)
print(f"Body text: {len(body)} characters")

# ─── Phase 2: Sequential ganzhi scan with lookahead ─────────────────────────
# Follow the 60-year cycle. When the expected next marker isn't found before
# a subsequent marker, treat it as corrupted/missing (insert blank entry).

entries = []

# Find starting 甲子
start = body.find('甲子')
if start < 0:
    raise ValueError("Cannot find starting 甲子")

pos = start
cycle_idx = 0  # 甲子 = index 0
corruptions = []

while pos < len(body) - 1:
    gz = GANZHI_CYCLE[cycle_idx]

    # Verify we're at the expected ganzhi
    if body[pos:pos + 2] != gz:
        break  # shouldn't happen in normal flow

    marker_line = body_chars[pos][1]
    text_start = pos + 2

    # Find next marker: search expected + lookahead candidates, take earliest.
    # Don't break early on skip=0 — a corrupted marker (e.g. 申寅 for 甲寅)
    # means the expected ganzhi is found far away while the NEXT one is nearby.
    best_pos = -1
    best_skip = -1  # how many positions we skip (0 = found expected)

    for skip in range(LOOKAHEAD):
        try_idx = (cycle_idx + 1 + skip) % 60
        try_gz = GANZHI_CYCLE[try_idx]
        found = body.find(try_gz, text_start)
        if found >= 0 and (best_pos < 0 or found < best_pos):
            best_pos = found
            best_skip = skip

    if best_pos < 0:
        # Last entry: no more markers found
        event_text = body[text_start:].strip()
        entries.append({"tiangan": gz[0], "dizhi": gz[1], "text": event_text, "line": marker_line})
        break

    # Extract text for current entry
    event_text = body[text_start:best_pos].strip()
    entries.append({"tiangan": gz[0], "dizhi": gz[1], "text": event_text, "line": marker_line})

    # Insert blank entries for any skipped (corrupted/missing) markers
    if best_skip > 0:
        for s in range(best_skip):
            skip_idx = (cycle_idx + 1 + s) % 60
            skip_gz = GANZHI_CYCLE[skip_idx]
            est_line = body_chars[min(text_start, len(body_chars) - 1)][1]
            entries.append({"tiangan": skip_gz[0], "dizhi": skip_gz[1], "text": "", "line": est_line})
            corruptions.append((skip_gz, est_line))

    # Advance to the found marker
    pos = best_pos
    cycle_idx = (cycle_idx + 1 + best_skip) % 60

# ─── Phase 3: Validate cycle continuity ─────────────────────────────────────

expected_cycle = [GANZHI_CYCLE[(i) % 60] for i in range(len(entries))]
actual_cycle = [e["tiangan"] + e["dizhi"] for e in entries]
mismatches = [(i, exp, act) for i, (exp, act) in enumerate(zip(expected_cycle, actual_cycle)) if exp != act]

if mismatches:
    print(f"\n⚠ {len(mismatches)} cycle mismatches:")
    for i, exp, act in mismatches[:10]:
        print(f"  entry {i}: expected {exp}, got {act} (line {entries[i]['line']})")
else:
    print(f"✓ All {len(entries)} entries follow sequential 60-year cycle")

if corruptions:
    print(f"\n⚠ {len(corruptions)} corrupted/missing markers (filled as blank):")
    for gz, line in corruptions:
        print(f"  {gz} near line {line}")

# ─── Phase 4: Statistics ────────────────────────────────────────────────────

total = len(entries)
with_text = sum(1 for e in entries if e["text"])
blank = total - with_text

print(f"\n{'='*60}")
print(f"Total entries:     {total}")
print(f"  With text:       {with_text}")
print(f"  Blank:           {blank}")
print(f"  Coverage:        {with_text/total*100:.1f}%")
print(f"  30-year blocks:  {total / 30:.1f}")

# Distribution by 天干 (entries with text)
tg_dist = Counter(e["tiangan"] for e in entries if e["text"])
print(f"\nDistribution by 天干 (entries with text):")
for tg in TIANGAN:
    count = tg_dist.get(tg, 0)
    bar = "█" * (count // 2)
    print(f"  {tg}: {count:4d}  {bar}")

# Distribution by 天干 (all entries)
tg_all = Counter(e["tiangan"] for e in entries)
print(f"\nDistribution by 天干 (all entries):")
for tg in TIANGAN:
    print(f"  {tg}: {tg_all.get(tg, 0):4d}")

# Distribution by 地支 (entries with text)
dz_dist = Counter(e["dizhi"] for e in entries if e["text"])
print(f"\nDistribution by 地支 (entries with text):")
for dz in DIZHI:
    count = dz_dist.get(dz, 0)
    bar = "█" * (count // 2)
    print(f"  {dz}: {count:4d}  {bar}")

# Text length statistics
text_lens = [len(e["text"]) for e in entries if e["text"]]
if text_lens:
    print(f"\nEvent text lengths:")
    print(f"  Min:    {min(text_lens)}")
    print(f"  Max:    {max(text_lens)}")
    print(f"  Mean:   {sum(text_lens)/len(text_lens):.1f}")
    print(f"  Median: {sorted(text_lens)[len(text_lens)//2]}")

# ─── Phase 5: Print samples ────────────────────────────────────────────────

def fmt_entry(e, max_text=70):
    gz = e["tiangan"] + e["dizhi"]
    t = e["text"]
    text = t[:max_text] + ("..." if len(t) > max_text else "")
    return f"  L{e['line']:4d} {gz} [{len(t):3d}] {text}"

print(f"\n{'─'*60}")
print("First 20 entries:")
for e in entries[:20]:
    print(fmt_entry(e))

print(f"\n{'─'*60}")
print("Last 20 entries:")
for e in entries[-20:]:
    print(fmt_entry(e))

# Entries around the corruption point
print(f"\n{'─'*60}")
print("Entries around corruption (225-240):")
for e in entries[225:245]:
    idx = entries.index(e)
    print(f"  [{idx:4d}] {fmt_entry(e)}")

# Longest entries
print(f"\n{'─'*60}")
print("Top 10 longest entries:")
by_len = sorted(entries, key=lambda e: len(e["text"]), reverse=True)
for e in by_len[:10]:
    idx = entries.index(e)
    print(f"  [{idx:4d}] {fmt_entry(e, max_text=80)}")

# ─── Phase 6: Save JSON ────────────────────────────────────────────────────

out_path = HERE / "hjjs_events.json"
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)
print(f"\n✓ Saved {total} entries to {out_path}")
