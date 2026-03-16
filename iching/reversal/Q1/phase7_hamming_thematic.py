#!/usr/bin/env python3
"""Q1 Phase 7: Hamming-Thematic Anti-Correlation Deep Dive.

Phase 6 found: hexagrams close in Hamming distance have MORE distant thematic
content (r ≈ -0.10, strengthens to -0.17 excluding complements). This script
investigates the line-level mechanism behind this anti-correlation.

Tests:
  1. Line-level mechanism — changed line vs shared lines
  2. Position dependence — which line positions drive the effect
  3. Trigram-level analysis — shared trigram families
  4. Hamming=5 (near-complement) analysis
  5. Cross-model verification
"""

import numpy as np
import json
from pathlib import Path
from collections import defaultdict

from scipy.spatial.distance import cosine as cos_dist
from scipy.stats import pearsonr, spearmanr

from phase1_residual_structure import load_data, build_design_matrix, extract_residuals

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/iching
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
OUT_DIR = Path(__file__).resolve().parent

MODELS = ['bge-m3', 'e5-large', 'labse']


# ═══════════════════════════════════════════════════════
# Setup
# ═══════════════════════════════════════════════════════

def load_residuals_for_model(shortname):
    """Load embeddings and extract residuals for a model."""
    if shortname == 'bge-m3':
        yaoci, meta, atlas = load_data()
    else:
        emb_path = OUT_DIR / f"embeddings_{shortname}.npz"
        yaoci = np.load(emb_path)['yaoci']
        _, meta, atlas = load_data()

    X, _ = build_design_matrix(meta)
    residual, r2, _ = extract_residuals(yaoci, X)
    return residual, atlas


def build_pairs_by_hamming():
    """Build all 2016 hex pairs grouped by Hamming distance."""
    pairs_by_d = defaultdict(list)
    for i in range(64):
        for j in range(i + 1, 64):
            d = bin(i ^ j).count('1')
            pairs_by_d[d].append((i, j))
    return pairs_by_d


def hamming1_by_position():
    """Hamming-1 pairs grouped by the differing bit position."""
    by_pos = defaultdict(list)
    for i in range(64):
        for j in range(i + 1, 64):
            diff = i ^ j
            if bin(diff).count('1') == 1:
                pos = diff.bit_length() - 1  # 0-indexed from bottom
                by_pos[pos].append((i, j))
    return by_pos


def trigram_sharing(h1, h2):
    """Classify trigram sharing: 'upper', 'lower', 'both', 'neither'."""
    share_lower = (h1 & 7) == (h2 & 7)
    share_upper = (h1 >> 3) == (h2 >> 3)
    if share_lower and share_upper:
        return 'both'
    elif share_upper:
        return 'upper'
    elif share_lower:
        return 'lower'
    else:
        return 'neither'


# ═══════════════════════════════════════════════════════
# Test 1: Line-Level Mechanism (Hamming-1 pairs)
# ═══════════════════════════════════════════════════════

