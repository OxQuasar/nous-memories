#!/usr/bin/env python3
"""
Phase B: Partition Comparison, Directed Graphs, and Quotient Structure

Probe 3: Mutual information between 6 partitions of 8 trigrams
Probe 4: 生/克 as directed graphs on Z₂³ and 16-node inner space
Probe 5: Algebraic quotient structure — symmetry groups, entropy decomposition

Encoding: bit0 = bottom line, bit2 = top line (consistent with cycle_algebra.py).
"""

import sys
from collections import defaultdict
from itertools import combinations, product as iterproduct
from pathlib import Path
from math import log2, factorial

sys.path.insert(0, 'memories/iching/opposition-theory/phase4')

from cycle_algebra import (
    TRIGRAM_ELEMENT, TRIGRAM_NAMES, ELEMENTS, ELEMENT_ZH,
    SHENG_CYCLE, KE_CYCLE, SHENG_EDGES, KE_EDGES,
    SHENG_MAP, KE_MAP, ELEM_TRIGRAMS,
    hamming3, fmt3, popcount,
)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUTDIR = Path(__file__).parent
N_TRIG = 8

# ═══════════════════════════════════════════════════════════════════════
# Reused helpers from 01_cube_and_inner.py
# ═══════════════════════════════════════════════════════════════════════

ELEM_COLORS = {
    "Wood": "#4caf50", "Fire": "#e53935", "Earth": "#ab8a3c",
    "Metal": "#78909c", "Water": "#1e88e5",
}

def fmt4(x): return format(x, '04b')

def lower_nuclear(v): return v & 0b111
def upper_nuclear(v): return (v >> 1) & 0b111

def basin_of_inner(v):
    b1, b2 = (v >> 1) & 1, (v >> 2) & 1
    if b1 == 0 and b2 == 0: return "Kun"
    if b1 == 1 and b2 == 1: return "Qian"
    return "Cycle"

def inner_hugua(v):
    i1, i2 = (v >> 1) & 1, (v >> 2) & 1
    return i1 | (i2 << 1) | (i1 << 2) | (i2 << 3)

INNER_ATTRACTORS = frozenset({0, 5, 10, 15})

def phase_rel(src_elem, tgt_elem):
    if src_elem == tgt_elem: return "same"
    if SHENG_MAP[src_elem] == tgt_elem: return "gen_fwd"
    if SHENG_MAP[tgt_elem] == src_elem: return "gen_rev"
    if KE_MAP[src_elem] == tgt_elem: return "over_fwd"
    if KE_MAP[tgt_elem] == src_elem: return "over_rev"
    raise ValueError(f"No relation: {src_elem} vs {tgt_elem}")

REL_ZH = {
    'same': '比', 'gen_fwd': '生→', 'gen_rev': '←生',
    'over_fwd': '克→', 'over_rev': '←克',
}
ALL_RELS = ['same', 'gen_fwd', 'gen_rev', 'over_fwd', 'over_rev']


# ═══════════════════════════════════════════════════════════════════════
# PROBE 3: Partition Comparison
# ═══════════════════════════════════════════════════════════════════════

def build_partitions():
    """Define 6 partitions of the 8 trigrams."""
    # 1. Wuxing
    wuxing = {}
    for t in range(N_TRIG):
        wuxing[t] = TRIGRAM_ELEMENT[t]

    # 2. Yang count
    yang_count = {t: f"{popcount(t)}yang" for t in range(N_TRIG)}

    # 3. Basin of doubled trigram TT
    # Interface of TT = (bit2_of_T, bit0_of_T)
    def basin_of_doubled(t):
        t2, t0 = (t >> 2) & 1, t & 1
        if t2 == 0 and t0 == 0: return "Kun"
        if t2 == 1 and t0 == 1: return "Qian"
        return "Cycle"
    basin_doubled = {t: basin_of_doubled(t) for t in range(N_TRIG)}

    # 4. Later Heaven quadrant
    # S=Li(101), SW=Kun(000) → South
    # W=Dui(011), NW=Qian(111) → West
    # N=Kan(010), NE=Gen(100) → North
    # E=Zhen(001), SE=Xun(110) → East
    lh_quadrant = {
        0b001: "East", 0b110: "East",    # Zhen, Xun
        0b101: "South", 0b000: "South",  # Li, Kun
        0b011: "West", 0b111: "West",    # Dui, Qian
        0b010: "North", 0b100: "North",  # Kan, Gen
    }

    # 5. Complement pair (XOR 111)
    comp_pair = {}
    for t in range(N_TRIG):
        pair = tuple(sorted([t, t ^ 0b111]))
        comp_pair[t] = str(pair)

    # 6. b₀⊕b₁ parity
    parity_01 = {t: f"p{(t & 1) ^ ((t >> 1) & 1)}" for t in range(N_TRIG)}

    return {
        'Wuxing': wuxing,
        'Yang count': yang_count,
        'Basin(TT)': basin_doubled,
        'Later Heaven': lh_quadrant,
        'Complement': comp_pair,
        'b0+b1 parity': parity_01,
    }


def partition_to_classes(part):
    """Convert trigram→label dict to {label: set(trigrams)}."""
    classes = defaultdict(set)
    for t, label in part.items():
        classes[label].add(t)
    return dict(classes)


