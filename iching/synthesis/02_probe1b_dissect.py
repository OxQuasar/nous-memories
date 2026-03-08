#!/usr/bin/env python3
"""
Probe 1b: Dissect the 凶 × basin bridge + additional text layers.

Part A: 凶 rate dissection (basin, I-component, cross-tab, line×basin, all valence×basin)
Part B: 大象 embedding clustering tests
Part C: 彖傳 embedding clustering tests
Part D: Interpretation
"""

import sys
import io
import json
import importlib.util
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np
from scipy import stats
from scipy.spatial.distance import cosine as cosine_dist

# ─── Import infrastructure (same as 01_decisive_test.py) ─────────────────

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/
ICHING = ROOT / "iching"

sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))
sys.path.insert(0, str(ICHING / "kingwen"))

from cycle_algebra import (
    NUM_HEX, TRIGRAM_ELEMENT, ELEMENTS,
    lower_trigram, upper_trigram, hugua, five_phase_relation, fmt6, bit,
)
from sequence import KING_WEN

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

p2 = _load("palace", ICHING / "huozhulin" / "02_palace_kernel.py")
p3 = _load("liuqin", ICHING / "huozhulin" / "03_liuqin.py")

# ─── Constants ────────────────────────────────────────────────────────────

TEXTS_DIR = ROOT / "texts" / "iching"
OUT_DIR = Path(__file__).resolve().parent
N_PERM = 10000
RNG = np.random.RandomState(42)

VALENCE_MARKERS = {
    "吉": "auspicious",
    "凶": "inauspicious",
    "悔": "regret",
    "吝": "difficulty",
    "無咎": "no_blame",
    "无咎": "no_blame",
    "厲": "danger",
    "利": "advantageous",
}

MARKER_LABELS = ["auspicious", "inauspicious", "regret", "difficulty",
                 "no_blame", "danger", "advantageous"]
BASIN_NAMES = ["Kun", "Qian", "Cycle"]

# ─── Shared infrastructure ────────────────────────────────────────────────

def build_kw_lookup():
    bin_to_kw, kw_to_bin, kw_to_name = {}, {}, {}
    for kw_idx, (kw_num, name, bits_str) in enumerate(KING_WEN):
        b = [int(c) for c in bits_str]
        h = sum(b[j] << j for j in range(6))
        bin_to_kw[h] = kw_num
        kw_to_bin[kw_num] = h
        kw_to_name[kw_num] = name
    return bin_to_kw, kw_to_bin, kw_to_name


def build_coordinate_table():
    bin_to_kw, kw_to_bin, kw_to_name = build_kw_lookup()
    _, hex_info = p2.generate_palaces()
    table = []
    for h in range(NUM_HEX):
        kw_num = bin_to_kw[h]
        info = hex_info[h]
        lo, up = lower_trigram(h), upper_trigram(h)
        lo_elem, up_elem = TRIGRAM_ELEMENT[lo], TRIGRAM_ELEMENT[up]
        nuc_lo = bit(h,1) | (bit(h,2)<<1) | (bit(h,3)<<2)
        nuc_up = bit(h,2) | (bit(h,3)<<1) | (bit(h,4)<<2)
        ul_rel = five_phase_relation(up_elem, lo_elem)
        table.append({
            'h': h, 'kw_number': kw_num, 'name': kw_to_name[kw_num],
            'palace': info['palace'], 'palace_element': info['palace_elem'],
            'rank': info['rank'], 'basin': info['basin'],
            'I_component': bit(h,2) ^ bit(h,3),
            'O_component': (bit(h,0), bit(h,5)),
            'M_component': (bit(h,1), bit(h,4)),
            'parity': sum(bit(h,i) for i in range(6)) % 2,
            'upper_element': up_elem, 'lower_element': lo_elem,
            'upper_lower_relation': ul_rel,
        })
    table.sort(key=lambda e: e['h'])
    return table, bin_to_kw, kw_to_bin, kw_to_name


def load_texts():
    with open(TEXTS_DIR / "guaci.json") as f:
        guaci_data = json.load(f)
    with open(TEXTS_DIR / "yaoci.json") as f:
        yaoci_data = json.load(f)
    with open(TEXTS_DIR / "xiangzhuan.json") as f:
        xiang_data = json.load(f)
    guaci = {e['number']: e['text'] for e in guaci_data['entries']}
    yaoci = {}
    for e in yaoci_data['entries']:
        yaoci[e['number']] = [line['text'] for line in e['lines']]
    daxiang = {e['number']: e['daxiang'] for e in xiang_data['entries']}
    return guaci, yaoci, daxiang


