#!/usr/bin/env python3
"""Q1 Phase 5: Syntactic Frame Classification of 爻辭.

Tests whether syntactic frames (directive, conditional, locative, motion,
state-description) correlate with embedding geometry — the last clean
mechanical test available.

Phase 1: Classify each of 384 lines by syntactic frame (binary vector)
Phase 2: Test frame vectors against embedding geometry
Phase 3: Characterize which frames carry signal (or report null)
"""

import json
import numpy as np
from pathlib import Path
from collections import Counter, defaultdict
from scipy.spatial.distance import pdist, squareform
from scipy.stats import pearsonr, spearmanr, mannwhitneyu, chi2 as chi2_dist

Q1 = Path(__file__).resolve().parent
ICHING = Q1.parent.parent  # memories/iching
MEMORIES = ICHING.parent   # memories
YAOCI = MEMORIES / "texts" / "iching" / "yaoci.json"
ATLAS = ICHING / "atlas" / "atlas.json"
EMBEDDINGS = ICHING / "synthesis" / "embeddings.npz"

N_HEX = 64
N_LINES = 6
N_TOTAL = N_HEX * N_LINES  # 384

# ═══════════════════════════════════════════════════════
# Frame Definitions
# ═══════════════════════════════════════════════════════
#
# Each frame is defined by markers — specific characters/bigrams.
# A line can match multiple frames (binary vector).
# Classification is purely mechanical: marker present → frame tagged.

FRAME_DEFS = {
    'directive': {
        'description': 'Prescriptive/proscriptive instruction',
        'markers': ['利', '勿', '不可', '宜'],
    },
    'conditional': {
        'description': 'If/when construction',
        'markers': ['若', '如', '則'],
        # Note: 如 in classical Chinese often means "like/as if" not "if",
        # but both are compositional frame markers
    },
    'locative': {
        'description': 'Spatial placement (at/in X)',
        'markers': ['在', '于'],
    },
    'motion': {
        'description': 'Movement/travel verb',
        'markers': ['往', '來', '征', '行', '涉', '入', '出'],
    },
    'negation': {
        'description': 'Explicit negation',
        'markers': ['不', '勿', '弗', '匪', '无', '無'],
    },
}

FRAME_NAMES = list(FRAME_DEFS.keys())
N_FRAMES = len(FRAME_NAMES)

# Lines with no markers at all are classified as 'state_description' (pure imagery)
# This is a derived feature, not a marker-based frame


def classify_line(text):
    """Classify a line into frame types. Returns binary vector."""
    vec = np.zeros(N_FRAMES, dtype=int)
    for fi, fname in enumerate(FRAME_NAMES):
        markers = FRAME_DEFS[fname]['markers']
        for m in markers:
            if m in text:
                vec[fi] = 1
                break
    return vec


# ═══════════════════════════════════════════════════════
# Data Loading
# ═══════════════════════════════════════════════════════

def load_data():
    """Load yaoci texts, atlas, and embeddings. Return in hex_val order."""
    with open(YAOCI) as f:
        yaoci = json.load(f)
    with open(ATLAS) as f:
        atlas = json.load(f)

    # Build kw→hv mapping
    kw_to_hv = {}
    for hv in range(N_HEX):
        kw = atlas[str(hv)]['kw_number']
        kw_to_hv[kw] = hv

    # Texts in hex_val order
    line_texts = [''] * N_TOTAL
    hex_names = [''] * N_HEX
    for kw in range(1, N_HEX + 1):
        hv = kw_to_hv[kw]
        entry = yaoci['entries'][kw - 1]
        hex_names[hv] = entry['name']
        for li in range(N_LINES):
            line_texts[hv * N_LINES + li] = entry['lines'][li]['text']

    # Embeddings in hex_val order
    emb_data = np.load(str(EMBEDDINGS))
    yaoci_emb = emb_data['yaoci']  # (384, 1024), kw order
    emb_reordered = np.zeros_like(yaoci_emb)
    for kw in range(1, N_HEX + 1):
        hv = kw_to_hv[kw]
        for li in range(N_LINES):
            emb_reordered[hv * N_LINES + li] = yaoci_emb[(kw - 1) * N_LINES + li]

    return line_texts, hex_names, atlas, emb_reordered


# ═══════════════════════════════════════════════════════
# Phase 1: Classification
# ═══════════════════════════════════════════════════════