def entropy(part):
    """H(P) for a partition over 8 uniform items."""
    classes = partition_to_classes(part)
    n = sum(len(c) for c in classes.values())
    h = 0.0
    for c in classes.values():
        p = len(c) / n
        if p > 0:
            h -= p * log2(p)
    return h


def joint_entropy(p1, p2):
    """H(P1, P2) = joint entropy."""
    n = N_TRIG
    # Count joint cells
    counts = defaultdict(int)
    for t in range(n):
        counts[(p1[t], p2[t])] += 1
    h = 0.0
    for cnt in counts.values():
        p = cnt / n
        if p > 0:
            h -= p * log2(p)
    return h


def mutual_info(p1, p2):
    return entropy(p1) + entropy(p2) - joint_entropy(p1, p2)


def cond_entropy(target, given):
    """H(target | given) = H(target, given) - H(given)."""
    return joint_entropy(target, given) - entropy(given)


def probe3_mi_matrix(partitions):
    """Compute MI and NMI matrices for all partition pairs."""
    names = list(partitions.keys())
    n = len(names)

    # Entropies
    H = {name: entropy(partitions[name]) for name in names}

    # MI matrix
    mi = np.zeros((n, n))
    nmi = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            mi[i, j] = mutual_info(partitions[names[i]], partitions[names[j]])
            min_h = min(H[names[i]], H[names[j]])
            nmi[i, j] = mi[i, j] / min_h if min_h > 0 else 0.0

    # Conditional entropy H(Wuxing | X)
    cond_h = {}
    for name in names:
        if name != 'Wuxing':
            cond_h[name] = cond_entropy(partitions['Wuxing'], partitions[name])

    # Can any PAIR of other partitions capture all of Wuxing?
    pair_cond = {}
    other_names = [n for n in names if n != 'Wuxing']
    for i in range(len(other_names)):
        for j in range(i + 1, len(other_names)):
            n1, n2 = other_names[i], other_names[j]
            # Combine p1 and p2 into a joint partition
            combined = {t: (partitions[n1][t], partitions[n2][t]) for t in range(N_TRIG)}
            pair_cond[(n1, n2)] = cond_entropy(partitions['Wuxing'], combined)

    return names, H, mi, nmi, cond_h, pair_cond


# ═══════════════════════════════════════════════════════════════════════
# PROBE 4: Directed Graphs
# ═══════════════════════════════════════════════════════════════════════

def probe4_trigram_graphs():
    """4a: Build 5 directed relation graphs on 8 trigrams."""
    graphs = {r: [] for r in ALL_RELS}
    for s in range(N_TRIG):
        for t in range(N_TRIG):
            if s == t:
                continue
            rel = phase_rel(TRIGRAM_ELEMENT[s], TRIGRAM_ELEMENT[t])
            graphs[rel].append((s, t))

    # Verify: all 5 graphs partition the 56 directed non-self edges
    total = sum(len(e) for e in graphs.values())
    assert total == N_TRIG * (N_TRIG - 1), f"Expected 56 edges, got {total}"

    # Degree distributions
    degrees = {}
    for rel, edges in graphs.items():
        in_deg = defaultdict(int)
        out_deg = defaultdict(int)
        for s, t in edges:
            out_deg[s] += 1
            in_deg[t] += 1
        degrees[rel] = {
            'edges': len(edges), 'in_deg': dict(in_deg), 'out_deg': dict(out_deg),
        }

    return graphs, degrees


def probe4_inner_graphs():
    """4b: Five-phase relations on 16-node inner space + hugua comparison."""
    # Element lookup for inner states
    inner_elems = {}
    for v in range(16):
        lo = lower_nuclear(v)
        up = upper_nuclear(v)
        inner_elems[v] = (TRIGRAM_ELEMENT[lo], TRIGRAM_ELEMENT[up])

    # All directed edges between inner states, classified by lo/up relations
    inner_edges = []
    for v in range(16):
        for w in range(16):
            if v == w:
                continue
            lo_v, up_v = inner_elems[v]
            lo_w, up_w = inner_elems[w]
            lo_rel = phase_rel(lo_v, lo_w)
            up_rel = phase_rel(up_v, up_w)
            inner_edges.append({
                'src': v, 'tgt': w,
                'lo_rel': lo_rel, 'up_rel': up_rel,
            })

    # Count "both gen_fwd", "both over_fwd" etc
    both_counts = defaultdict(int)
    for e in inner_edges:
        both_counts[(e['lo_rel'], e['up_rel'])] += 1

    # Hugua edges and their five-phase relations
    hugua_edges = []
    for v in range(16):
        w = inner_hugua(v)
        if v == w:
            continue
        lo_v, up_v = inner_elems[v]
        lo_w, up_w = inner_elems[w]
        lo_rel = phase_rel(lo_v, lo_w)
        up_rel = phase_rel(up_v, up_w)
        basin = basin_of_inner(v)
        hugua_edges.append({
            'src': v, 'tgt': w, 'basin': basin,
            'lo_rel': lo_rel, 'up_rel': up_rel,
        })

    # Statistics on hugua edges
    hugua_rel_counts = defaultdict(int)
    hugua_has_gen = 0
    hugua_has_over = 0
    hugua_both_same_type = 0
    for e in hugua_edges:
        hugua_rel_counts[(e['lo_rel'], e['up_rel'])] += 1
        if e['lo_rel'] in ('gen_fwd', 'gen_rev') or e['up_rel'] in ('gen_fwd', 'gen_rev'):
            hugua_has_gen += 1
        if e['lo_rel'] in ('over_fwd', 'over_rev') or e['up_rel'] in ('over_fwd', 'over_rev'):
            hugua_has_over += 1
        if e['lo_rel'] == e['up_rel']:
            hugua_both_same_type += 1

    # Cross-tab: hugua edges × basin
    hugua_by_basin = defaultdict(list)
    for e in hugua_edges:
        hugua_by_basin[e['basin']].append(e)

    return {
        'inner_elems': inner_elems,
        'inner_edges': inner_edges,
        'both_counts': dict(both_counts),
        'hugua_edges': hugua_edges,
        'hugua_rel_counts': dict(hugua_rel_counts),
        'hugua_has_gen': hugua_has_gen,
        'hugua_has_over': hugua_has_over,
        'hugua_both_same_type': hugua_both_same_type,
        'hugua_by_basin': dict(hugua_by_basin),
    }