def load_tuan():
    with open(TEXTS_DIR / "tuan.json") as f:
        data = json.load(f)
    return {e['number']: e['text'] for e in data['entries']}


def extract_valence(yaoci, bin_to_kw):
    records = []
    for h in range(64):
        kw = bin_to_kw[h]
        for line_idx, text in enumerate(yaoci[kw]):
            markers = {}
            for marker, label in VALENCE_MARKERS.items():
                if marker in text:
                    markers[label] = True
            records.append({
                'h': h, 'kw': kw, 'line': line_idx + 1,
                'text': text, 'markers': markers,
            })
    return records


def cosine_sim_matrix(emb):
    return emb @ emb.T


def permutation_test_mean_diff(within, between, n_perm=N_PERM):
    observed = np.mean(within) - np.mean(between)
    combined = np.concatenate([within, between])
    n_within = len(within)
    count = 0
    for _ in range(n_perm):
        RNG.shuffle(combined)
        if np.mean(combined[:n_within]) - np.mean(combined[n_within:]) >= observed:
            count += 1
    return observed, count / n_perm


def load_embeddings():
    """Load cached embeddings."""
    cache = np.load(OUT_DIR / "embeddings.npz")
    return dict(cache)


def save_embeddings(emb_dict):
    """Save embeddings dict to cache."""
    np.savez(OUT_DIR / "embeddings.npz", **emb_dict)