def phase1_classify(line_texts):
    """Classify all 384 lines by syntactic frame."""
    print("=" * 70)
    print("PHASE 1: Syntactic Frame Classification")
    print("=" * 70)

    # Classify each line
    frame_matrix = np.zeros((N_TOTAL, N_FRAMES), dtype=int)
    for i, text in enumerate(line_texts):
        frame_matrix[i] = classify_line(text)

    # Derived feature: state_description = no markers at all
    is_state = (frame_matrix.sum(axis=1) == 0).astype(int)

    # Stats
    print(f"\n  Frame distribution across {N_TOTAL} lines:")
    print(f"  {'Frame':<16} {'Lines':>6} {'%':>7}")
    print(f"  {'-' * 31}")
    for fi, fname in enumerate(FRAME_NAMES):
        n = frame_matrix[:, fi].sum()
        pct = 100 * n / N_TOTAL
        print(f"  {fname:<16} {n:>6} {pct:>6.1f}%")
    n_state = is_state.sum()
    print(f"  {'state_desc':<16} {n_state:>6} {100*n_state/N_TOTAL:>6.1f}%")

    # Co-occurrence of frames
    print(f"\n  Frame co-occurrence:")
    for i in range(N_FRAMES):
        for j in range(i + 1, N_FRAMES):
            both = ((frame_matrix[:, i] == 1) & (frame_matrix[:, j] == 1)).sum()
            if both > 0:
                print(f"    {FRAME_NAMES[i]} + {FRAME_NAMES[j]}: {both} lines")

    # Lines per frame count
    frame_counts = frame_matrix.sum(axis=1)
    print(f"\n  Frames per line: "
          f"0={n_state}, 1={(frame_counts==1).sum()}, "
          f"2={(frame_counts==2).sum()}, 3+={(frame_counts>=3).sum()}")

    # Unique frame profiles
    profiles = set(tuple(row) for row in frame_matrix)
    print(f"  Distinct frame profiles: {len(profiles)}")

    return frame_matrix, is_state


# ═══════════════════════════════════════════════════════
# Phase 2: Test Against Embedding Geometry
# ═══════════════════════════════════════════════════════

