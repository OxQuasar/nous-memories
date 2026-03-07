#!/usr/bin/env python3
"""
Shared parser for 京氏易傳 source texts.

Reads 卷上 and 卷中, splits by hexagram unicode markers (U+4DC0–U+4DFF),
maps each to King Wen number and 6-bit hex_val.
"""

import re
import sys
from pathlib import Path

# ─── Path setup ────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "kingwen"))
sys.path.insert(0, str(BASE_DIR / "huozhulin"))
sys.path.insert(0, str(BASE_DIR / "opposition-theory" / "phase4"))

from sequence import KING_WEN

# ─── Constants ─────────────────────────────────────────────────────────────

TEXT_DIR = BASE_DIR.parent / "texts" / "jingshi_yizhuan"
SOURCE_FILES = [
    TEXT_DIR / "jingshi_yizhuan_1.md",  # 卷上: 32 hexagrams
    TEXT_DIR / "jingshi_yizhuan_2.md",  # 卷中: 32 hexagrams
]

HEX_UNICODE_START = 0x4DC0

# KW number → hex_val (6-bit int, bit 0 = bottom line)
KW_TO_HEX = {}
HEX_TO_KW = {}
for _kw_num, _name, _binstr in KING_WEN:
    _hv = int(_binstr[::-1], 2)
    KW_TO_HEX[_kw_num] = _hv
    HEX_TO_KW[_hv] = {"kw_num": _kw_num, "name": _name, "binstr": _binstr}


# ─── Parser ────────────────────────────────────────────────────────────────

def parse_entries():
    """Parse 京氏易傳 into per-hexagram entries.

    Returns:
        dict mapping hex_val (6-bit int) → {
            "kw_num": int,
            "unicode": str,
            "text": str,
            "name": str,
        }
    """
    full_text = ""
    for f in SOURCE_FILES:
        full_text += f.read_text()

    # Locate all hexagram unicode markers
    markers = []
    for i, ch in enumerate(full_text):
        code = ord(ch)
        if HEX_UNICODE_START <= code <= HEX_UNICODE_START + 63:
            kw_num = code - HEX_UNICODE_START + 1
            markers.append((i, ch, kw_num))

    # Split into per-hexagram text blocks
    entries = {}
    for idx, (pos, char, kw_num) in enumerate(markers):
        end = markers[idx + 1][0] if idx + 1 < len(markers) else len(full_text)
        text = full_text[pos + 1 : end].strip()
        hex_val = KW_TO_HEX[kw_num]
        entries[hex_val] = {
            "kw_num": kw_num,
            "unicode": char,
            "text": text,
            "name": HEX_TO_KW[hex_val]["name"],
        }

    return entries


if __name__ == "__main__":
    entries = parse_entries()
    print(f"Parsed {len(entries)} hexagram entries\n")
    for hv in sorted(entries.keys()):
        e = entries[hv]
        print(f"  KW#{e['kw_num']:2d} {e['unicode']} {e['name']:12s} "
              f"(hex={hv:06b}) — {len(e['text'])} chars")
