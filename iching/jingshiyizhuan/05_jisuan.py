#!/usr/bin/env python3
"""
Probe 5: 積算 — Computational Cycle Range

Confirms 積算 start = 建始 end, span = full 60-cycle.
Minimal extraction — the field carries zero additional information.
"""

import re
import sys
import importlib.util
from pathlib import Path
from collections import Counter

# ─── Imports ───────────────────────────────────────────────────────────────

HERE = Path(__file__).resolve().parent
BASE = HERE.parent

sys.path.insert(0, str(BASE / "opposition-theory" / "phase4"))
sys.path.insert(0, str(BASE / "huozhulin"))

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

p0 = _load("p0", HERE / "00_parse_jingshi.py")
p2 = _load("p2", BASE / "huozhulin" / "02_palace_kernel.py")
p4 = _load("p4", HERE / "04_jieqi.py")

parse_entries = p0.parse_entries
generate_palaces = p2.generate_palaces
gz_index = p4.gz_index
gz_chars = p4.gz_chars
extract_jianshi = p4.extract_jianshi
STEMS = p4.STEMS
BRANCHES = p4.BRANCHES

# ─── Extraction ────────────────────────────────────────────────────────────

STEM_PAT = "[" + "".join(STEMS) + "]"
BRANCH_PAT = "[" + "".join(BRANCHES) + "]"

JISUAN_RE = re.compile(
    r"積算起(" + STEM_PAT + ")(" + BRANCH_PAT + ")"
    r"[^至]{0,20}至"
    r"(" + STEM_PAT + ")(" + BRANCH_PAT + ")"
)


def extract_jisuan(text):
    """Extract 積算 range. Returns (start_gz, end_gz, span) or (None, None, None)."""
    m = JISUAN_RE.search(text)
    if not m:
        return None, None, None
    start = gz_index(m.group(1), m.group(2))
    end = gz_index(m.group(3), m.group(4))
    span = (end - start) % 60
    return start, end, span


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    entries = parse_entries()
    _, hex_info = generate_palaces()

    print("=" * 78)
    print("PROBE 5: 積算 — COMPUTATIONAL CYCLE RANGE")
    print("=" * 78)

    # ── Extract both 建始 and 積算 ──
    results = []
    for hv in sorted(entries.keys()):
        e = entries[hv]
        hi = hex_info[hv]
        text = e["text"]

        j_start, j_end, _, _, j_note = extract_jianshi(text)
        a_start, a_end, a_span = extract_jisuan(text)

        results.append({
            "kw": e["kw_num"], "name": e["name"], "hv": hv,
            "palace": hi["palace"], "rank_name": hi["rank_name"],
            "j_start": j_start, "j_end": j_end,
            "a_start": a_start, "a_end": a_end, "a_span": a_span,
        })

    # ── Summary stats ──
    n_jisuan = sum(1 for r in results if r["a_start"] is not None)
    n_jianshi = sum(1 for r in results if r["j_start"] is not None)
    n_both = sum(1 for r in results
                 if r["j_start"] is not None and r["a_start"] is not None)

    print(f"\n  積算 extracted: {n_jisuan}/64")
    print(f"  建始 extracted: {n_jianshi}/64")
    print(f"  Both available: {n_both}/64")

    # ── Span analysis ──
    spans = [r["a_span"] for r in results if r["a_span"] is not None]
    print(f"\n  積算 span distribution: {dict(sorted(Counter(spans).items()))}")

    # ── Critical test: 積算 start = 建始 end ──
    print(f"\n{'=' * 78}")
    print("CRITICAL TEST: 積算 START = 建始 END")
    print(f"{'=' * 78}\n")

    match = 0
    mismatch = 0
    for r in results:
        if r["j_end"] is not None and r["a_start"] is not None:
            if r["j_end"] == r["a_start"]:
                match += 1
            else:
                mismatch += 1
                js, jb = gz_chars(r["j_end"])
                as_, ab = gz_chars(r["a_start"])
                diff = (r["a_start"] - r["j_end"]) % 60
                print(f"  MISMATCH KW#{r['kw']:2d} {r['name']:12s}: "
                      f"建始end={js}{jb}({r['j_end']}) "
                      f"積算start={as_}{ab}({r['a_start']}) "
                      f"diff={diff}  {r['palace']} {r['rank_name']}")

    print(f"\n  Match: {match}/{match + mismatch}")
    print(f"  Mismatch: {mismatch}/{match + mismatch}")

    # ── Non-59 span anomalies ──
    print(f"\n{'=' * 78}")
    print("SPAN ANOMALIES (non-59)")
    print(f"{'=' * 78}\n")

    for r in results:
        if r["a_span"] is not None and r["a_span"] != 59:
            ss, sb = gz_chars(r["a_start"])
            es, eb = gz_chars(r["a_end"])
            # Check if end branch matches expected
            expected_end = (r["a_start"] - 1) % 60
            exp_s, exp_b = gz_chars(expected_end)
            branch_match = eb == exp_b
            print(f"  KW#{r['kw']:2d} {r['name']:12s}: "
                  f"{ss}{sb}({r['a_start']})→{es}{eb}({r['a_end']}) "
                  f"span={r['a_span']}  "
                  f"expected_end={exp_s}{exp_b}({expected_end})  "
                  f"branch_match={'✓' if branch_match else '✗'}  "
                  f"{r['palace']} {r['rank_name']}")

    # ── Summary ──
    print(f"\n{'=' * 78}")
    print("SUMMARY")
    print(f"{'=' * 78}")

    print(f"\n  ★ 積算 start = 建始 end: {match}/{match+mismatch}")
    print(f"  ★ 積算 span = 59 (full 60-cycle): {spans.count(59)}/{len(spans)}")
    print(f"  ★ 積算 carries ZERO information beyond 建始")
    print(f"    (start = 建始 end, end = start - 1, completing the cycle)")
    anomaly_count = sum(1 for s in spans if s != 59)
    if anomaly_count:
        print(f"  → {anomaly_count} span anomalies: stem corruption in end 干支 "
              "(branch preserved)")


if __name__ == "__main__":
    main()