def test_line_mechanism(residual, atlas, label=''):
    """For Hamming-1 pairs: is distance from the changed line or shared lines?"""
    print(f"\n{'='*70}")
    print(f"TEST 1: LINE-LEVEL MECHANISM{f' ({label})' if label else ''}")
    print(f"{'='*70}")

    h1_by_pos = hamming1_by_position()

    changed_dists = []  # cosine distance at the changed line
    shared_dists = []   # mean cosine distance at the 5 shared-structure lines
    hex_dists = []      # centroid-level cosine distance

    per_pos_changed = defaultdict(list)
    per_pos_shared = defaultdict(list)
    per_pos_hex = defaultdict(list)

    for pos in range(6):
        for h1, h2 in h1_by_pos[pos]:
            # Line embeddings
            l1_changed = residual[h1 * 6 + pos]
            l2_changed = residual[h2 * 6 + pos]
            changed_d = cos_dist(l1_changed, l2_changed)
            changed_dists.append(changed_d)
            per_pos_changed[pos].append(changed_d)

            # Shared lines (5 other positions)
            shared_d_list = []
            for k in range(6):
                if k != pos:
                    d = cos_dist(residual[h1 * 6 + k], residual[h2 * 6 + k])
                    shared_d_list.append(d)
            mean_shared = np.mean(shared_d_list)
            shared_dists.append(mean_shared)
            per_pos_shared[pos].append(mean_shared)

            # Hex centroid distance
            c1 = residual[h1 * 6:(h1 + 1) * 6].mean(axis=0)
            c2 = residual[h2 * 6:(h2 + 1) * 6].mean(axis=0)
            hd = cos_dist(c1, c2)
            hex_dists.append(hd)
            per_pos_hex[pos].append(hd)

    changed_dists = np.array(changed_dists)
    shared_dists = np.array(shared_dists)
    hex_dists = np.array(hex_dists)

    print(f"\n  192 Hamming-1 pairs:")
    print(f"  Changed line mean cosine dist: {np.mean(changed_dists):.5f} ± {np.std(changed_dists):.5f}")
    print(f"  Shared lines mean cosine dist: {np.mean(shared_dists):.5f} ± {np.std(shared_dists):.5f}")
    print(f"  Hex centroid cosine dist:      {np.mean(hex_dists):.5f} ± {np.std(hex_dists):.5f}")
    print(f"  Ratio changed/shared:          {np.mean(changed_dists)/np.mean(shared_dists):.3f}")

    # Per-position breakdown
    print(f"\n  Per-position (32 pairs each):")
    print(f"  {'Pos':<5} {'Line':<5} {'Changed':>10} {'Shared':>10} {'Hex':>10} {'Ratio':>8}")
    print(f"  {'-'*48}")
    line_names = ['初', '二', '三', '四', '五', '上']
    for pos in range(6):
        cd = np.mean(per_pos_changed[pos])
        sd = np.mean(per_pos_shared[pos])
        hd = np.mean(per_pos_hex[pos])
        ratio = cd / sd if sd > 0 else float('inf')
        print(f"  {pos:<5} {line_names[pos]:<5} {cd:>10.5f} {sd:>10.5f} {hd:>10.5f} {ratio:>8.3f}")

    return {
        'changed_mean': float(np.mean(changed_dists)),
        'shared_mean': float(np.mean(shared_dists)),
        'hex_mean': float(np.mean(hex_dists)),
        'per_pos_changed': {p: float(np.mean(v)) for p, v in per_pos_changed.items()},
        'per_pos_shared': {p: float(np.mean(v)) for p, v in per_pos_shared.items()},
        'per_pos_hex': {p: float(np.mean(v)) for p, v in per_pos_hex.items()},
    }


# ═══════════════════════════════════════════════════════
# Test 2: Position Dependence (full Hamming spectrum)
# ═══════════════════════════════════════════════════════

def test_position_dependence(residual, atlas, label=''):
    """Which line positions contribute most to thematic distance?"""
    print(f"\n{'='*70}")
    print(f"TEST 2: POSITION DEPENDENCE{f' ({label})' if label else ''}")
    print(f"{'='*70}")

    # For ALL 2016 pairs, decompose thematic distance by line
    pairs_by_d = build_pairs_by_hamming()

    # Per-line distance contribution across all pairs
    per_line_dist = {pos: [] for pos in range(6)}
    for d in range(1, 7):
        for h1, h2 in pairs_by_d[d]:
            for pos in range(6):
                bit_differs = bool((h1 ^ h2) & (1 << pos))
                ld = cos_dist(residual[h1 * 6 + pos], residual[h2 * 6 + pos])
                key = f"d{d}_{'changed' if bit_differs else 'shared'}"
                per_line_dist[pos].append((d, bit_differs, ld))

    # Summary: mean line distance by position, split by changed vs shared
    print(f"\n  Mean line cosine distance by position:")
    print(f"  {'Pos':<5} {'Overall':>10} {'When changed':>12} {'When shared':>12} {'Δ':>8}")
    print(f"  {'-'*50}")
    line_names = ['初', '二', '三', '四', '五', '上']
    pos_results = {}
    for pos in range(6):
        all_d = [x[2] for x in per_line_dist[pos]]
        changed = [x[2] for x in per_line_dist[pos] if x[1]]
        shared = [x[2] for x in per_line_dist[pos] if not x[1]]
        overall = np.mean(all_d)
        ch_mean = np.mean(changed) if changed else 0
        sh_mean = np.mean(shared) if shared else 0
        delta = ch_mean - sh_mean
        print(f"  {pos:<5} {overall:>10.5f} {ch_mean:>12.5f} {sh_mean:>12.5f} {delta:>+8.5f}")
        pos_results[pos] = {
            'overall': float(overall),
            'changed': float(ch_mean),
            'shared': float(sh_mean),
            'delta': float(delta),
        }

    return pos_results


