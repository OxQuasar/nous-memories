#!/usr/bin/env python3
"""
bridge_scan.py — Exhaustive bridge scan (Q4)

Tests ALL algebraic coordinates × ALL text markers for statistical
association, with position control (CMH). Determines whether basin×凶
and 生体×吉 are isolated leaders or part of a gradient.

Output: bridge_scan_results.json + printed summary table.
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from itertools import product as iterproduct

import numpy as np
from scipy import stats as sp_stats

# ─── Paths ──────────────────────────────────────────────────────────

HERE = Path(__file__).resolve().parent
ICHING = HERE.parent
ATLAS_PATH = ICHING / "atlas" / "atlas.json"
MARKERS_PATH = ICHING / "semantic-map" / "data" / "stock_phrases.json"
OUT_PATH = HERE / "bridge_scan_results.json"

# ─── Load data ──────────────────────────────────────────────────────

def load_data():
    with open(ATLAS_PATH) as f:
        atlas = json.load(f)
    with open(MARKERS_PATH) as f:
        sp = json.load(f)
    return atlas, sp["marker_matrix"]


# ─── Build records ──────────────────────────────────────────────────

# Markers to test (binary flags)
MARKER_NAMES = ["吉", "凶", "无咎", "利", "厲", "吝", "悔", "亨", "咎", "悔亡", "貞", "利貞", "利涉大川"]

# Core projection coordinates (derive from nuclear / inner structure)
CORE_COORDS = ["basin", "hu_depth", "hu_relation", "i_component"]

# Shell projection coordinates (derive from surface / palace structure)
SHELL_COORDS = ["surface_relation", "palace", "rank", "shi", "palace_element"]

ALL_COORDS = CORE_COORDS + SHELL_COORDS


def build_records(atlas, marker_matrix):
    """Build 384 records: one per yaoci, with markers + algebraic coords."""
    # Index marker_matrix by (hex_val, line)
    marker_index = {}
    for entry in marker_matrix:
        marker_index[(entry["hex_val"], entry["line"])] = entry["markers"]

    records = []
    for h in range(64):
        a = atlas[str(h)]
        for line in range(6):
            markers_present = marker_index.get((h, line), [])
            marker_flags = {m: (m in markers_present) for m in MARKER_NAMES}

            rec = {
                "hex_val": h,
                "line_position": line,
                # Markers
                **marker_flags,
                # Core coords
                "basin": a["basin"],
                "hu_depth": a["hu_depth"],
                "hu_relation": a["hu_relation"],
                "i_component": a["i_component"],
                # Shell coords
                "surface_relation": a["surface_relation"],
                "palace": a["palace"],
                "rank": a["rank"],
                "shi": a["shi"],
                "palace_element": a["palace_element"],
            }
            records.append(rec)
    return records


# ─── Statistical tests ─────────────────────────────────────────────

def contingency_2x2(records, coord_val_func, marker):
    """Build 2×2 table: coord_positive × marker_positive."""
    a, b, c, d = 0, 0, 0, 0
    for r in records:
        cv = coord_val_func(r)
        mv = r[marker]
        if cv and mv:     a += 1
        elif cv and not mv: b += 1
        elif not cv and mv: c += 1
        else:              d += 1
    return np.array([[a, b], [c, d]])


def contingency_kx2(records, coord, marker):
    """Build k×2 table: k levels of coord × marker present/absent."""
    levels = sorted(set(r[coord] for r in records), key=str)
    table = np.zeros((len(levels), 2), dtype=int)
    level_idx = {lv: i for i, lv in enumerate(levels)}
    for r in records:
        i = level_idx[r[coord]]
        j = 0 if r[marker] else 1
        table[i, j] += 1
    return table, levels


def fisher_or_chi2(table):
    """Use Fisher exact for 2×2 with any cell < 5, else chi-squared."""
    if table.shape == (2, 2) and table.min() < 5:
        odds, p = sp_stats.fisher_exact(table)
        return p, odds, "fisher"
    else:
        # For tables with zero rows/columns, remove them
        nonzero_rows = table.sum(axis=1) > 0
        nonzero_cols = table.sum(axis=0) > 0
        t = table[nonzero_rows][:, nonzero_cols]
        if t.shape[0] < 2 or t.shape[1] < 2:
            return 1.0, None, "degenerate"
        try:
            chi2, p, dof, _ = sp_stats.chi2_contingency(t)
            # Cramér's V
            n = t.sum()
            k = min(t.shape) - 1
            v = np.sqrt(chi2 / (n * max(k, 1))) if k > 0 else 0
            return p, v, "chi2"
        except ValueError:
            return 1.0, None, "error"


def cmh_test(records, coord_val_func, marker, strata_func):
    """
    Cochran-Mantel-Haenszel test.

    For each stratum defined by strata_func, build a 2×2 table
    (coord_positive × marker_positive). Compute common OR and CMH chi-squared.
    """
    strata = defaultdict(lambda: np.zeros((2, 2), dtype=float))
    for r in records:
        s = strata_func(r)
        cv = 1 if coord_val_func(r) else 0
        mv = 1 if r[marker] else 0
        strata[s][cv, mv] += 1

    # CMH formula
    numer = 0.0
    denom = 0.0
    or_numer = 0.0
    or_denom = 0.0

    for s, t in strata.items():
        a, b, c, d = t[1, 1], t[1, 0], t[0, 1], t[0, 0]
        n = a + b + c + d
        if n == 0:
            continue
        r1 = a + b  # coord=1 row total
        r0 = c + d  # coord=0 row total
        c1 = a + c  # marker=1 col total
        c0 = b + d  # marker=0 col total

        numer += a - (r1 * c1) / n
        denom += (r1 * r0 * c1 * c0) / (n * n * (n - 1)) if n > 1 else 0

        # MH common OR components
        or_numer += (a * d) / n if n > 0 else 0
        or_denom += (b * c) / n if n > 0 else 0

    if denom <= 0:
        return 1.0, None

    chi2_cmh = (abs(numer) - 0.5) ** 2 / denom  # continuity correction
    p_cmh = 1 - sp_stats.chi2.cdf(chi2_cmh, df=1)

    common_or = or_numer / or_denom if or_denom > 0 else float('inf')

    return p_cmh, common_or


def cmh_multi_level(records, coord, marker, strata_func):
    """
    For multi-level coordinate: test each level vs rest as binary,
    return the most significant pairwise contrast.
    """
    levels = sorted(set(r[coord] for r in records), key=str)
    results = []
    for lv in levels:
        val_func = lambda r, lv=lv: r[coord] == lv
        p, common_or = cmh_test(records, val_func, marker, strata_func)
        results.append((lv, p, common_or))
    return results


def position_stratum(r):
    return r["line_position"]


def position_basin_stratum(r):
    return (r["line_position"], r["basin"])


def position_surface_stratum(r):
    return (r["line_position"], r["surface_relation"])


# ─── Main scan ──────────────────────────────────────────────────────

def run_scan(records):
    results = []

    # Drop very rare markers (< 5 occurrences) from significance testing
    marker_counts = {m: sum(1 for r in records if r[m]) for m in MARKER_NAMES}
    active_markers = [m for m in MARKER_NAMES if marker_counts[m] >= 5]

    print(f"Active markers (≥5 occurrences): {active_markers}")
    print(f"Dropped: {[m for m in MARKER_NAMES if marker_counts[m] < 5]}")
    print(f"Marker counts: {marker_counts}")
    print()

    for coord in ALL_COORDS:
        projection = "core" if coord in CORE_COORDS else "shell"
        levels = sorted(set(r[coord] for r in records), key=str)
        n_levels = len(levels)

        for marker in active_markers:
            # Skip very rare markers for this coord
            if marker_counts[marker] < 5:
                continue

            # ── Raw test (overall) ──
            table, lvls = contingency_kx2(records, coord, marker)
            raw_p, raw_effect, raw_method = fisher_or_chi2(table)

            # ── CMH position-controlled (pairwise binary) ──
            pairwise = cmh_multi_level(records, coord, marker, position_stratum)
            best_pw = min(pairwise, key=lambda x: x[1])
            best_level, cmh_p, cmh_or = best_pw

            # ── Overall multi-level CMH (aggregate) ──
            # For multi-level coords, also do an overall chi-squared
            # within position strata (Generalized CMH)
            overall_cmh_p = None
            if n_levels > 2:
                # Use pairwise min as primary signal
                pass

            # ── Bridge-controlled test ──
            bridge_p = None
            bridge_or = None
            if cmh_p < 0.05:
                val_func = lambda r, lv=best_level: r[coord] == lv
                if projection == "shell":
                    # Control for (position, basin)
                    bridge_p, bridge_or = cmh_test(records, val_func, marker,
                                                    position_basin_stratum)
                else:
                    # Control for (position, surface_relation)
                    bridge_p, bridge_or = cmh_test(records, val_func, marker,
                                                    position_surface_stratum)

            entry = {
                "coord": coord,
                "projection": projection,
                "marker": marker,
                "n_levels": n_levels,
                "marker_count": marker_counts[marker],
                "raw_p": raw_p,
                "raw_effect": raw_effect if raw_effect is not None else None,
                "raw_method": raw_method,
                "cmh_p": cmh_p,
                "cmh_or": cmh_or if cmh_or is not None else None,
                "cmh_best_level": str(best_level),
                "bridge_p": bridge_p,
                "bridge_or": bridge_or,
                "all_pairwise": [(str(lv), p, o) for lv, p, o in pairwise],
            }
            results.append(entry)

    # Sort by CMH p-value
    results.sort(key=lambda x: x["cmh_p"])
    return results


# ─── Display ────────────────────────────────────────────────────────

def print_table(results):
    print("=" * 120)
    print("  EXHAUSTIVE BRIDGE SCAN — ALL COORDINATE × MARKER PAIRS")
    print("  Sorted by CMH position-controlled p-value")
    print("=" * 120)
    print()

    # Header
    hdr = f"{'Coord':<20} {'Proj':<6} {'Marker':<8} {'Raw p':>10} {'CMH p':>10} {'CMH OR':>8} {'Best Level':<12} {'Bridge p':>10} {'Bridge OR':>8}"
    print(hdr)
    print("-" * len(hdr))

    sig_count = 0
    sig_after_bridge = 0

    for r in results:
        raw_p = f"{r['raw_p']:.2e}" if r['raw_p'] is not None else "N/A"
        cmh_p = f"{r['cmh_p']:.2e}" if r['cmh_p'] is not None else "N/A"
        cmh_or = f"{r['cmh_or']:.2f}" if r['cmh_or'] is not None else "N/A"
        bridge_p = f"{r['bridge_p']:.2e}" if r['bridge_p'] is not None else ""
        bridge_or = f"{r['bridge_or']:.2f}" if r['bridge_or'] is not None else ""

        flag = ""
        if r['cmh_p'] < 0.05:
            sig_count += 1
            flag = " *"
            if r['bridge_p'] is not None and r['bridge_p'] < 0.05:
                sig_after_bridge += 1
                flag = " **"

        print(f"{r['coord']:<20} {r['projection']:<6} {r['marker']:<8} "
              f"{raw_p:>10} {cmh_p:>10} {cmh_or:>8} {r['cmh_best_level']:<12} "
              f"{bridge_p:>10} {bridge_or:>8}{flag}")

    print()
    print(f"Total pairs tested: {len(results)}")
    print(f"Significant at CMH p < 0.05: {sig_count}")
    print(f"Significant after bridge control: {sig_after_bridge}")
    print()

    # ── Bonferroni correction ──
    n_tests = len(results)
    bonf_threshold = 0.05 / n_tests
    bonf_sig = sum(1 for r in results if r['cmh_p'] < bonf_threshold)
    print(f"Bonferroni threshold (0.05/{n_tests}): {bonf_threshold:.2e}")
    print(f"Significant after Bonferroni: {bonf_sig}")
    print()

    # ── Detail on CMH-significant pairs ──
    print("=" * 80)
    print("  DETAIL: All CMH-significant pairs (p < 0.05)")
    print("=" * 80)
    for r in results:
        if r['cmh_p'] >= 0.05:
            break
        print(f"\n  {r['coord']} × {r['marker']} (projection: {r['projection']})")
        print(f"    Raw p={r['raw_p']:.2e}, CMH p={r['cmh_p']:.2e}")
        print(f"    CMH OR={r['cmh_or']:.3f} at level '{r['cmh_best_level']}'")
        if r['bridge_p'] is not None:
            print(f"    Bridge-controlled: p={r['bridge_p']:.2e}, OR={r['bridge_or']:.3f}")
            if r['bridge_p'] < 0.05:
                print(f"    → SURVIVES bridge control")
            else:
                print(f"    → Absorbed by bridge")
        print(f"    All pairwise contrasts:")
        for lv, p, o in r['all_pairwise']:
            o_str = f"{o:.3f}" if o is not None else "N/A"
            flag = " ← best" if lv == r['cmh_best_level'] else ""
            print(f"      {lv:>15}: CMH p={p:.4e}, OR={o_str}{flag}")

    print()

    # ── Summary: the bridge question ──
    print("=" * 80)
    print("  SUMMARY: BRIDGE ISOLATION TEST")
    print("=" * 80)
    print()

    core_sig = [r for r in results if r['projection'] == 'core' and r['cmh_p'] < 0.05]
    shell_sig = [r for r in results if r['projection'] == 'shell' and r['cmh_p'] < 0.05]

    print(f"  Core projection significant pairs: {len(core_sig)}")
    for r in core_sig:
        bstr = f", bridge p={r['bridge_p']:.2e}" if r['bridge_p'] is not None else ""
        print(f"    {r['coord']}×{r['marker']}: CMH p={r['cmh_p']:.2e}{bstr}")

    print(f"\n  Shell projection significant pairs: {len(shell_sig)}")
    for r in shell_sig:
        bstr = f", bridge p={r['bridge_p']:.2e}" if r['bridge_p'] is not None else ""
        print(f"    {r['coord']}×{r['marker']}: CMH p={r['cmh_p']:.2e}{bstr}")

    # Count surviving after bridge control
    core_surviving = [r for r in core_sig if r['bridge_p'] is None or r['bridge_p'] < 0.05]
    shell_surviving = [r for r in shell_sig if r['bridge_p'] is None or r['bridge_p'] < 0.05]

    print(f"\n  Core surviving bridge control: {len(core_surviving)}")
    print(f"  Shell surviving bridge control: {len(shell_surviving)}")
    print()

    prediction_holds = (
        any(r['coord'] == 'basin' and r['marker'] == '凶' and r['cmh_p'] < 0.05
            for r in results) and
        any(r['coord'] == 'surface_relation' and r['marker'] == '吉' and r['cmh_p'] < 0.05
            for r in results)
    )
    print(f"  Prediction (basin×凶 + surface_relation×吉 as leaders): {'CONFIRMED' if prediction_holds else 'REJECTED'}")


# ─── Main ───────────────────────────────────────────────────────────

def main():
    atlas, marker_matrix = load_data()
    records = build_records(atlas, marker_matrix)
    print(f"Built {len(records)} yaoci records")
    print()

    results = run_scan(records)
    print_table(results)

    # Save results
    # Convert for JSON serialization
    json_results = []
    for r in results:
        jr = dict(r)
        for k in ['raw_p', 'raw_effect', 'cmh_p', 'cmh_or', 'bridge_p', 'bridge_or']:
            if jr[k] is not None:
                if np.isinf(jr[k]):
                    jr[k] = "Inf"
                elif np.isnan(jr[k]):
                    jr[k] = "NaN"
        json_results.append(jr)

    with open(OUT_PATH, 'w') as f:
        json.dump(json_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