# ═══════════════════════════════════════════════════════════════════════
# PROBE 5: Quotient Structure
# ═══════════════════════════════════════════════════════════════════════

def mat_mul_f2(A, B):
    """Multiply two 3×3 matrices over F₂."""
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s ^= A[i][k] & B[k][j]
            C[i][j] = s
    return C


def mat_vec_f2(A, v):
    """A × v over F₂, v is a 3-bit integer, returns 3-bit integer."""
    result = 0
    for i in range(3):
        s = 0
        for j in range(3):
            s ^= A[i][j] & ((v >> j) & 1)
        result |= (s << i)
    return result


def mat_det_f2(A):
    """Determinant of 3×3 matrix over F₂."""
    a = A[0][0]; b = A[0][1]; c = A[0][2]
    d = A[1][0]; e = A[1][1]; f = A[1][2]
    g = A[2][0]; h = A[2][1]; k = A[2][2]
    return (a*(e*k ^ f*h) ^ b*(d*k ^ f*g) ^ c*(d*h ^ e*g)) & 1


def enumerate_gl3_f2():
    """Enumerate all invertible 3×3 matrices over F₂ (order 168)."""
    matrices = []
    for bits in range(1 << 9):
        A = [[(bits >> (i*3 + j)) & 1 for j in range(3)] for i in range(3)]
        if mat_det_f2(A):
            matrices.append(A)
    return matrices


def partition_classes(mapping):
    """Convert trigram→label to frozenset of frozensets."""
    classes = defaultdict(set)
    for t, label in mapping.items():
        classes[label].add(t)
    return frozenset(frozenset(c) for c in classes.values())


def probe5_symmetry():
    """5a: Find linear and affine symmetries preserving Wuxing partition."""
    wuxing = {t: TRIGRAM_ELEMENT[t] for t in range(N_TRIG)}
    wuxing_classes = partition_classes(wuxing)

    gl3 = enumerate_gl3_f2()
    assert len(gl3) == 168, f"GL(3,F₂) should have 168 elements, got {len(gl3)}"

    # Linear symmetries: A such that A(class) = class for all classes
    linear_sym = []
    for A in gl3:
        # Apply A to each trigram
        image = {}
        for t in range(N_TRIG):
            image[t] = mat_vec_f2(A, t)
        # Check if partition is preserved
        image_classes = defaultdict(set)
        for t, elem in wuxing.items():
            image_classes[elem].add(image[t])
        if all(image_classes[e] == set(ELEM_TRIGRAMS[e]) for e in ELEMENTS):
            linear_sym.append(A)

    # Affine symmetries: x → Ax + b
    affine_sym = []
    for A in gl3:
        for b in range(N_TRIG):
            image = {}
            for t in range(N_TRIG):
                image[t] = mat_vec_f2(A, t) ^ b
            image_classes = defaultdict(set)
            for t, elem in wuxing.items():
                image_classes[elem].add(image[t])
            if all(image_classes[e] == set(ELEM_TRIGRAMS[e]) for e in ELEMENTS):
                affine_sym.append((A, b))

    return {
        'linear_count': len(linear_sym),
        'linear_sym': linear_sym,
        'affine_count': len(affine_sym),
        'affine_sym': affine_sym,
        'gl3_order': len(gl3),
    }