def phase2_test(frame_matrix, is_state, emb, atlas, line_texts):
    """Test syntactic frames against embedding geometry."""
    print("\n" + "=" * 70)
    print("PHASE 2: Frame Vectors vs Embedding Geometry")
    print("=" * 70)

    # Add state_description as a column
    full_matrix = np.hstack([frame_matrix, is_state.reshape(-1, 1)])
    full_names = FRAME_NAMES + ['state_desc']
    n_full = full_matrix.shape[1]

    # ─── 2a: Line-level Mantel test ───
    print(f"\n  --- 2a: Line-Level Mantel Test (384×384) ---")

    # Use Hamming for frame distance, cosine for embedding
    frame_dist = pdist(full_matrix, metric='hamming')
    emb_dist = pdist(emb, metric='cosine')

    r_line, p_line = pearsonr(frame_dist, emb_dist)
    rs_line, ps_line = spearmanr(frame_dist, emb_dist)
    print(f"  Pearson r={r_line:.4f}, p={p_line:.4g}")
    print(f"  Spearman ρ={rs_line:.4f}, p={ps_line:.4g}")

    # Permutation test
    n_perm = 4999
    count = 0
    for _ in range(n_perm):
        perm = np.random.permutation(N_TOTAL)
        r_perm = np.corrcoef(pdist(emb[perm], metric='cosine'), frame_dist)[0, 1]
        if r_perm >= r_line:
            count += 1
    p_perm_line = (count + 1) / (n_perm + 1)
    print(f"  Permutation p ({n_perm} perms): {p_perm_line:.4f}")

    # ─── 2b: Hexagram-level Mantel test ───
    print(f"\n  --- 2b: Hexagram-Level Mantel Test (64×64) ---")

    # Aggregate frames per hexagram (sum across 6 lines)
    hex_frames = np.zeros((N_HEX, n_full))
    hex_centroids = np.zeros((N_HEX, emb.shape[1]))
    for hv in range(N_HEX):
        start = hv * N_LINES
        hex_frames[hv] = full_matrix[start:start + N_LINES].sum(axis=0)
        hex_centroids[hv] = emb[start:start + N_LINES].mean(axis=0)

    hex_frame_dist = pdist(hex_frames, metric='cosine')
    hex_emb_dist = pdist(hex_centroids, metric='cosine')

    # Remove NaN from frame_dist (hexagrams with identical frame profiles → cosine=0/nan)
    valid = ~(np.isnan(hex_frame_dist) | np.isnan(hex_emb_dist))
    if valid.sum() < len(hex_frame_dist):
        print(f"  Warning: {(~valid).sum()} NaN distances removed (identical frame profiles)")

    r_hex, p_hex = pearsonr(hex_frame_dist[valid], hex_emb_dist[valid])
    rs_hex, ps_hex = spearmanr(hex_frame_dist[valid], hex_emb_dist[valid])
    print(f"  Pearson r={r_hex:.4f}, p={p_hex:.4g}")
    print(f"  Spearman ρ={rs_hex:.4f}, p={ps_hex:.4g}")

    # Permutation
    count_hex = 0
    for _ in range(n_perm):
        perm = np.random.permutation(N_HEX)
        d_perm = pdist(hex_centroids[perm], metric='cosine')
        v = ~(np.isnan(hex_frame_dist) | np.isnan(d_perm))
        r_p = np.corrcoef(d_perm[v], hex_frame_dist[v])[0, 1]
        if not np.isnan(r_p) and r_p >= r_hex:
            count_hex += 1
    p_perm_hex = (count_hex + 1) / (n_perm + 1)
    print(f"  Permutation p: {p_perm_hex:.4f}")

    # Also try Euclidean distance for frames (more suitable for count data)
    hex_frame_dist_euc = pdist(hex_frames, metric='euclidean')
    r_hex_e, p_hex_e = pearsonr(hex_frame_dist_euc, hex_emb_dist)
    print(f"\n  (Euclidean frame dist) Pearson r={r_hex_e:.4f}, p={p_hex_e:.4g}")

    # ─── 2c: Complement-specific test ───
    print(f"\n  --- 2c: Complement Pair Frame Profiles ---")

    comp_pairs = []
    for hv in range(N_HEX):
        cv = int(atlas[str(hv)]['complement'])
        if hv < cv:
            comp_pairs.append((hv, cv))

    # Frame difference per complement pair
    comp_frame_diffs = np.array([hex_frames[h] - hex_frames[c] for h, c in comp_pairs])

    # Random pair frame differences
    all_pairs = [(i, j) for i in range(N_HEX) for j in range(i + 1, N_HEX)
                 if (i, j) not in set(comp_pairs)]
    rand_frame_diffs = np.array([hex_frames[i] - hex_frames[j] for i, j in all_pairs])

    # Compare magnitudes: do complement pairs differ MORE in frame profile?
    comp_norms = np.linalg.norm(comp_frame_diffs, axis=1)
    rand_norms = np.linalg.norm(rand_frame_diffs, axis=1)
    u_stat, p_u = mannwhitneyu(comp_norms, rand_norms, alternative='two-sided')
    print(f"  Complement frame diff magnitude: mean={comp_norms.mean():.3f}, std={comp_norms.std():.3f}")
    print(f"  Random pair frame diff magnitude: mean={rand_norms.mean():.3f}, std={rand_norms.std():.3f}")
    print(f"  Mann-Whitney U={u_stat:.0f}, p={p_u:.4g}")

    # Per-frame: which frames differ between complements?
    print(f"\n  Per-frame complement contrast:")
    for fi, fname in enumerate(full_names):
        comp_vals = comp_frame_diffs[:, fi]
        mean_abs = np.abs(comp_vals).mean()
        # How often does the frame count differ?
        n_diff = (comp_vals != 0).sum()
        print(f"    {fname:<16}: mean|diff|={mean_abs:.2f}, differs in {n_diff}/32 pairs")

    # ─── 2d: Position × Frame cross-tabulation ───
    print(f"\n  --- 2d: Position × Frame Cross-tabulation ---")

    pos_frame = np.zeros((N_LINES, n_full), dtype=int)
    for i in range(N_TOTAL):
        pos = i % N_LINES
        pos_frame[pos] += full_matrix[i]

    print(f"\n  {'Frame':<16}" + ''.join(f"{'L'+str(p+1):>6}" for p in range(N_LINES)) + f"{'Total':>8}")
    print(f"  {'-' * (16 + 6*N_LINES + 8)}")
    for fi, fname in enumerate(full_names):
        row = pos_frame[:, fi]
        total = row.sum()
        cells = ''.join(f"{v:>6}" for v in row)
        print(f"  {fname:<16}{cells}{total:>8}")

    # χ² test per frame
    print(f"\n  Position bias (χ² goodness-of-fit):")
    for fi, fname in enumerate(full_names):
        row = pos_frame[:, fi]
        total = row.sum()
        if total < 6:
            continue
        expected = np.full(N_LINES, total / N_LINES)
        chi2_val = np.sum((row - expected) ** 2 / expected)
        p_chi2 = 1 - chi2_dist.cdf(chi2_val, N_LINES - 1)
        sig = '*' if p_chi2 < 0.05 else ''
        print(f"    {fname:<16}: χ²={chi2_val:.2f}, p={p_chi2:.4g} {sig}")

    # ─── 2e: Per-frame embedding prediction ───
    print(f"\n  --- 2e: Per-Frame Embedding Prediction ---")
    print(f"  Does distance within a single frame predict embedding distance?")

    for fi, fname in enumerate(full_names):
        # Binary single-frame distance
        col = full_matrix[:, fi].reshape(-1, 1)
        f_dist = pdist(col, metric='hamming')
        r_f, p_f = pearsonr(emb_dist, f_dist)
        sig = '*' if p_f < 0.05 else ('**' if p_f < 0.01 else '')
        print(f"    {fname:<16}: Pearson r={r_f:>+.4f}, p={p_f:.4g} {sig}")

    return {
        'line_mantel': {'r': r_line, 'p': p_line, 'p_perm': p_perm_line},
        'hex_mantel': {'r': r_hex, 'p': p_hex, 'p_perm': p_perm_hex,
                       'r_euc': r_hex_e, 'p_euc': p_hex_e},
        'complement': {'comp_mean': comp_norms.mean(), 'rand_mean': rand_norms.mean(),
                       'U': u_stat, 'p': p_u},
        'pos_frame': pos_frame.tolist(),
    }


