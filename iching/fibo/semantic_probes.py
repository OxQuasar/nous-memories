#!/usr/bin/env python3
"""
Semantic Probe Vectors Against Complement Opposition Space
===========================================================
Tests whether specific vocabulary-based semantic axes align with the
complement opposition directions in embedding space.

8 probes × (yaoci: 4 models, guaci: 1 model) = 40 cells.
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent          # memories/iching
TEXTS = ROOT.parent / "texts" / "iching"
ATLAS_PATH = ROOT / "atlas" / "atlas.json"
Q1_DIR = ROOT / "reversal" / "Q1"
SYNTH_DIR = ROOT / "synthesis"

N_HEX = 64
N_LINES = 6
N_PERM = 10_000

# ── Data loading ─────────────────────────────────────────────

def load_atlas():
    atlas = json.load(open(ATLAS_PATH))
    # Build hex_val → kw_number and kw_number → hex_val
    hex_to_kw = {int(k): v['kw_number'] for k, v in atlas.items() if k.isdigit()}
    kw_to_hex = {v: k for k, v in hex_to_kw.items()}
    return atlas, hex_to_kw, kw_to_hex

def load_complement_pairs(atlas):
    """Return list of 32 (h_lo, h_hi) complement pairs with h_lo < h_hi."""
    pairs = []
    seen = set()
    for h in range(N_HEX):
        c = atlas[str(h)]['complement']
        pair = (min(h, c), max(h, c))
        if pair not in seen:
            pairs.append(pair)
            seen.add(pair)
    assert len(pairs) == 32
    return pairs

def load_texts_by_hex(hex_to_kw):
    """Load yaoci and guaci texts, indexed by hex_val (0-63)."""
    yaoci_data = json.load(open(TEXTS / "yaoci.json"))['entries']
    guaci_data = json.load(open(TEXTS / "guaci.json"))['entries']

    # Build kw_number → entry
    yaoci_by_kw = {e['number']: e for e in yaoci_data}
    guaci_by_kw = {e['number']: e for e in guaci_data}

    yaoci_texts = {}  # hex_val → list of 6 line texts
    guaci_texts = {}  # hex_val → single text

    for h in range(N_HEX):
        kw = hex_to_kw[h]
        yaoci_texts[h] = [line['text'] for line in yaoci_by_kw[kw]['lines']]
        guaci_texts[h] = guaci_by_kw[kw]['text']

    return yaoci_texts, guaci_texts

def load_embeddings():
    """Load all available embeddings.
    Returns dict: model_name → dict with 'yaoci' (384×d) and optionally 'guaci' (64×d).
    All ordered by hex_val (0-63).
    """
    models = {}

    # Q1 cached yaoci: 4 models
    for name in ['bge-m3', 'e5-large', 'labse', 'sikuroberta']:
        data = np.load(Q1_DIR / f"embeddings_{name}.npz")
        models[name] = {'yaoci': data['yaoci']}  # (384, d)

    # Synthesis has guaci for bge-m3
    synth = np.load(SYNTH_DIR / "embeddings.npz")
    models['bge-m3']['guaci'] = synth['guaci']  # (64, 1024)

    return models


# ── Probe definitions ────────────────────────────────────────

# Each probe: (name, positive_tokens, negative_tokens) or custom function
# 吉凶, 利, 往來, 貞, 社會, 時間, 長度, 否定

PROBES = [
    ("吉凶 valence",    ['吉', '元吉', '大吉', '無咎'],   ['凶', '厲', '悔', '吝']),
    ("利 favorability", ['利'],                            ['不利']),
    ("往來 direction",  ['往'],                            ['來']),
    ("貞 frequency",    ['貞'],                            []),
    ("社會 social",     ['君子', '大人'],                   ['小人']),
    ("時間 temporal",   ['初', '始', '先'],                 ['終', '後', '既']),
    ("text length",     None,                              None),  # custom
    ("否定 negation",   ['不', '勿', '無', '非'],           []),
]

def count_tokens(text, tokens):
    """Count occurrences of each token in text."""
    total = 0
    for tok in tokens:
        total += text.count(tok)
    return total

def score_hexagram(yaoci_lines, guaci_text, probe):
    """Score a hexagram on a probe. Returns (yaoci_score, guaci_score)."""
    name, pos, neg = probe

    if name == "text length":
        yaoci_score = sum(len(line) for line in yaoci_lines)
        guaci_score = len(guaci_text)
        return yaoci_score, guaci_score

    all_yaoci = ''.join(yaoci_lines)

    yaoci_score = count_tokens(all_yaoci, pos) - (count_tokens(all_yaoci, neg) if neg else 0)
    guaci_score = count_tokens(guaci_text, pos) - (count_tokens(guaci_text, neg) if neg else 0)

    return yaoci_score, guaci_score


# ── Core analysis ────────────────────────────────────────────

def compute_centroids(yaoci_emb):
    """(384, d) → (64, d) hex centroids."""
    return np.array([yaoci_emb[h*6:(h+1)*6].mean(axis=0) for h in range(N_HEX)])

def probe_r2(centroids, scores, pairs):
    """Compute R² of probe direction on complement opposition.

    1. OLS regression: centroids (64×d) ~ scores (64,)
    2. Probe direction = normalized coefficient vector
    3. For each complement pair, compute difference vector
    4. Project differences onto probe direction
    5. R² = sum(projections²) / sum(||diff||²)
    """
    scores = np.array(scores, dtype=float)

    # Check for zero-variance scores
    if np.std(scores) < 1e-10:
        return 0.0, np.zeros(len(pairs))

    # OLS: centroids = scores × β + ε
    # β = (X^T X)^{-1} X^T Y, but simpler: correlation of each dimension with scores
    scores_centered = scores - scores.mean()
    # β_j = Σ(scores_centered * centroids[:,j]) / Σ(scores_centered²)
    denom = np.sum(scores_centered ** 2)
    beta = centroids.T @ scores_centered / denom  # (d,)
    probe_dir = beta / np.linalg.norm(beta)  # unit direction

    # Complement pair differences
    diffs = np.array([centroids[h1] - centroids[h2] for h1, h2 in pairs])  # (32, d)

    # Projections
    projections = diffs @ probe_dir  # (32,)

    # R² = fraction of opposition variance along probe
    total_var = np.sum(diffs ** 2)
    probe_var = np.sum(projections ** 2)
    r2 = probe_var / total_var

    return r2, projections

def permutation_test(centroids, scores, pairs, n_perm=N_PERM):
    """Compute actual R² and p-value via permutation."""
    r2_actual, projections = probe_r2(centroids, scores, pairs)

    rng = np.random.default_rng(42)
    scores_arr = np.array(scores)
    n_ge = 0

    for _ in range(n_perm):
        perm_scores = rng.permutation(scores_arr)
        r2_perm, _ = probe_r2(centroids, perm_scores, pairs)
        if r2_perm >= r2_actual:
            n_ge += 1

    p_val = (n_ge + 1) / (n_perm + 1)  # conservative
    return r2_actual, p_val, projections


# ── Main ─────────────────────────────────────────────────────

def main():
    print("=" * 80)
    print("SEMANTIC PROBE VECTORS AGAINST COMPLEMENT OPPOSITION SPACE")
    print("=" * 80)
    print()

    # Load data
    atlas, hex_to_kw, kw_to_hex = load_atlas()
    pairs = load_complement_pairs(atlas)
    yaoci_texts, guaci_texts = load_texts_by_hex(hex_to_kw)
    models = load_embeddings()

    # Score all hexagrams on all probes
    yaoci_scores = {}  # probe_name → [64 scores]
    guaci_scores = {}

    print("--- Probe scores (first 5 hexagrams by hex_val) ---")
    for probe in PROBES:
        name = probe[0]
        ys, gs = [], []
        for h in range(N_HEX):
            y, g = score_hexagram(yaoci_texts[h], guaci_texts[h], probe)
            ys.append(y)
            gs.append(g)
        yaoci_scores[name] = ys
        guaci_scores[name] = gs
        print(f"  {name:20s}: yaoci range [{min(ys):4}, {max(ys):4}], "
              f"guaci range [{min(gs):3}, {max(gs):3}], "
              f"yaoci mean={np.mean(ys):.1f}, guaci mean={np.mean(gs):.1f}")
    print()

    # Run analysis for each probe × model × layer
    MODEL_ORDER = ['bge-m3', 'e5-large', 'labse', 'sikuroberta']

    # Build centroids for each model
    yaoci_centroids = {}
    for mname in MODEL_ORDER:
        yaoci_centroids[mname] = compute_centroids(models[mname]['yaoci'])

    guaci_centroids = {}
    if 'guaci' in models['bge-m3']:
        guaci_centroids['bge-m3'] = models['bge-m3']['guaci']  # already per-hex

    # Results storage
    results = {}  # (probe, layer, model) → (r2, p, projections)

    print("--- Running permutation tests (10K each) ---")
    total = len(PROBES) * (len(MODEL_ORDER) + len(guaci_centroids))
    done = 0

    for probe in PROBES:
        pname = probe[0]
        for mname in MODEL_ORDER:
            r2, p, proj = permutation_test(yaoci_centroids[mname], yaoci_scores[pname], pairs)
            results[(pname, 'yaoci', mname)] = (r2, p, proj)
            done += 1
            sig = " ***" if p < 0.01 else " *" if p < 0.05 else ""
            print(f"  [{done:2d}/{total}] {pname:20s} yaoci/{mname:12s}: R²={r2:.4f}, p={p:.4f}{sig}")

        for mname in guaci_centroids:
            r2, p, proj = permutation_test(guaci_centroids[mname], guaci_scores[pname], pairs)
            results[(pname, 'guaci', mname)] = (r2, p, proj)
            done += 1
            sig = " ***" if p < 0.01 else " *" if p < 0.05 else ""
            print(f"  [{done:2d}/{total}] {pname:20s} guaci/{mname:12s}: R²={r2:.4f}, p={p:.4f}{sig}")

    print()

    # ── Summary table ──
    print("=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print()
    header = f"{'Probe':20s} | {'bge-m3':12s} {'e5-large':12s} {'labse':12s} {'sikuroberta':12s} | {'guaci/bge':12s}"
    print(header)
    print("-" * len(header))

    flagged = []

    for probe in PROBES:
        pname = probe[0]
        cells = []
        cross_model_sig = 0

        for mname in MODEL_ORDER:
            r2, p, _ = results[(pname, 'yaoci', mname)]
            cell = f"{r2:.3f}({p:.3f})"
            if p < 0.01:
                cell += "*"
                cross_model_sig += 1
            cells.append(f"{cell:12s}")

        guaci_cell = ""
        if ('bge-m3') in guaci_centroids:
            r2, p, _ = results[(pname, 'guaci', 'bge-m3')]
            guaci_cell = f"{r2:.3f}({p:.3f})"
            if p < 0.01:
                guaci_cell += "*"

        row = f"{pname:20s} | {' '.join(cells)} | {guaci_cell:12s}"

        if cross_model_sig >= 3:
            row += "  ◄ CROSS-MODEL"
            flagged.append(pname)

        print(row)

    print()
    if flagged:
        print(f"FLAGGED PROBES (p<0.01 in ≥3 models): {flagged}")
    else:
        print("No probes achieved p<0.01 in ≥3 of 4 models.")
    print()

    # ── Diagnostics for flagged probes ──
    if flagged:
        print("=" * 80)
        print("DIAGNOSTICS FOR FLAGGED PROBES")
        print("=" * 80)
        print()

        for pname in flagged:
            print(f"--- {pname} ---")
            print()

            scores = yaoci_scores[pname]

            # Correlation with algebraic coordinates
            print("  Correlation with algebraic coordinates:")
            alg_coords = {}
            for h in range(N_HEX):
                d = atlas[str(h)]
                alg_coords.setdefault('lower_element', []).append(d['lower_trigram']['element'])
                alg_coords.setdefault('upper_element', []).append(d['upper_trigram']['element'])
                alg_coords.setdefault('basin', []).append(d['basin'])
                alg_coords.setdefault('surface_relation', []).append(d['surface_relation'])
                alg_coords.setdefault('hamming_wt', []).append(sum(int(b) for b in d['binary']))

            from scipy.stats import spearmanr, kruskal

            # Numeric: hamming_wt
            r, p = spearmanr(scores, alg_coords['hamming_wt'])
            print(f"    hamming_weight: ρ={r:.3f}, p={p:.4f}")

            # Categorical: Kruskal-Wallis
            for cname in ['lower_element', 'upper_element', 'basin', 'surface_relation']:
                groups = defaultdict(list)
                for h in range(N_HEX):
                    groups[alg_coords[cname][h]].append(scores[h])
                group_lists = [np.array(v) for v in groups.values() if len(v) > 1]
                if len(group_lists) >= 2:
                    stat, p = kruskal(*group_lists)
                    print(f"    {cname:20s}: H={stat:.2f}, p={p:.4f}")
            print()

            # Top/bottom 5 pairs by projection (use bge-m3 yaoci)
            _, _, proj = results[(pname, 'yaoci', 'bge-m3')]
            pair_proj = list(zip(pairs, proj))
            pair_proj.sort(key=lambda x: x[1])

            print("  Bottom 5 pairs (most negative projection):")
            for (h1, h2), p_val in pair_proj[:5]:
                n1 = atlas[str(h1)]['kw_name']
                n2 = atlas[str(h2)]['kw_name']
                s1 = scores[h1]
                s2 = scores[h2]
                print(f"    {n1:10s}({s1:+3d}) ↔ {n2:10s}({s2:+3d}): proj={p_val:+.4f}")

            print("  Top 5 pairs (most positive projection):")
            for (h1, h2), p_val in pair_proj[-5:]:
                n1 = atlas[str(h1)]['kw_name']
                n2 = atlas[str(h2)]['kw_name']
                s1 = scores[h1]
                s2 = scores[h2]
                print(f"    {n1:10s}({s1:+3d}) ↔ {n2:10s}({s2:+3d}): proj={p_val:+.4f}")
            print()

    # ── 升↔无妄 deep dive ──
    print("=" * 80)
    print("升 (Sheng, hex 6) ↔ 无妄 (Wu Wang, hex 57) DEEP DIVE")
    print("=" * 80)
    print()

    h_sheng = 6    # 升 = KW#46
    h_wuwang = 57  # 无妄 = KW#25
    pair_idx = None
    for i, (h1, h2) in enumerate(pairs):
        if (h1 == h_sheng and h2 == h_wuwang) or (h1 == h_wuwang and h2 == h_sheng):
            pair_idx = i
            break

    print(f"  Pair index: {pair_idx} (of 32)")
    print(f"  升 (hex {h_sheng}, KW #{atlas[str(h_sheng)]['kw_number']}, {atlas[str(h_sheng)]['kw_name']})")
    print(f"  无妄 (hex {h_wuwang}, KW #{atlas[str(h_wuwang)]['kw_number']}, {atlas[str(h_wuwang)]['kw_name']})")
    print()

    # Complement cosine similarity across models
    print("  Complement cosine similarity (raw centroids):")
    for mname in MODEL_ORDER:
        c = yaoci_centroids[mname]
        cos_sim = np.dot(c[h_sheng], c[h_wuwang]) / (np.linalg.norm(c[h_sheng]) * np.linalg.norm(c[h_wuwang]))
        # Also compute all 32 pair cosines for rank
        all_cos = []
        for h1, h2 in pairs:
            cs = np.dot(c[h1], c[h2]) / (np.linalg.norm(c[h1]) * np.linalg.norm(c[h2]))
            all_cos.append(cs)
        rank = sorted(range(32), key=lambda i: all_cos[i]).index(pair_idx) + 1
        print(f"    {mname:12s}: cos={cos_sim:.4f}, rank={rank}/32 "
              f"(min={min(all_cos):.4f}, median={np.median(all_cos):.4f}, max={max(all_cos):.4f})")
    print()

    # Vocabulary scores comparison
    print("  Vocabulary scores:")
    print(f"  {'Probe':20s} | {'升 yaoci':>9s} {'无妄 yaoci':>10s} {'diff':>6s} | {'升 guaci':>9s} {'无妄 guaci':>10s} {'diff':>6s}")
    print("  " + "-" * 80)
    for probe in PROBES:
        pname = probe[0]
        ys_sheng = yaoci_scores[pname][h_sheng]
        ys_wuwang = yaoci_scores[pname][h_wuwang]
        gs_sheng = guaci_scores[pname][h_sheng]
        gs_wuwang = guaci_scores[pname][h_wuwang]
        print(f"  {pname:20s} | {ys_sheng:9d} {ys_wuwang:10d} {ys_sheng - ys_wuwang:+6d} | "
              f"{gs_sheng:9d} {gs_wuwang:10d} {gs_sheng - gs_wuwang:+6d}")
    print()

    # Projection rank of 升↔无妄 on each significant probe
    print("  Projection rank of 升↔无妄 on all probes (yaoci/bge-m3):")
    for probe in PROBES:
        pname = probe[0]
        key = (pname, 'yaoci', 'bge-m3')
        r2, p, proj = results[key]
        if pair_idx is not None:
            abs_proj = np.abs(proj)
            rank = (abs_proj >= abs_proj[pair_idx]).sum()  # 1 = highest
            print(f"    {pname:20s}: |proj|={abs_proj[pair_idx]:.4f}, "
                  f"rank={rank}/32, R²={r2:.4f}, p={p:.4f}")
    print()

    # Compare 升↔无妄 score differences to mean absolute differences
    print("  Score difference vs mean absolute difference across all 32 pairs:")
    for probe in PROBES:
        pname = probe[0]
        scores_y = yaoci_scores[pname]
        abs_diffs = [abs(scores_y[h1] - scores_y[h2]) for h1, h2 in pairs]
        mean_abs = np.mean(abs_diffs)
        sw_diff = abs(scores_y[h_sheng] - scores_y[h_wuwang])
        rank = sum(1 for d in abs_diffs if d >= sw_diff)
        print(f"    {pname:20s}: |diff|={sw_diff:.0f}, mean|diff|={mean_abs:.1f}, "
              f"rank={rank}/32")
    print()

    # ── Overall assessment ──
    print("=" * 80)
    print("ASSESSMENT")
    print("=" * 80)
    print()

    # Count significant results
    sig_01 = sum(1 for k, (r2, p, _) in results.items() if p < 0.01)
    sig_05 = sum(1 for k, (r2, p, _) in results.items() if p < 0.05)
    total_tests = len(results)
    expected_05 = total_tests * 0.05
    expected_01 = total_tests * 0.01

    print(f"  Total tests: {total_tests}")
    print(f"  p<0.05: {sig_05} (expected by chance: {expected_05:.1f})")
    print(f"  p<0.01: {sig_01} (expected by chance: {expected_01:.1f})")
    print()

    if flagged:
        print(f"  Cross-model significant probes: {flagged}")
        print("  These probes capture real structure in the complement opposition.")
        print("  Check algebraic correlation diagnostics above to determine")
        print("  whether this is new or already captured by known coordinates.")
    else:
        print("  No cross-model significant probes found.")
        print("  The complement opposition is not aligned with any single")
        print("  vocabulary-based semantic axis tested here.")


if __name__ == "__main__":
    main()