def probe5_decomposition():
    """5b-5c: Algebraic decomposition and cosmological residual."""
    # The partition hierarchy:
    # Level 0: all 8 trigrams
    # Level 1: b₀⊕b₁ parity → splits into {0,3,4,7} and {1,2,5,6}
    # Level 2: within parity-0: b₀ → {0,4}=Earth vs {3,7}=Metal
    #          within parity-1: ?=non-algebraic
    # Level 3: within parity-1: {1,6}=Wood vs {2}=Water vs {5}=Fire

    parity = {t: (t & 1) ^ ((t >> 1) & 1) for t in range(N_TRIG)}
    b0 = {t: t & 1 for t in range(N_TRIG)}
    wuxing = {t: TRIGRAM_ELEMENT[t] for t in range(N_TRIG)}

    # Entropies at each level
    H_wuxing = entropy(wuxing)
    H_given_parity = cond_entropy(wuxing, parity)

    # H(Wuxing | parity, b₀) = conditional on knowing both
    combined_p_b0 = {t: (parity[t], b0[t]) for t in range(N_TRIG)}
    H_given_parity_b0 = cond_entropy(wuxing, combined_p_b0)

    # The parity-1 coset
    coset_1 = [t for t in range(N_TRIG) if parity[t] == 1]  # {1,2,5,6}

    # Within coset_1, complement pairs under XOR=111:
    # 1(001)↔6(110), 2(010)↔5(101)
    # Wuxing groups: {1,6}=Wood, {2}=Water, {5}=Fire
    # Only choice: which complement pair stays together?
    # There are exactly 2 complement pairs in the coset: (1,6) and (2,5)
    # Traditional: (1,6) stays → Wood
    coset_1_comp_pairs = []
    seen = set()
    for t in coset_1:
        if t not in seen:
            comp = t ^ 0b111
            if comp in coset_1 and comp != t:
                coset_1_comp_pairs.append((t, comp))
                seen.add(t)
                seen.add(comp)

    # Parity-0 coset
    coset_0 = [t for t in range(N_TRIG) if parity[t] == 0]  # {0,3,4,7}
    coset_0_comp_pairs = []
    seen = set()
    for t in coset_0:
        if t not in seen:
            comp = t ^ 0b111
            if comp in coset_0 and comp != t:
                coset_0_comp_pairs.append((t, comp))
                seen.add(t)
                seen.add(comp)

    return {
        'H_wuxing': H_wuxing,
        'H_given_parity': H_given_parity,
        'H_given_parity_b0': H_given_parity_b0,
        'coset_1': coset_1,
        'coset_1_comp_pairs': coset_1_comp_pairs,
        'coset_0': coset_0,
        'coset_0_comp_pairs': coset_0_comp_pairs,
        'algebraic_bits': H_wuxing - H_given_parity_b0,
        'cosmological_bits': H_given_parity_b0,
    }


def enumerate_221_partitions():
    """Enumerate all partitions of {0..7} with shape (2,2,2,1,1)."""
    items = list(range(N_TRIG))
    partitions = []
    seen = set()

    # Choose 3 unordered pairs, remainder = 2 singletons
    for p1 in combinations(items, 2):
        rem1 = [x for x in items if x not in p1]
        for p2 in combinations(rem1, 2):
            if p2 < p1:
                continue  # canonical ordering of pairs
            rem2 = [x for x in rem1 if x not in p2]
            for p3 in combinations(rem2, 2):
                if p3 < p2:
                    continue
                singletons = tuple(x for x in rem2 if x not in p3)
                # Canonical form: sorted pairs, sorted singletons
                key = (p1, p2, p3, singletons)
                if key not in seen:
                    seen.add(key)
                    # Convert to partition dict
                    part = {}
                    for t in p1: part[t] = 0
                    for t in p2: part[t] = 1
                    for t in p3: part[t] = 2
                    part[singletons[0]] = 3
                    part[singletons[1]] = 4
                    partitions.append(part)

    return partitions


def probe5_comparison(partitions_named):
    """5d: Compare traditional Wuxing to all (2,2,2,1,1) partitions."""
    all_parts = enumerate_221_partitions()
    n_parts = len(all_parts)

    wuxing = partitions_named['Wuxing']
    yang_count = partitions_named['Yang count']
    basin_doubled = partitions_named['Basin(TT)']
    later_heaven = partitions_named['Later Heaven']

    # For each partition, compute MI with 3 reference partitions
    mi_yang = []
    mi_basin = []
    mi_lh = []
    mi_complement = []
    has_affine_sym = []

    # Pre-compute GL(3,F₂)
    gl3 = enumerate_gl3_f2()

    for part in all_parts:
        mi_yang.append(mutual_info(part, yang_count))
        mi_basin.append(mutual_info(part, basin_doubled))
        mi_lh.append(mutual_info(part, later_heaven))

        # Count affine symmetry group order (including identity)
        part_classes = partition_classes(part)
        sym_order = 0
        for A in gl3:
            for b in range(N_TRIG):
                image = {t: mat_vec_f2(A, t) ^ b for t in range(N_TRIG)}
                img_classes = defaultdict(set)
                for t, label in part.items():
                    img_classes[label].add(image[t])
                if frozenset(frozenset(c) for c in img_classes.values()) == part_classes:
                    sym_order += 1
        has_affine_sym.append(sym_order)

    # Find traditional Wuxing's rank
    wuxing_classes = partition_classes(wuxing)
    trad_idx = None
    for i, part in enumerate(all_parts):
        if partition_classes(part) == wuxing_classes:
            trad_idx = i
            break

    # Compute total MI score = sum of MI with all 3 references
    total_mi = [mi_yang[i] + mi_basin[i] + mi_lh[i] for i in range(n_parts)]

    return {
        'n_parts': n_parts,
        'mi_yang': mi_yang,
        'mi_basin': mi_basin,
        'mi_lh': mi_lh,
        'has_affine_sym': has_affine_sym,
        'total_mi': total_mi,
        'trad_idx': trad_idx,
        'all_parts': all_parts,
    }