# ═══════════════════════════════════════════════════════
# Phase 3: Interpretation
# ═══════════════════════════════════════════════════════

def phase3_interpret(frame_matrix, is_state, emb, atlas, results):
    """Characterize results or report null."""
    print("\n" + "=" * 70)
    print("PHASE 3: Interpretation")
    print("=" * 70)

    p_line = results['line_mantel']['p_perm']
    p_hex = results['hex_mantel']['p_perm']
    r_line = results['line_mantel']['r']
    r_hex = results['hex_mantel']['r']

    if p_line < 0.05 or p_hex < 0.05:
        print(f"\n  *** SIGNIFICANT correlation detected ***")
        print(f"  Line-level: r={r_line:.4f}, p_perm={p_line:.4f}")
        print(f"  Hex-level:  r={r_hex:.4f}, p_perm={p_hex:.4f}")
        print(f"\n  Syntactic frames capture SOME embedding structure.")
        print(f"  This breaks the triple dissociation — compositional pattern matters.")
    else:
        print(f"\n  No significant correlation.")
        print(f"  Line-level: r={r_line:.4f}, p_perm={p_line:.4f}")
        print(f"  Hex-level:  r={r_hex:.4f}, p_perm={p_hex:.4f}")
        print(f"\n  QUADRUPLE DISSOCIATION confirmed:")
        print(f"    1. Algebra (R119): r ≈ 0")
        print(f"    2. Vocabulary (R135): p = 0.897")
        print(f"    3. 說卦傳 象 (R146): r = -0.003")
        print(f"    4. Syntactic frames: r = {r_line:.4f}")
        print(f"\n  The 爻辭 embedding geometry is irreducible to ANY mechanical analysis.")
        print(f"  It lives in the sub-syntactic compositional texture of the text —")
        print(f"  how characters combine to create meaning, below the level of")
        print(f"  detectable vocabulary, grammar, or symbolic associations.")


# ═══════════════════════════════════════════════════════
# Results Writer
# ═══════════════════════════════════════════════════════