# ═══════════════════════════════════════════════════════
# Test 3: Trigram-Level Analysis
# ═══════════════════════════════════════════════════════

def test_trigram_analysis(residual, atlas):
    """Group pairs by trigram sharing, report thematic distances."""
    print(f"\n{'='*70}")
    print("TEST 3: TRIGRAM-LEVEL ANALYSIS")
    print(f"{'='*70}")

    centroids = np.array([residual[h * 6:(h + 1) * 6].mean(axis=0) for h in range(64)])
    pairs_by_d = build_pairs_by_hamming()

    # For each Hamming distance, group by trigram sharing
    print(f"\n  Mean hex centroid cosine distance by Hamming dist × trigram sharing:")
    print(f"  {'Hamming':>7} {'Upper':>10} {'Lower':>10} {'Neither':>10} {'Overall':>10} {'n_pairs':>8}")
    print(f"  {'-'*58}")

    overall_by_sharing = defaultdict(list)
    results = {}

    for d in range(1, 7):
        by_sharing = defaultdict(list)
        for h1, h2 in pairs_by_d[d]:
            sharing = trigram_sharing(h1, h2)
            cd = cos_dist(centroids[h1], centroids[h2])
            by_sharing[sharing].append(cd)
            overall_by_sharing[sharing].append(cd)

        upper = np.mean(by_sharing['upper']) if by_sharing['upper'] else float('nan')
        lower = np.mean(by_sharing['lower']) if by_sharing['lower'] else float('nan')
        neither = np.mean(by_sharing['neither']) if by_sharing['neither'] else float('nan')
        all_d = [cd for pairs in by_sharing.values() for cd in pairs]
        overall = np.mean(all_d)

        n_u = len(by_sharing['upper'])
        n_l = len(by_sharing['lower'])
        n_n = len(by_sharing['neither'])

        print(f"  d={d:>5} {upper:>10.5f} {lower:>10.5f} {neither:>10.5f} "
              f"{overall:>10.5f} {n_u+n_l+n_n:>8}")

        results[d] = {
            'upper': float(upper) if not np.isnan(upper) else None,
            'lower': float(lower) if not np.isnan(lower) else None,
            'neither': float(neither) if not np.isnan(neither) else None,
            'overall': float(overall),
            'counts': {'upper': n_u, 'lower': n_l, 'neither': n_n},
        }

    # Overall by sharing type
    print(f"\n  Overall by trigram sharing (all Hamming distances):")
    for sharing in ['upper', 'lower', 'neither']:
        vals = overall_by_sharing[sharing]
        if vals:
            print(f"    Share {sharing:>8}: mean={np.mean(vals):.5f} ± {np.std(vals):.5f} (n={len(vals)})")

    # Excluding complements (d=6)
    print(f"\n  Excluding complements (d=1..5 only):")
    for sharing in ['upper', 'lower', 'neither']:
        vals = []
        for d in range(1, 6):
            for h1, h2 in pairs_by_d[d]:
                if trigram_sharing(h1, h2) == sharing:
                    vals.append(cos_dist(centroids[h1], centroids[h2]))
        if vals:
            print(f"    Share {sharing:>8}: mean={np.mean(vals):.5f} ± {np.std(vals):.5f} (n={len(vals)})")

    return results


# ═══════════════════════════════════════════════════════
# Test 4: Hamming=5 (Near-Complement) Analysis
# ═══════════════════════════════════════════════════════