# ═══════════════════════════════════════════════════════════════════════
# Visualization
# ═══════════════════════════════════════════════════════════════════════

def viz_mi_matrix(names, nmi):
    """Heatmap of the NMI matrix."""
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(nmi, cmap='YlOrRd', vmin=0, vmax=1, aspect='equal')

    # Labels
    short_names = [n.replace('b0+b1 parity', 'b0+b1').replace('Basin(TT)', 'Basin')
                   .replace('Later Heaven', 'LH') for n in names]
    ax.set_xticks(range(len(names)))
    ax.set_yticks(range(len(names)))
    ax.set_xticklabels(short_names, rotation=45, ha='right', fontsize=10)
    ax.set_yticklabels(short_names, fontsize=10)

    # Annotate cells
    for i in range(len(names)):
        for j in range(len(names)):
            color = 'white' if nmi[i, j] > 0.6 else 'black'
            ax.text(j, i, f"{nmi[i,j]:.2f}", ha='center', va='center',
                   fontsize=9, color=color, fontweight='bold')

    ax.set_title("Normalized Mutual Information (NMI)\n6 Trigram Partitions",
                fontsize=13, fontweight='bold')
    plt.colorbar(im, ax=ax, shrink=0.8, label='NMI')
    plt.tight_layout()

    for ext in ('png', 'svg'):
        path = OUTDIR / f"02_mi_matrix.{ext}"
        fig.savefig(str(path), dpi=150, bbox_inches='tight')
        print(f"  Saved: {path}")
    plt.close()


# ═══════════════════════════════════════════════════════════════════════
# Markdown Output
# ═══════════════════════════════════════════════════════════════════════