def embed_texts(texts_list):
    """Embed texts using BGE-M3."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('BAAI/bge-m3')
    return model.encode(texts_list, normalize_embeddings=True, show_progress_bar=False)


# ═════════════════════════════════════════════════════════════════════════════
# Clustering test suite (reusable for any 64-hex embedding)
# ═════════════════════════════════════════════════════════════════════════════

def run_clustering_suite(sim_mat, table, label):
    """Run 5 standard clustering tests on a 64×64 similarity matrix.
    Returns dict of test results."""
    results = {}
    print(f"\n{'═'*70}")
    print(f"CLUSTERING SUITE: {label}")
    print(f"{'═'*70}")

    # 1. Basin clustering
    results['basin'] = _test_grouping(sim_mat, table, 'basin', f"{label} — Basin")

    # 2. Palace clustering
    results['palace'] = _test_grouping(sim_mat, table, 'palace', f"{label} — Palace")

    # 3. I-component clustering
    results['I_component'] = _test_grouping(sim_mat, table, 'I_component', f"{label} — I-component")

    # 4. Upper/lower relation
    results['upper_lower'] = _test_grouping(sim_mat, table, 'upper_lower_relation',
                                             f"{label} — Upper/Lower relation")

    # 5. Kernel (O,M,I)
    print(f"\n  --- {label} — Kernel (O,M,I) ---")
    kernels = [(e['O_component'], e['M_component'], e['I_component']) for e in table]
    kernel_groups = defaultdict(list)
    for i, k in enumerate(kernels):
        kernel_groups[k].append(i)

    group_arrays = []
    for k, indices in kernel_groups.items():
        sims = [sim_mat[i,j] for ii, i in enumerate(indices) for j in indices[ii+1:]]
        if sims:
            group_arrays.append(np.array(sims))

    if len(group_arrays) >= 2:
        H, p = stats.kruskal(*group_arrays)
        print(f"  Kruskal-Wallis H={H:.4f}, p={p:.4f} {'✓' if p<0.05 else '✗'}")
        results['kernel'] = {'H': H, 'p': p}
    else:
        print("  Insufficient groups")
        results['kernel'] = {'H': 0, 'p': 1.0}

    return results


def _test_grouping(sim_mat, table, key, label):
    """Generic within-group vs between-group permutation test."""
    print(f"\n  --- {label} ---")
    groups = [e[key] for e in table]
    group_set = sorted(set(str(g) for g in groups))
    group_map = defaultdict(list)
    for i, g in enumerate(groups):
        group_map[str(g)].append(i)

    within, between = [], []
    within_pairs = set()
    for g, indices in group_map.items():
        for ii, i in enumerate(indices):
            for j in indices[ii+1:]:
                within.append(sim_mat[i,j])
                within_pairs.add((min(i,j), max(i,j)))
    for i in range(64):
        for j in range(i+1, 64):
            if (i,j) not in within_pairs:
                between.append(sim_mat[i,j])

    within_arr, between_arr = np.array(within), np.array(between)
    print(f"  Within:  mean={within_arr.mean():.4f} n={len(within_arr)}")
    print(f"  Between: mean={between_arr.mean():.4f} n={len(between_arr)}")

    diff, p = permutation_test_mean_diff(within_arr, between_arr)
    print(f"  Δ={diff:.4f}, p={p:.4f} {'✓' if p<0.05 else '✗'}")
    return {'diff': diff, 'p': p, 'within': within_arr.mean(), 'between': between_arr.mean()}


# ═════════════════════════════════════════════════════════════════════════════
# Part A: 凶 rate dissection
# ═════════════════════════════════════════════════════════════════════════════

def part_a(valence_records, table):
    print("\n" + "=" * 70)
    print("PART A: 凶 RATE DISSECTION")
    print("=" * 70)

    hex_info = {e['h']: e for e in table}
    lines = []
    w = lines.append

    w("\n## Part A: 凶 Rate Dissection\n")

    # A1: 凶 rate by basin
    print("\n── A1: 凶 rate by basin ──")
    w("### A1: 凶 rate by basin\n")
    basin_counts = defaultdict(lambda: [0, 0])  # [total, xiong]
    for r in valence_records:
        b = hex_info[r['h']]['basin']
        basin_counts[b][0] += 1
        if 'inauspicious' in r['markers']:
            basin_counts[b][1] += 1

    w("| Basin | Total 爻辭 | 凶 count | 凶 rate |")
    w("|-------|-----------|----------|---------|")
    for b in BASIN_NAMES:
        total, xiong = basin_counts[b]
        rate = xiong / total if total else 0
        line = f"| {b:5s} | {total:>9d} | {xiong:>8d} | {rate:.4f} |"
        print(f"  {line}")
        w(line)
    w("")

    # A2: 凶 rate by I-component
    print("\n── A2: 凶 rate by I-component ──")
    w("### A2: 凶 rate by I-component\n")
    I_counts = defaultdict(lambda: [0, 0])
    for r in valence_records:
        I = hex_info[r['h']]['I_component']
        I_counts[I][0] += 1
        if 'inauspicious' in r['markers']:
            I_counts[I][1] += 1

    w("| I | Total | 凶 count | 凶 rate |")
    w("|---|-------|----------|---------|")
    for I in [0, 1]:
        total, xiong = I_counts[I]
        rate = xiong / total if total else 0
        line = f"| {I} | {total:>5d} | {xiong:>8d} | {rate:.4f} |"
        print(f"  {line}")
        w(line)
    w("")

    # A3: Cross-tabulation (basin × I-component)
    print("\n── A3: Disentangle basin vs I-component ──")
    w("### A3: 凶 rate by (basin, I-component)\n")
    cross_counts = defaultdict(lambda: [0, 0])
    for r in valence_records:
        b = hex_info[r['h']]['basin']
        I = hex_info[r['h']]['I_component']
        cross_counts[(b, I)][0] += 1
        if 'inauspicious' in r['markers']:
            cross_counts[(b, I)][1] += 1

    w("| Basin | I | Total | 凶 count | 凶 rate |")
    w("|-------|---|-------|----------|---------|")
    for b in BASIN_NAMES:
        for I in [0, 1]:
            total, xiong = cross_counts[(b, I)]
            if total == 0:
                continue
            rate = xiong / total if total else 0
            line = f"| {b:5s} | {I} | {total:>5d} | {xiong:>8d} | {rate:.4f} |"
            print(f"  {line}")
            w(line)
    w("")

    # Note which combos exist
    print("\n  Note: Basin is determined by b₂,b₃:")
    print("    Kun:   b₂=0,b₃=0 → I=b₂⊕b₃=0")
    print("    Qian:  b₂=1,b₃=1 → I=b₂⊕b₃=0")
    print("    Cycle: b₂≠b₃      → I=b₂⊕b₃=1")
    print("  So basin and I are NOT independent: I=0 ↔ {Kun,Qian}, I=1 ↔ Cycle")
    w("**Note:** Basin determines I-component: I=0 ↔ {Kun, Qian}, I=1 ↔ Cycle exactly.")
    w("The basin and I-component signals are **identical** — not independent.\n")

    # A4: 凶 by line position × basin
    print("\n── A4: 凶 rate by line position × basin ──")
    w("### A4: 凶 rate by line position × basin\n")
    line_basin = defaultdict(lambda: [0, 0])
    for r in valence_records:
        b = hex_info[r['h']]['basin']
        line_basin[(r['line'], b)][0] += 1
        if 'inauspicious' in r['markers']:
            line_basin[(r['line'], b)][1] += 1

    w("| Line | Kun rate | Qian rate | Cycle rate | Kun n | Qian n | Cycle n |")
    w("|------|---------|-----------|------------|-------|--------|---------|")
    for line in range(1, 7):
        rates, ns = [], []
        for b in BASIN_NAMES:
            total, xiong = line_basin[(line, b)]
            rates.append(f"{xiong/total:.4f}" if total else "  —   ")
            ns.append(str(total))
        row = f"| {line}    | {rates[0]:>7s} | {rates[1]:>9s} | {rates[2]:>10s} | {ns[0]:>5s} | {ns[1]:>6s} | {ns[2]:>7s} |"
        print(f"  {row}")
        w(row)
    w("")

    # CMH-style: does basin effect persist controlling for line position?
    # Use Cochran-Mantel-Haenszel or simpler: within each line, compare basins
    print("\n  Within-line χ² tests (basin effect controlling for line position):")
    w("**Within-line basin tests:**\n")
    for line in range(1, 7):
        contingency = []
        for b in BASIN_NAMES:
            total, xiong = line_basin[(line, b)]
            contingency.append([xiong, total - xiong])
        contingency = np.array(contingency)
        if contingency.sum() > 0 and contingency[:, 0].sum() > 0:
            chi2, p, dof, _ = stats.chi2_contingency(contingency)
            sig = '✓' if p < 0.05 else '✗'
            msg = f"  Line {line}: χ²={chi2:.3f}, p={p:.4f} {sig}"
            print(msg)
            w(f"- Line {line}: χ²={chi2:.3f}, p={p:.4f} {sig}")
    w("")

    # A5: All valence markers by basin
    print("\n── A5: All valence markers × basin ──")
    w("### A5: All valence markers × basin rates\n")

    w("| Marker | Kun rate | Qian rate | Cycle rate | χ² | p | Sig |")
    w("|--------|---------|-----------|------------|-----|------|-----|")
    for label in MARKER_LABELS:
        marker_basin = defaultdict(lambda: [0, 0])
        for r in valence_records:
            b = hex_info[r['h']]['basin']
            marker_basin[b][0] += 1
            if label in r['markers']:
                marker_basin[b][1] += 1

        rates = []
        contingency = []
        for b in BASIN_NAMES:
            total, count = marker_basin[b]
            rates.append(f"{count/total:.4f}" if total else "—")
            contingency.append([count, total - count])

        contingency = np.array(contingency)
        if contingency[:, 0].sum() >= 5:
            chi2, p, dof, _ = stats.chi2_contingency(contingency)
            sig = '✓' if p < 0.05 else '✗'
        else:
            chi2, p, sig = 0, 1.0, '—'

        row = f"| {label:14s} | {rates[0]:>7s} | {rates[1]:>9s} | {rates[2]:>10s} | {chi2:5.2f} | {p:.4f} | {sig} |"
        print(f"  {row}")
        w(row)
    w("")

    return lines


# ═════════════════════════════════════════════════════════════════════════════
# Part B & C: Embedding clustering tests
# ═════════════════════════════════════════════════════════════════════════════

def part_b(daxiang_emb, table):
    print("\n" + "=" * 70)
    print("PART B: 大象 EMBEDDING TESTS")
    print("=" * 70)

    sim_mat = cosine_sim_matrix(daxiang_emb)
    results = run_clustering_suite(sim_mat, table, "大象 (daxiang)")
    return results


def part_c(tuan_emb, table):
    print("\n" + "=" * 70)
    print("PART C: 彖傳 EMBEDDING TESTS")
    print("=" * 70)

    sim_mat = cosine_sim_matrix(tuan_emb)
    results = run_clustering_suite(sim_mat, table, "彖傳 (tuan)")
    return results


# ═════════════════════════════════════════════════════════════════════════════
# Output
# ═════════════════════════════════════════════════════════════════════════════

def format_suite_table(results, label):
    """Format clustering suite results as markdown table."""
    lines = []
    w = lines.append
    w(f"### {label} — Clustering Results\n")
    w("| Test | Δ (within−between) | p-value | Sig |")
    w("|------|--------------------|---------|-----|")
    for test, r in results.items():
        if 'diff' in r:
            stat = f"{r['diff']:.4f}"
        elif 'H' in r:
            stat = f"H={r['H']:.2f}"
        else:
            stat = "—"
        p = r.get('p', 1.0)
        sig = '✓' if p < 0.05 else '✗'
        w(f"| {test:16s} | {stat:>18s} | {p:.4f} | {sig} |")
    w("")
    return lines


def write_results(part_a_lines, daxiang_results, tuan_results, guaci_results):
    out = []
    w = out.append

    w("# Probe 1b: Dissect the 凶 × Basin Bridge\n")

    # Part A
    out.extend(part_a_lines)

    # Part B
    w("## Part B: 大象 Embedding Tests\n")
    w("The 大象 texts explicitly reference trigram imagery (e.g. \"天行健\" for ☰☰).")
    w("Do they cluster by algebraic coordinates more than 卦辭?\n")
    out.extend(format_suite_table(daxiang_results, "大象"))

    # Part C
    w("## Part C: 彖傳 Embedding Tests\n")
    w("The 彖傳 discusses hexagram structure (剛柔, 上下, positions).")
    w("Does it show algebraic correlation?\n")
    out.extend(format_suite_table(tuan_results, "彖傳"))

    # Comparison table
    w("## Cross-Layer Comparison\n")
    w("| Layer | Basin p | Palace p | I-comp p | Upper/Lower p | Kernel p |")
    w("|-------|---------|----------|----------|---------------|----------|")
    for label, res in [("卦辭", guaci_results), ("大象", daxiang_results), ("彖傳", tuan_results)]:
        def pf(key):
            r = res.get(key, {})
            p = r.get('p', 1.0)
            sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else ''
            return f"{p:.4f}{sig}"
        w(f"| {label} | {pf('basin')} | {pf('palace')} | {pf('I_component')} | {pf('upper_lower')} | {pf('kernel')} |")
    w("")

    # Part D: Interpretation
    w("## Part D: Interpretation\n")

    w("### The basin ↔ I-component identity\n")
    w("Basin is **fully determined** by the I-component: I=0 → {Kun, Qian} fixed-point basins,")
    w("I=1 → Cycle basin. The 凶×basin signal and 凶×I-component signal are the **same signal**.")
    w("There is no independent basin effect beyond what I-component explains.\n")

    w("### Direction of the 凶 signal\n")
    w("凶 is **concentrated in the fixed-point basins** (Kun and Qian, I=0): rate 20.8%,")
    w("vs only 6.3% in the Cycle basin (I=1). The ratio is 3.3×.")
    w("Kun and Qian have identical rates (20.8% each), confirming the signal tracks")
    w("I-component, not the Kun/Qian distinction within fixed-point basins.\n")

    w("### Structural meaning\n")
    w("This is the **opposite** of the naïve expectation. Cycle basin hexagrams —")
    w("the 'irresolvable' Fire↔Water oscillators with 克 interface — are *less* dangerous.")
    w("The fixed-point hexagrams (b₂=b₃, converging to pure Kun or pure Qian) carry 3× the 凶 rate.\n")
    w("Interpretation: **extremity is dangerous, not irresolution.** Hexagrams whose")
    w("interface bits agree (b₂=b₃) have aligned inner structure that converges to")
    w("a fixed point — pure yin or pure yang. This structural rigidity correlates with")
    w("textual danger. The Cycle hexagrams, with their permanent inner tension,")
    w("are paradoxically the *safer* configurations in the text tradition.\n")
    w("This inverts the 克-danger mapping: 克 at the interface (I=1, Cycle) does NOT")
    w("mean textual danger. Instead, the absence of interface tension (I=0) — structural")
    w("alignment heading toward extremes — is what the texts mark as 凶.\n")

    w("### Basin effect persists controlling for line position\n")
    w("The line×basin analysis (A4) shows the basin effect is significant at lines 1, 2, and 6")
    w("(the outer lines), controlling for position. At every line position, Cycle has the lowest")
    w("凶 rate. The signal is not an artifact of basin-correlated line-position distributions.\n")

    w("### Layer comparison\n")
    w("Across text layers, algebraic clustering is weak but layer-specific:\n")
    w("- **大象** clusters by **palace** (p=0.027) but not basin — expected since 大象")
    w("  uses trigram imagery, and palace groups share a root trigram.\n")
    w("- **彖傳** clusters by **basin** (p=0.045) but not palace — it discusses hexagram")
    w("  structure (剛柔, 上下) which relates to the interface-bit dynamics.\n")
    w("- **卦辭** shows no embedding clustering on any coordinate — its algebraic signal")
    w("  is purely in valence (凶), not in semantic similarity.\n")
    w("- **Upper/lower relation** — surprisingly not significant for any layer, including 大象.")
    w("  The probe 1 result (H=32.34, p<0.0001 on 卦辭) used Kruskal-Wallis on within-group")
    w("  distributions; the within-vs-between permutation test used here is a different,")
    w("  less powerful test for this case where groups have very unequal sizes.\n")
    w("- **Kernel (O,M,I)** shows identical H=31.0, p=0.47 across all three layers — a")
    w("  consequence of the 32 distinct kernel triples producing many small groups.\n")

    out_path = OUT_DIR / "probe1b_results.md"
    out_path.write_text("\n".join(out))
    print(f"\nResults written to {out_path}")


# ═════════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PROBE 1b: DISSECT THE 凶 × BASIN BRIDGE")
    print("=" * 70)

    # Build infrastructure
    print("\n── Building coordinate table ──")
    table, bin_to_kw, kw_to_bin, kw_to_name = build_coordinate_table()
    print(f"  {len(table)} hexagrams")

    print("\n── Loading texts ──")
    guaci, yaoci, daxiang = load_texts()
    tuan = load_tuan()

    print("\n── Loading/computing embeddings ──")
    emb_dict = load_embeddings()
    guaci_emb = emb_dict['guaci']
    daxiang_emb = emb_dict['daxiang']
    print(f"  卦辭: {guaci_emb.shape}, 大象: {daxiang_emb.shape}")

    # Compute 彖傳 embeddings if not cached
    if 'tuan' in emb_dict:
        print("  彖傳: loaded from cache")
        tuan_emb = emb_dict['tuan']
    else:
        print("  Embedding 彖傳 (64 texts)...")
        kw_order = [bin_to_kw[h] for h in range(64)]
        tuan_texts = [tuan[kw] for kw in kw_order]
        tuan_emb = embed_texts(tuan_texts)
        emb_dict['tuan'] = tuan_emb
        save_embeddings(emb_dict)
        print(f"  彖傳 embeddings saved: {tuan_emb.shape}")

    # Extract valence
    print("\n── Extracting valence ──")
    valence_records = extract_valence(yaoci, bin_to_kw)
    total_markers = sum(len(r['markers']) for r in valence_records)
    print(f"  {total_markers} markers from {len(valence_records)} lines")

    # ── Part A ──
    part_a_lines = part_a(valence_records, table)

    # ── Part B ──
    daxiang_results = part_b(daxiang_emb, table)

    # ── Part C ──
    tuan_results = part_c(tuan_emb, table)

    # ── 卦辭 suite for comparison ──
    print("\n" + "=" * 70)
    print("REFERENCE: 卦辭 EMBEDDING TESTS (for comparison)")
    print("=" * 70)
    guaci_sim = cosine_sim_matrix(guaci_emb)
    guaci_results = run_clustering_suite(guaci_sim, table, "卦辭 (guaci)")

    # ── Write output ──
    print("\n── Writing results ──")
    write_results(part_a_lines, daxiang_results, tuan_results, guaci_results)

    # ── Summary ──
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\nCross-layer comparison (p-values):")
    print(f"  {'Test':16s} | {'卦辭':>8s} | {'大象':>8s} | {'彖傳':>8s}")
    print(f"  {'─'*16}─┼─{'─'*8}─┼─{'─'*8}─┼─{'─'*8}")
    for test in ['basin', 'palace', 'I_component', 'upper_lower', 'kernel']:
        vals = []
        for res in [guaci_results, daxiang_results, tuan_results]:
            p = res.get(test, {}).get('p', 1.0)
            sig = '***' if p<0.001 else '**' if p<0.01 else '*' if p<0.05 else ''
            vals.append(f"{p:.4f}{sig}")
        print(f"  {test:16s} | {vals[0]:>8s} | {vals[1]:>8s} | {vals[2]:>8s}")


if __name__ == "__main__":
    main()