def test_hamming5(residual, atlas):
    """Detailed analysis of Hamming-5 pairs (near-complements)."""
    print(f"\n{'='*70}")
    print("TEST 4: HAMMING=5 (NEAR-COMPLEMENT) ANALYSIS")
    print(f"{'='*70}")

    centroids = np.array([residual[h * 6:(h + 1) * 6].mean(axis=0) for h in range(64)])
    pairs_by_d = build_pairs_by_hamming()

    # Full Hamming spectrum for context
    print(f"\n  Hamming distance vs mean thematic distance (hex centroids):")
    print(f"  {'d':>3} {'Mean cos dist':>14} {'Std':>10} {'n_pairs':>8}")
    print(f"  {'-'*38}")
    for d in range(1, 7):
        dists = [cos_dist(centroids[h1], centroids[h2]) for h1, h2 in pairs_by_d[d]]
        is_comp = " (complements)" if d == 6 else ""
        print(f"  {d:>3} {np.mean(dists):>14.5f} {np.std(dists):>10.5f} {len(dists):>8}{is_comp}")

    # Hamming=5 details: which bit is NOT flipped?
    h5_pairs = pairs_by_d[5]
    print(f"\n  Hamming-5 pairs grouped by the UN-flipped position:")

    by_kept_pos = defaultdict(list)
    for h1, h2 in h5_pairs:
        diff = h1 ^ h2
        # The bit NOT flipped is the one that's 0 in diff (among the 6 bits)
        kept = [k for k in range(6) if not (diff & (1 << k))]
        assert len(kept) == 1
        kept_pos = kept[0]
        cd = cos_dist(centroids[h1], centroids[h2])
        by_kept_pos[kept_pos].append((h1, h2, cd))

    line_names = ['初', '二', '三', '四', '五', '上']
    print(f"  {'Kept pos':<10} {'Line':<5} {'Mean dist':>10} {'Std':>10} {'n':>5}")
    print(f"  {'-'*42}")
    for pos in range(6):
        pairs = by_kept_pos[pos]
        dists = [p[2] for p in pairs]
        print(f"  {pos:<10} {line_names[pos]:<5} {np.mean(dists):>10.5f} "
              f"{np.std(dists):>10.5f} {len(dists):>5}")

    # Compare Hamming-5 to non-complement Hamming-1..4
    print(f"\n  Non-complement Hamming distance spectrum:")
    for d in range(1, 6):
        dists = [cos_dist(centroids[h1], centroids[h2]) for h1, h2 in pairs_by_d[d]]
        print(f"    d={d}: mean={np.mean(dists):.5f}")

    # Correlation: Hamming distance vs thematic distance (excl complements)
    all_hamming = []
    all_thematic = []
    for d in range(1, 6):
        for h1, h2 in pairs_by_d[d]:
            all_hamming.append(d)
            all_thematic.append(cos_dist(centroids[h1], centroids[h2]))

    r, p = pearsonr(all_hamming, all_thematic)
    rho, p_s = spearmanr(all_hamming, all_thematic)
    print(f"\n  Hamming vs thematic (d=1..5, {len(all_hamming)} pairs):")
    print(f"    Pearson r={r:+.4f} (p={p:.4e})")
    print(f"    Spearman ρ={rho:+.4f} (p={p_s:.4e})")

    # Also with complements
    for h1, h2 in pairs_by_d[6]:
        all_hamming.append(6)
        all_thematic.append(cos_dist(centroids[h1], centroids[h2]))
    r_full, p_full = pearsonr(all_hamming, all_thematic)
    rho_full, p_s_full = spearmanr(all_hamming, all_thematic)
    print(f"\n  Hamming vs thematic (d=1..6, {len(all_hamming)} pairs):")
    print(f"    Pearson r={r_full:+.4f} (p={p_full:.4e})")
    print(f"    Spearman ρ={rho_full:+.4f} (p={p_s_full:.4e})")

    return {
        'spectrum': {d: float(np.mean([cos_dist(centroids[h1], centroids[h2])
                                        for h1, h2 in pairs_by_d[d]]))
                     for d in range(1, 7)},
        'h5_by_kept': {pos: float(np.mean([p[2] for p in by_kept_pos[pos]]))
                       for pos in range(6)},
        'pearson_excl_comp': float(r),
        'pearson_p_excl': float(p),
        'pearson_incl_comp': float(r_full),
        'pearson_p_incl': float(p_full),
    }


# ═══════════════════════════════════════════════════════
# Test 5: Cross-Model Verification
# ═══════════════════════════════════════════════════════