def write_findings(p3_data, p4_trig, p4_inner, p5_sym, p5_decomp, p5_comp, partitions):
    """Write 02_findings.md."""
    lines = []
    w = lines.append

    w("# Phase B: Partition Comparison, Directed Graphs & Quotient Structure\n")

    # ──────── PROBE 3 ────────
    w("## Probe 3: Partition Comparison\n")

    names, H, mi, nmi, cond_h, pair_cond = p3_data

    # Partition descriptions
    w("### Partition definitions\n")
    for name in names:
        part = partitions[name]
        classes = partition_to_classes(part)
        class_strs = []
        for label, members in sorted(classes.items(), key=lambda x: -len(x[1])):
            trig_names = [TRIGRAM_NAMES[t].split()[0] for t in sorted(members)]
            class_strs.append(f"{label}: {{{', '.join(trig_names)}}}")
        w(f"**{name}** (H={H[name]:.4f} bits): {'; '.join(class_strs)}")
    w("")

    # MI matrix
    w("### Mutual Information matrix\n")
    header = "| | " + " | ".join(names) + " |"
    sep = "|---|" + "|".join(["---:"] * len(names)) + "|"
    w(header)
    w(sep)
    for i, name in enumerate(names):
        vals = " | ".join(f"{mi[i,j]:.4f}" for j in range(len(names)))
        w(f"| {name} | {vals} |")
    w("")

    # NMI matrix
    w("### Normalized MI matrix\n")
    w(header)
    w(sep)
    for i, name in enumerate(names):
        vals = " | ".join(f"{nmi[i,j]:.2f}" for j in range(len(names)))
        w(f"| {name} | {vals} |")
    w("")

    # Key observations
    w("### Key observations\n")

    # Highest MI pairs (off-diagonal)
    pairs_mi = []
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            pairs_mi.append((nmi[i,j], names[i], names[j], mi[i,j]))
    pairs_mi.sort(reverse=True)

    w("**Highest NMI pairs:**\n")
    for nmi_val, n1, n2, mi_val in pairs_mi[:5]:
        w(f"- {n1} ↔ {n2}: NMI={nmi_val:.4f}, MI={mi_val:.4f} bits")
    w("")

    w("**Lowest NMI pairs:**\n")
    for nmi_val, n1, n2, mi_val in pairs_mi[-3:]:
        w(f"- {n1} ↔ {n2}: NMI={nmi_val:.4f}, MI={mi_val:.4f} bits")
    w("")

    # Conditional entropy: what best predicts Wuxing?
    w("### Wuxing predictability\n")
    w("H(Wuxing) = {:.4f} bits\n".format(H['Wuxing']))
    w("| Predictor X | H(Wuxing \\| X) | Information gained | % of Wuxing |")
    w("|-------------|---------------|-------------------|-------------|")
    for name in sorted(cond_h, key=cond_h.get):
        gain = H['Wuxing'] - cond_h[name]
        pct = 100 * gain / H['Wuxing'] if H['Wuxing'] > 0 else 0
        w(f"| {name} | {cond_h[name]:.4f} | {gain:.4f} | {pct:.1f}% |")
    w("")

    # Pair predictors
    w("### Pair predictors: H(Wuxing | X, Y)\n")
    w("| X | Y | H(Wuxing \\| X,Y) | Residual % |")
    w("|---|---|-----------------|------------|")
    for (n1, n2), h in sorted(pair_cond.items(), key=lambda x: x[1]):
        pct = 100 * h / H['Wuxing'] if H['Wuxing'] > 0 else 0
        w(f"| {n1} | {n2} | {h:.4f} | {pct:.1f}% |")
    w("")

    # Is Wuxing redundant?
    best_single = min(cond_h.values())
    best_pair = min(pair_cond.values())
    w(f"**Best single predictor leaves {best_single:.4f} bits ({100*best_single/H['Wuxing']:.1f}% of Wuxing)**\n")
    w(f"**Best pair predictor leaves {best_pair:.4f} bits ({100*best_pair/H['Wuxing']:.1f}% of Wuxing)**\n")
    if best_pair < 0.01:
        w("→ Wuxing is fully captured by the best pair of other partitions.\n")
    elif best_pair < best_single * 0.5:
        w("→ Wuxing is partially captured by combining partitions, but retains independent information.\n")
    else:
        w("→ Wuxing carries substantial unique information not captured by any pair of other partitions.\n")

    # ──────── PROBE 4 ────────
    w("## Probe 4: Directed Graphs\n")

    # 4a: Trigram graphs
    w("### 4a. Five-phase graphs on Z₂³ (8 trigrams)\n")
    trig_graphs, trig_degrees = p4_trig

    w("| Relation | Edges | In-degree range | Out-degree range |")
    w("|----------|-------|-----------------|------------------|")
    for rel in ALL_RELS:
        d = trig_degrees[rel]
        in_vals = list(d['in_deg'].values()) if d['in_deg'] else [0]
        out_vals = list(d['out_deg'].values()) if d['out_deg'] else [0]
        w(f"| {REL_ZH[rel]} ({rel}) | {d['edges']} | "
          f"{min(in_vals)}–{max(in_vals)} | {min(out_vals)}–{max(out_vals)} |")
    w("")

    total_edges = sum(trig_degrees[r]['edges'] for r in ALL_RELS)
    w(f"**Total:** {total_edges} edges = 8×7 = 56 ✓ (complete digraph minus self-loops)\n")

    # Degree details for gen_fwd and over_fwd
    for rel, label in [('gen_fwd', '生'), ('over_fwd', '克')]:
        w(f"**{label} ({rel}) degree by trigram:**\n")
        w("| Trigram | Element | Out-degree | In-degree |")
        w("|---------|---------|------------|-----------|")
        d = trig_degrees[rel]
        for t in range(N_TRIG):
            od = d['out_deg'].get(t, 0)
            id_ = d['in_deg'].get(t, 0)
            w(f"| {TRIGRAM_NAMES[t]} | {TRIGRAM_ELEMENT[t]} | {od} | {id_} |")
        w("")

    # 4b: Inner space
    w("### 4b. Five-phase on 16-node inner space\n")

    w("#### Combined relation distribution (all ordered pairs)\n")
    w("| Lower rel | Upper rel | Count |")
    w("|-----------|-----------|-------|")
    for (lr, ur), cnt in sorted(p4_inner['both_counts'].items(),
                                key=lambda x: -x[1])[:15]:
        w(f"| {REL_ZH[lr]} | {REL_ZH[ur]} | {cnt} |")
    w("")

    w("#### Hugua edges: five-phase classification\n")
    w(f"Total hugua edges (non-self): {len(p4_inner['hugua_edges'])}\n")
    w("| Lower rel | Upper rel | Count | Basin |")
    w("|-----------|-----------|-------|-------|")
    for e in sorted(p4_inner['hugua_edges'], key=lambda x: x['src']):
        w(f"| {REL_ZH[e['lo_rel']]} | {REL_ZH[e['up_rel']]} | "
          f"{e['src']}→{e['tgt']} | {e['basin']} |")
    w("")

    w(f"**Hugua edges with 生 on at least one position:** "
      f"{p4_inner['hugua_has_gen']}/{len(p4_inner['hugua_edges'])}\n")
    w(f"**Hugua edges with 克 on at least one position:** "
      f"{p4_inner['hugua_has_over']}/{len(p4_inner['hugua_edges'])}\n")
    w(f"**Hugua edges with SAME relation on both positions:** "
      f"{p4_inner['hugua_both_same_type']}/{len(p4_inner['hugua_edges'])}\n")

    # By basin
    w("#### Hugua edge relations by basin\n")
    for basin in ["Kun", "Cycle", "Qian"]:
        edges = p4_inner['hugua_by_basin'].get(basin, [])
        if not edges:
            continue
        rel_dist = defaultdict(int)
        for e in edges:
            rel_dist[(e['lo_rel'], e['up_rel'])] += 1
        w(f"**{basin}** ({len(edges)} edges):")
        for (lr, ur), cnt in sorted(rel_dist.items(), key=lambda x: -x[1]):
            w(f"  - ({REL_ZH[lr]}, {REL_ZH[ur]}): {cnt}")
        w("")

    # ──────── PROBE 5 ────────
    w("## Probe 5: Quotient Structure\n")

    # 5a: Symmetry
    w("### 5a. Symmetry group\n")
    w(f"|GL(3,F₂)| = {p5_sym['gl3_order']}\n")
    w(f"**Linear symmetries preserving Wuxing:** {p5_sym['linear_count']}\n")
    w(f"**Affine symmetries preserving Wuxing:** {p5_sym['affine_count']}\n")

    if p5_sym['linear_count'] > 0:
        w("Linear symmetries (matrices A where A preserves each element class):\n")
        for A in p5_sym['linear_sym']:
            rows = [f"  [{' '.join(str(x) for x in row)}]" for row in A]
            w("```")
            for r in rows:
                w(r)
            w("```")
            # Show what it does
            perm = {t: mat_vec_f2(A, t) for t in range(N_TRIG)}
            perm_str = ", ".join(f"{fmt3(t)}→{fmt3(perm[t])}" for t in range(N_TRIG) if t != perm[t])
            if perm_str:
                w(f"  Action: {perm_str}")
            else:
                w("  Action: identity")
            w("")

    if p5_sym['affine_count'] > p5_sym['linear_count']:
        w("Additional affine symmetries (Ax+b with b≠0):\n")
        for A, b in p5_sym['affine_sym']:
            if b == 0:
                continue  # already shown
            perm = {t: mat_vec_f2(A, t) ^ b for t in range(N_TRIG)}
            perm_str = ", ".join(f"{fmt3(t)}→{fmt3(perm[t])}" for t in range(N_TRIG))
            w(f"- b={fmt3(b)}: {perm_str}")
        w("")

    w("*Note: these count symmetries preserving each **named** element class "
      "(Earth→Earth, Metal→Metal, etc.). The unlabeled partition automorphism group "
      "(allowing class permutation) is larger — see §5d.*\n")

    # 5b: Decomposition
    w("### 5b. Algebraic decomposition\n")
    d = p5_decomp
    w(f"H(Wuxing) = {d['H_wuxing']:.4f} bits\n")
    w("**Decomposition hierarchy:**\n")
    w(f"1. b₀⊕b₁ parity → H(Wuxing | parity) = {d['H_given_parity']:.4f}")
    w(f"   - Information from parity: {d['H_wuxing'] - d['H_given_parity']:.4f} bits")
    w(f"2. + b₀ within parity → H(Wuxing | parity, b₀) = {d['H_given_parity_b0']:.4f}")
    w(f"   - Additional from b₀: {d['H_given_parity'] - d['H_given_parity_b0']:.4f} bits")
    w(f"3. Residual (cosmological): {d['H_given_parity_b0']:.4f} bits\n")
    w(f"**Algebraic bits:** {d['algebraic_bits']:.4f}")
    w(f"**Cosmological bits:** {d['cosmological_bits']:.4f}\n")

    # 5c: The non-linear residual
    w("### 5c. The non-linear residual\n")
    w(f"Parity-0 coset: {{{', '.join(fmt3(t) for t in d['coset_0'])}}} "
      f"→ complement pairs: {d['coset_0_comp_pairs']}")
    w(f"  Wuxing: {{{', '.join(fmt3(t) + '=' + TRIGRAM_ELEMENT[t] for t in d['coset_0'])}}}")
    w(f"  Within this coset, b₀ cleanly separates Earth(b₀=0) from Metal(b₀=1).\n")

    w(f"Parity-1 coset: {{{', '.join(fmt3(t) for t in d['coset_1'])}}} "
      f"→ complement pairs: {d['coset_1_comp_pairs']}")
    w(f"  Wuxing: {{{', '.join(fmt3(t) + '=' + TRIGRAM_ELEMENT[t] for t in d['coset_1'])}}}")
    w(f"  Complement pairs in coset: {len(d['coset_1_comp_pairs'])}")
    w(f"  Traditional choice: keep pair {d['coset_1_comp_pairs'][0]} together → Wood")
    w(f"  Alternative: keep pair {d['coset_1_comp_pairs'][1]} together → would merge Water+Fire")
    w(f"  **This is 1 binary choice** — the sole cosmological input to Wuxing.\n")

    w("**Information accounting:**")
    w(f"- H(Wuxing) = {d['H_wuxing']:.4f} bits")
    w(f"- Algebraic (linear features): {d['algebraic_bits']:.4f} bits")
    w(f"- Cosmological (1 binary choice): {d['cosmological_bits']:.4f} bits")
    w(f"- Sum: {d['algebraic_bits'] + d['cosmological_bits']:.4f} bits ✓\n")

    # 5d: Comparison to all (2,2,2,1,1) partitions
    w("### 5d. Ranking among all (2,2,2,1,1) partitions\n")
    c = p5_comp
    w(f"Total partitions with shape (2,2,2,1,1): **{c['n_parts']}**\n")

    trad = c['trad_idx']
    if trad is not None:
        w(f"Traditional Wuxing = partition #{trad}\n")

        # MI rankings
        for metric_name, values in [
            ('MI with Yang count', c['mi_yang']),
            ('MI with Basin(TT)', c['mi_basin']),
            ('MI with Later Heaven', c['mi_lh']),
            ('Total MI (sum)', c['total_mi']),
        ]:
            arr = np.array(values)
            trad_val = arr[trad]
            rank = int(np.sum(arr > trad_val)) + 1
            pct = 100 * rank / len(arr)
            w(f"- **{metric_name}:** {trad_val:.4f} (rank {rank}/{len(arr)}, top {pct:.1f}%)")
        w("")

    # Affine symmetry group order
    sym_orders = np.array(c['has_affine_sym'])
    if trad is not None:
        trad_order = sym_orders[trad]
        order_rank = int(np.sum(sym_orders > trad_order)) + 1
        w(f"**Affine automorphism group order:**")
        w(f"- Traditional Wuxing: |Aut| = {trad_order}")
        w(f"- Range across all partitions: {sym_orders.min()}–{sym_orders.max()}")
        w(f"- Mean: {sym_orders.mean():.1f}, Median: {np.median(sym_orders):.0f}")
        w(f"- Wuxing rank by |Aut|: {order_rank}/{c['n_parts']} "
          f"(higher = more symmetric)\n")

    # Top partitions by total MI
    w("#### Top 10 partitions by total MI\n")
    ranked = sorted(range(c['n_parts']), key=lambda i: -c['total_mi'][i])
    w("| Rank | MI(Yang) | MI(Basin) | MI(LH) | Total | |Aut| | Is Wuxing? |")
    w("|------|----------|-----------|--------|-------|-------|------------|")
    for rank_idx, idx in enumerate(ranked[:10]):
        is_trad = "✓" if idx == trad else ""
        w(f"| {rank_idx+1} | {c['mi_yang'][idx]:.4f} | {c['mi_basin'][idx]:.4f} | "
          f"{c['mi_lh'][idx]:.4f} | {c['total_mi'][idx]:.4f} | "
          f"{c['has_affine_sym'][idx]} | {is_trad} |")
    w("")

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("PHASE B: PARTITION COMPARISON, DIRECTED GRAPHS & QUOTIENT STRUCTURE")
    print("=" * 70)

    partitions = build_partitions()

    # ── Probe 3 ──
    print("\n── Probe 3: Partition Comparison ──\n")
    p3_data = probe3_mi_matrix(partitions)
    names, H, mi, nmi, cond_h, pair_cond = p3_data

    print("Entropies:")
    for name in names:
        print(f"  {name:18s}: H = {H[name]:.4f}")

    print("\nNMI matrix (upper triangle):")
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            print(f"  {names[i]:18s} ↔ {names[j]:18s}: NMI={nmi[i,j]:.4f}")

    print("\nH(Wuxing | X):")
    for name in sorted(cond_h, key=cond_h.get):
        print(f"  {name:18s}: {cond_h[name]:.4f}")

    print("\nBest pair predictors:")
    for (n1, n2), h in sorted(pair_cond.items(), key=lambda x: x[1])[:3]:
        print(f"  {n1} + {n2}: H(Wuxing|X,Y) = {h:.4f}")

    # ── Probe 4 ──
    print("\n── Probe 4: Directed Graphs ──\n")
    p4_trig_data = probe4_trigram_graphs()
    trig_graphs, trig_degrees = p4_trig_data

    for rel in ALL_RELS:
        d = trig_degrees[rel]
        print(f"  {REL_ZH[rel]:4s} ({rel:9s}): {d['edges']:2d} edges")
    print(f"  Total: {sum(trig_degrees[r]['edges'] for r in ALL_RELS)} edges")

    p4_inner_data = probe4_inner_graphs()
    print(f"\n  Hugua edges: {len(p4_inner_data['hugua_edges'])} non-self")
    print(f"  With 生: {p4_inner_data['hugua_has_gen']}")
    print(f"  With 克: {p4_inner_data['hugua_has_over']}")
    print(f"  Both same type: {p4_inner_data['hugua_both_same_type']}")

    # ── Probe 5 ──
    print("\n── Probe 5: Quotient Structure ──\n")

    print("5a. Symmetry analysis...")
    p5_sym = probe5_symmetry()
    print(f"  Linear symmetries: {p5_sym['linear_count']}")
    print(f"  Affine symmetries: {p5_sym['affine_count']}")

    print("\n5b. Algebraic decomposition...")
    p5_decomp = probe5_decomposition()
    print(f"  H(Wuxing) = {p5_decomp['H_wuxing']:.4f}")
    print(f"  H(Wuxing|parity) = {p5_decomp['H_given_parity']:.4f}")
    print(f"  H(Wuxing|parity,b₀) = {p5_decomp['H_given_parity_b0']:.4f}")
    print(f"  Algebraic: {p5_decomp['algebraic_bits']:.4f}, "
          f"Cosmological: {p5_decomp['cosmological_bits']:.4f}")

    print("\n5d. Comparing to all (2,2,2,1,1) partitions...")
    p5_comp = probe5_comparison(partitions)
    print(f"  Total partitions: {p5_comp['n_parts']}")
    if p5_comp['trad_idx'] is not None:
        t = p5_comp['trad_idx']
        rank = int(np.sum(np.array(p5_comp['total_mi']) > p5_comp['total_mi'][t])) + 1
        print(f"  Traditional Wuxing: idx={t}, total MI rank={rank}/{p5_comp['n_parts']}")

    # ── Visualization ──
    print("\n── Generating visualization ──")
    viz_mi_matrix(names, nmi)

    # ── Write findings ──
    md = write_findings(p3_data, p4_trig_data, p4_inner_data,
                        p5_sym, p5_decomp, p5_comp, partitions)
    out_path = OUTDIR / "02_findings.md"
    out_path.write_text(md)
    print(f"\nFindings written to {out_path}")


if __name__ == '__main__':
    main()