def write_results(frame_matrix, is_state, results, line_texts):
    """Write phase5_results.md."""
    lines = []
    w = lines.append

    full_matrix = np.hstack([frame_matrix, is_state.reshape(-1, 1)])
    full_names = FRAME_NAMES + ['state_desc']

    w("# Q1 Phase 5: Syntactic Frame Analysis — Results\n")

    w("## Phase 1: Frame Classification\n")
    w(f"- **{N_TOTAL} lines** classified across {N_FRAMES} marker-based frames + state_description")
    w(f"- Classification is purely mechanical: marker present → frame tagged\n")

    w("| Frame | Markers | Lines | % |")
    w("|-------|---------|-------|---|")
    for fi, fname in enumerate(FRAME_NAMES):
        markers = ', '.join(FRAME_DEFS[fname]['markers'])
        n = frame_matrix[:, fi].sum()
        pct = 100 * n / N_TOTAL
        w(f"| {fname} | {markers} | {n} | {pct:.1f}% |")
    n_state = is_state.sum()
    w(f"| state_desc | (no markers) | {n_state} | {100*n_state/N_TOTAL:.1f}% |")

    frame_counts = frame_matrix.sum(axis=1)
    w(f"\n- Frames per line: 0={n_state}, 1={(frame_counts==1).sum()}, "
      f"2={(frame_counts==2).sum()}, 3+={(frame_counts>=3).sum()}")

    w("\n## Phase 2: Correlation Tests\n")

    w("### 2a: Line-Level Mantel Test (384×384)\n")
    m = results['line_mantel']
    w(f"- Pearson r = {m['r']:.4f}")
    w(f"- p (parametric) = {m['p']:.4g}")
    w(f"- **p (permutation) = {m['p_perm']:.4f}**")

    w("\n### 2b: Hexagram-Level Mantel Test (64×64)\n")
    m = results['hex_mantel']
    w(f"- Pearson r = {m['r']:.4f} (cosine frame dist)")
    w(f"- p (permutation) = {m['p_perm']:.4f}")
    w(f"- Euclidean frame dist: r = {m['r_euc']:.4f}, p = {m['p_euc']:.4g}")

    w("\n### 2c: Complement Pair Frame Profiles\n")
    c = results['complement']
    w(f"- Complement frame diff magnitude: {c['comp_mean']:.3f}")
    w(f"- Random pair frame diff magnitude: {c['rand_mean']:.3f}")
    w(f"- Mann-Whitney p = {c['p']:.4g}")

    w("\n### 2d: Position × Frame\n")
    pos_frame = np.array(results['pos_frame'])
    w("| Frame | L1 | L2 | L3 | L4 | L5 | L6 |")
    w("|-------|----|----|----|----|----|----| ")
    for fi, fname in enumerate(full_names):
        row = pos_frame[:, fi]
        w(f"| {fname} | {' | '.join(str(v) for v in row)} |")

    w("\n## Interpretation\n")

    p_line = results['line_mantel']['p_perm']
    p_hex = results['hex_mantel']['p_perm']
    r_line = results['line_mantel']['r']

    if p_line < 0.05 or p_hex < 0.05:
        w("**Syntactic frames correlate with embedding geometry.**\n")
        w("Compositional pattern (how markers frame the imagery) captures structure "
          "that vocabulary, 象, and algebra miss. The triple dissociation is broken — "
          "the residual has a syntactic component.")
    else:
        w("**Syntactic frames do NOT predict embedding geometry.**\n")
        w("**Quadruple dissociation** confirmed:\n")
        w("| Layer | Test | r | p |")
        w("|-------|------|---|---|")
        w("| 1. Algebra | R119/R125 | ≈ 0 | > 0.40 |")
        w("| 2. Vocabulary | R135 | — | 0.897 |")
        w("| 3. 說卦傳 象 | R146 | -0.003 | 0.543 |")
        w(f"| 4. Syntactic frames | This test | {r_line:.4f} | {p_line:.4f} |")
        w("\nThe embedding geometry is irreducible to any mechanically extractable feature. "
          "It lives in the sub-syntactic compositional texture — how characters combine "
          "to create situated meaning, below the level of grammar, vocabulary, or "
          "symbolic association.")

    with open(Q1 / 'phase5_results.md', 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"\n  Results written to {Q1 / 'phase5_results.md'}")


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    line_texts, hex_names, atlas, emb = load_data()

    # Phase 1
    frame_matrix, is_state = phase1_classify(line_texts)

    # Phase 2
    results = phase2_test(frame_matrix, is_state, emb, atlas, line_texts)

    # Phase 3
    phase3_interpret(frame_matrix, is_state, emb, atlas, results)

    # Write results
    write_results(frame_matrix, is_state, results, line_texts)

    print("\n" + "=" * 70)
    print("DONE — Q1 Phase 5 complete.")
    print("=" * 70)


if __name__ == '__main__':
    main()