def test_cross_model():
    """Run line-level and position analyses for all 3 models."""
    print(f"\n{'='*70}")
    print("TEST 5: CROSS-MODEL VERIFICATION")
    print(f"{'='*70}")

    cross_results = {}

    for shortname in MODELS:
        print(f"\n--- {shortname} ---")
        residual, atlas = load_residuals_for_model(shortname)

        # Line mechanism
        r1 = test_line_mechanism(residual, atlas, label=shortname)

        # Hamming spectrum + correlation
        centroids = np.array([residual[h * 6:(h + 1) * 6].mean(axis=0) for h in range(64)])
        pairs_by_d = build_pairs_by_hamming()

        spectrum = {}
        all_h, all_t = [], []
        for d in range(1, 7):
            dists = [cos_dist(centroids[h1], centroids[h2]) for h1, h2 in pairs_by_d[d]]
            spectrum[d] = float(np.mean(dists))
            for h1, h2 in pairs_by_d[d]:
                all_h.append(d)
                all_t.append(cos_dist(centroids[h1], centroids[h2]))

        r_full, p_full = pearsonr(all_h, all_t)

        # Excl complements
        all_h_nc = [h for h, d in zip(all_h, range(len(all_h))) if all_h[d] < 6]
        all_t_nc = [t for h, t in zip(all_h, all_t) if h < 6]
        r_nc, p_nc = pearsonr(all_h_nc, all_t_nc)

        print(f"\n  Hamming spectrum:")
        for d in range(1, 7):
            print(f"    d={d}: {spectrum[d]:.5f}")
        print(f"  Pearson (d=1..5): r={r_nc:+.4f} (p={p_nc:.4e})")
        print(f"  Pearson (d=1..6): r={r_full:+.4f} (p={p_full:.4e})")

        cross_results[shortname] = {
            'line_mechanism': r1,
            'spectrum': spectrum,
            'pearson_excl': float(r_nc),
            'pearson_p_excl': float(p_nc),
            'pearson_incl': float(r_full),
            'pearson_p_incl': float(p_full),
        }

    return cross_results


# ═══════════════════════════════════════════════════════
# Report
# ═══════════════════════════════════════════════════════

def write_report(r1, r2, r3, r4, r5):
    """Write markdown summary."""
    lines = [
        "# Phase 7: Hamming-Thematic Anti-Correlation Deep Dive",
        "",
        "## Test 1: Line-Level Mechanism (BGE-M3, Hamming-1 pairs)",
        "",
        "192 Hamming-1 pairs: each differs at exactly one line position.",
        "",
        f"- Changed line mean cosine dist: **{r1['changed_mean']:.5f}**",
        f"- Shared lines mean cosine dist: **{r1['shared_mean']:.5f}**",
        f"- Hex centroid cosine dist: {r1['hex_mean']:.5f}",
        f"- Ratio changed/shared: **{r1['changed_mean']/r1['shared_mean']:.3f}**",
        "",
        "### Per-position breakdown",
        "",
        "| Position | Line | Changed | Shared | Hex dist | Ratio |",
        "|----------|------|--------:|-------:|---------:|------:|",
    ]
    line_names = ['初', '二', '三', '四', '五', '上']
    for pos in range(6):
        cd = r1['per_pos_changed'][pos]
        sd = r1['per_pos_shared'][pos]
        hd = r1['per_pos_hex'][pos]
        ratio = cd / sd if sd > 0 else 0
        lines.append(f"| {pos} | {line_names[pos]} | {cd:.5f} | {sd:.5f} | {hd:.5f} | {ratio:.3f} |")

    # Test 2
    lines += [
        "",
        "## Test 2: Position Dependence",
        "",
        "| Position | Line | Overall | When changed | When shared | Δ |",
        "|----------|------|--------:|------------:|-----------:|--:|",
    ]
    for pos in range(6):
        r = r2[pos]
        lines.append(f"| {pos} | {line_names[pos]} | {r['overall']:.5f} | "
                     f"{r['changed']:.5f} | {r['shared']:.5f} | {r['delta']:+.5f} |")

    # Test 3
    lines += [
        "",
        "## Test 3: Trigram-Level Analysis",
        "",
        "| Hamming | Share upper | Share lower | Neither | Overall |",
        "|--------:|-----------:|-----------:|--------:|--------:|",
    ]
    for d in range(1, 7):
        r = r3[d]
        u = f"{r['upper']:.5f}" if r['upper'] is not None else "—"
        l = f"{r['lower']:.5f}" if r['lower'] is not None else "—"
        n = f"{r['neither']:.5f}" if r['neither'] is not None else "—"
        lines.append(f"| {d} | {u} | {l} | {n} | {r['overall']:.5f} |")

    # Test 4
    lines += [
        "",
        "## Test 4: Hamming Distance Spectrum",
        "",
        "| d | Mean cos dist |",
        "|--:|--------------:|",
    ]
    for d in range(1, 7):
        tag = " (complements)" if d == 6 else ""
        lines.append(f"| {d} | {r4['spectrum'][d]:.5f}{tag} |")

    lines += [
        "",
        f"- Pearson (d=1..5, excl complements): r={r4['pearson_excl_comp']:+.4f} (p={r4['pearson_p_excl']:.2e})",
        f"- Pearson (d=1..6, incl complements): r={r4['pearson_incl_comp']:+.4f} (p={r4['pearson_p_incl']:.2e})",
        "",
        "### Hamming-5 by un-flipped position",
        "",
        "| Kept pos | Line | Mean dist |",
        "|---------:|------:|----------:|",
    ]
    for pos in range(6):
        lines.append(f"| {pos} | {line_names[pos]} | {r4['h5_by_kept'][pos]:.5f} |")

    # Test 5: cross-model
    lines += [
        "",
        "## Test 5: Cross-Model Summary",
        "",
        "| Metric | bge-m3 | e5-large | labse |",
        "|--------|-------:|--------:|------:|",
    ]
    # Hamming spectrum per model
    for d in range(1, 7):
        vals = [f"{r5[m]['spectrum'][d]:.5f}" for m in MODELS]
        tag = " (comp)" if d == 6 else ""
        lines.append(f"| d={d} dist{tag} | " + " | ".join(vals) + " |")
    # Correlations
    vals_excl = [f"{r5[m]['pearson_excl']:+.4f}" for m in MODELS]
    vals_incl = [f"{r5[m]['pearson_incl']:+.4f}" for m in MODELS]
    lines.append(f"| Pearson (d=1..5) | " + " | ".join(vals_excl) + " |")
    lines.append(f"| Pearson (d=1..6) | " + " | ".join(vals_incl) + " |")
    # Line mechanism
    vals_ch = [f"{r5[m]['line_mechanism']['changed_mean']:.5f}" for m in MODELS]
    vals_sh = [f"{r5[m]['line_mechanism']['shared_mean']:.5f}" for m in MODELS]
    vals_ratio = [f"{r5[m]['line_mechanism']['changed_mean']/r5[m]['line_mechanism']['shared_mean']:.3f}" for m in MODELS]
    lines.append(f"| Changed line dist | " + " | ".join(vals_ch) + " |")
    lines.append(f"| Shared lines dist | " + " | ".join(vals_sh) + " |")
    lines.append(f"| Ratio changed/shared | " + " | ".join(vals_ratio) + " |")

    lines.append("")

    out_path = OUT_DIR / "phase7_hamming_results.md"
    out_path.write_text("\n".join(lines))
    print(f"\nReport saved to {out_path}")


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    print("Q1 Phase 7: Hamming-Thematic Anti-Correlation Deep Dive")
    print("=" * 70)

    # Primary analysis with BGE-M3
    residual, atlas = load_residuals_for_model('bge-m3')

    r1 = test_line_mechanism(residual, atlas)
    r2 = test_position_dependence(residual, atlas)
    r3 = test_trigram_analysis(residual, atlas)
    r4 = test_hamming5(residual, atlas)

    # Cross-model
    r5 = test_cross_model()

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"""
Line-Level Mechanism (Hamming-1, BGE-M3):
  Changed line:  {r1['changed_mean']:.5f}
  Shared lines:  {r1['shared_mean']:.5f}
  Ratio:         {r1['changed_mean']/r1['shared_mean']:.3f}

Hamming Spectrum (BGE-M3):
  d=1: {r4['spectrum'][1]:.5f}  d=2: {r4['spectrum'][2]:.5f}  d=3: {r4['spectrum'][3]:.5f}
  d=4: {r4['spectrum'][4]:.5f}  d=5: {r4['spectrum'][5]:.5f}  d=6: {r4['spectrum'][6]:.5f} (comp)

Anti-correlation (excl complements): r={r4['pearson_excl_comp']:+.4f} (p={r4['pearson_p_excl']:.2e})
Anti-correlation (incl complements): r={r4['pearson_incl_comp']:+.4f} (p={r4['pearson_p_incl']:.2e})

Cross-model Pearson (d=1..5):
  bge-m3:   {r5['bge-m3']['pearson_excl']:+.4f}
  e5-large: {r5['e5-large']['pearson_excl']:+.4f}
  labse:    {r5['labse']['pearson_excl']:+.4f}
""")

    write_report(r1, r2, r3, r4, r5)


if __name__ == '__main__':
    main()
