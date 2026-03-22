#!/usr/bin/env python3
"""
GMS bigram test: are consecutive 克-typed Q₃ transitions suppressed?

Two framings:
  A (strict temporal): consecutive bars both undergo Q₃-edge transitions
  B (Q₃ walk): extract Q₃-edge-only sequence, ignoring self-loops/multi-axis

Three null models:
  A: independence (P(克)² based on marginal 克 fraction)
  B: vertex-conditional (empirical transition probabilities from each vertex)
  C: permutation (shuffle edge-type labels, 10k iterations)
"""

import pandas as pd
import numpy as np
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from market_regime_predictions import (
    Z5_TYPING, Z5_NAMES, REGIMES, VERTICES, EDGES, AXIS_NAMES,
    edge_type as z5_edge_type, flipped_axis, find_paths,
)
from market_partition_test import build_bars, DATA_PATH

N_PERMUTATIONS = 10_000


# ── Build full transition sequence ───────────────────────────────────

def build_transition_sequence(bars):
    """Return list of dicts for each bar→bar transition."""
    v = bars['vertex'].values.astype(int)
    transitions = []
    for i in range(len(v) - 1):
        u, w = int(v[i]), int(v[i + 1])
        xor = u ^ w
        hamming = bin(xor).count('1')
        if hamming == 0:
            etype = 'self'
        elif hamming == 1:
            etype = z5_edge_type(Z5_TYPING[u], Z5_TYPING[w])
        else:
            etype = 'multi'
        transitions.append({
            'bar_idx': i, 'u': u, 'w': w,
            'hamming': hamming, 'edge_type': etype,
            'is_q3': hamming == 1,
        })
    return transitions


# ── Framing A: strict temporal adjacency ─────────────────────────────

def framing_a(transitions):
    """Count 克→克 among temporally adjacent Q₃-edge pairs."""
    n = len(transitions)
    bigrams = defaultdict(int)
    n_pairs = 0

    for i in range(n - 1):
        t1, t2 = transitions[i], transitions[i + 1]
        if not (t1['is_q3'] and t2['is_q3']):
            continue
        n_pairs += 1
        key = (t1['edge_type'], t2['edge_type'])
        bigrams[key] += 1

    return bigrams, n_pairs


# ── Framing B: Q₃ walk (skip non-Q₃ events) ────────────────────────

def framing_b(transitions):
    """Extract Q₃-edge-only sequence, count consecutive 克→克."""
    q3_edges = [t for t in transitions if t['is_q3']]
    bigrams = defaultdict(int)
    n_pairs = len(q3_edges) - 1

    for i in range(n_pairs):
        key = (q3_edges[i]['edge_type'], q3_edges[i + 1]['edge_type'])
        bigrams[key] += 1

    return bigrams, n_pairs, q3_edges


# ── Null A: independence ─────────────────────────────────────────────

def null_a(q3_edges, n_pairs):
    """P(克→克) = P(克)² under independence."""
    n_ke = sum(1 for t in q3_edges if t['edge_type'] == '克')
    p_ke = n_ke / len(q3_edges)
    expected = p_ke * p_ke * n_pairs
    return p_ke, expected


# ── Null B: vertex-conditional ───────────────────────────────────────

def null_b(q3_edges, n_pairs):
    """P(克→克) using empirical P(next_type=克 | at vertex v)."""
    # Count: from each vertex, how often is the next Q₃ edge 克-typed?
    # "next Q₃ edge from v" = the Q₃ edge DEPARTING from v
    depart_counts = defaultdict(lambda: defaultdict(int))
    for t in q3_edges:
        depart_counts[t['u']][t['edge_type']] += 1

    p_ke_from = {}
    for v in VERTICES:
        total = sum(depart_counts[v].values())
        p_ke_from[v] = depart_counts[v]['克'] / total if total > 0 else 0

    # For each consecutive pair in the Q₃ walk: if edge i arrives at vertex w,
    # the next edge departs from w. P(next=克 | at w) = p_ke_from[w].
    # P(克→克) = sum over 克 edges arriving at w: P(arriving 克) × P(departing 克 from w)
    expected_ke_ke = 0
    for i in range(len(q3_edges) - 1):
        if q3_edges[i]['edge_type'] == '克':
            dest = q3_edges[i]['w']
            expected_ke_ke += p_ke_from[dest]

    return expected_ke_ke, p_ke_from


# ── Null C: permutation ─────────────────────────────────────────────

def null_c_walk(q3_edges, observed_ke_ke, n_perm=N_PERMUTATIONS):
    """Shuffle edge-type labels among the Q₃ walk, count 克→克 each time."""
    types = [t['edge_type'] for t in q3_edges]
    rng = np.random.default_rng(42)
    counts = np.zeros(n_perm)

    for p in range(n_perm):
        shuffled = types.copy()
        rng.shuffle(shuffled)
        c = sum(1 for i in range(len(shuffled) - 1)
                if shuffled[i] == '克' and shuffled[i + 1] == '克')
        counts[p] = c

    p_value = (counts <= observed_ke_ke).mean()
    return counts, p_value


def null_c_temporal(transitions, observed_ke_ke, n_perm=N_PERMUTATIONS):
    """Shuffle edge-type labels among Q₃ edges in the full sequence, count temporal 克→克."""
    q3_indices = [i for i, t in enumerate(transitions) if t['is_q3']]
    types = [transitions[i]['edge_type'] for i in q3_indices]
    rng = np.random.default_rng(42)
    counts = np.zeros(n_perm)

    for p in range(n_perm):
        shuffled = types.copy()
        rng.shuffle(shuffled)
        # Reconstruct type map
        type_map = {q3_indices[j]: shuffled[j] for j in range(len(q3_indices))}
        c = 0
        for i in range(len(transitions) - 1):
            if transitions[i]['is_q3'] and transitions[i + 1]['is_q3']:
                if type_map[i] == '克' and type_map[i + 1] == '克':
                    c += 1
        counts[p] = c

    p_value = (counts <= observed_ke_ke).mean()
    return counts, p_value


# ── P₄ path analysis ────────────────────────────────────────────────

def p4_analysis(q3_edges):
    """Check how many 克→克 bigrams fall on the two P₄ paths."""
    ke_paths = find_paths('克')

    # Build set of forbidden directed 3-step sequences (v_a →克→ v_b →克→ v_c)
    # Each P₄ has 2 consecutive克 pairs, each pair can go in 2 directions
    forbidden_triples = set()
    for path in ke_paths:
        for j in range(len(path) - 2):
            a, b, c = path[j], path[j + 1], path[j + 2]
            forbidden_triples.add((a, b, c))
            forbidden_triples.add((c, b, a))  # reverse direction

    # Count 克→克 in Q₃ walk and check if they're on P₄
    on_p4 = 0
    off_p4 = 0
    ke_ke_details = []

    for i in range(len(q3_edges) - 1):
        e1, e2 = q3_edges[i], q3_edges[i + 1]
        if e1['edge_type'] == '克' and e2['edge_type'] == '克':
            triple = (e1['u'], e1['w'], e2['w'])
            is_on_p4 = triple in forbidden_triples
            if is_on_p4:
                on_p4 += 1
            else:
                off_p4 += 1
            ke_ke_details.append({
                'from': e1['u'], 'via': e1['w'], 'to': e2['w'],
                'on_p4': is_on_p4,
            })

    return on_p4, off_p4, ke_ke_details, forbidden_triples, ke_paths


# ── Main ─────────────────────────────────────────────────────────────

def main():
    print("Loading raw data...")
    cols = ['timestamp', 'price', 'trend_4h', 'realized_vol_4h', 'ob100_ratio_1m']
    df = pd.read_csv(DATA_PATH, usecols=cols)
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df = df.set_index('datetime')
    print(f"  {len(df):,} rows\n")

    bars = build_bars(df, '1h')
    transitions = build_transition_sequence(bars)

    n_total = len(transitions)
    n_q3 = sum(1 for t in transitions if t['is_q3'])
    n_self = sum(1 for t in transitions if t['edge_type'] == 'self')
    n_multi = sum(1 for t in transitions if t['edge_type'] == 'multi')
    print(f"1h bars: {len(bars)}, transitions: {n_total}")
    print(f"  Q₃ edges: {n_q3} ({100*n_q3/n_total:.1f}%)")
    print(f"  Self-loops: {n_self} ({100*n_self/n_total:.1f}%)")
    print(f"  Multi-axis: {n_multi} ({100*n_multi/n_total:.1f}%)")

    q3_only = [t for t in transitions if t['is_q3']]
    type_counts = defaultdict(int)
    for t in q3_only:
        type_counts[t['edge_type']] += 1
    print(f"\n  Q₃ type distribution:")
    for tp in ['比和', '生', '克']:
        print(f"    {tp}: {type_counts[tp]} ({100*type_counts[tp]/n_q3:.1f}%)")

    # ══════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("FRAMING A: STRICT TEMPORAL ADJACENCY")
    print("=" * 70)

    bigrams_a, n_pairs_a = framing_a(transitions)
    ke_ke_a = bigrams_a.get(('克', '克'), 0)

    print(f"\n  Temporally adjacent Q₃-edge pairs: {n_pairs_a}")
    print(f"  克→克 observed: {ke_ke_a}")

    # Full bigram table
    print(f"\n  Bigram table (row=first, col=second):")
    types = ['比和', '生', '克']
    print(f"  {'':>6}", end='')
    for t2 in types:
        print(f"  {t2:>6}", end='')
    print()
    for t1 in types:
        print(f"  {t1:>6}", end='')
        for t2 in types:
            c = bigrams_a.get((t1, t2), 0)
            print(f"  {c:>6}", end='')
        print()

    # Null A
    p_ke_a, exp_a = null_a(q3_only, n_pairs_a)
    print(f"\n  Null A (independence): P(克)={p_ke_a:.4f}, "
          f"expected 克→克={exp_a:.1f}, observed={ke_ke_a}")
    print(f"    ratio observed/expected = {ke_ke_a/exp_a:.3f}" if exp_a > 0 else "")

    # Null C (temporal)
    print(f"\n  Null C (permutation, {N_PERMUTATIONS:,} shuffles)...")
    perm_counts_a, p_val_a = null_c_temporal(transitions, ke_ke_a)
    print(f"    permutation mean={perm_counts_a.mean():.1f}, "
          f"std={perm_counts_a.std():.1f}")
    print(f"    observed={ke_ke_a}, p-value (≤observed)={p_val_a:.4f}")
    print(f"    {'✓ SUPPRESSED' if p_val_a < 0.05 else '✗ NOT SUPPRESSED'} at α=0.05")

    # ══════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("FRAMING B: Q₃ WALK (skip non-Q₃ events)")
    print("=" * 70)

    bigrams_b, n_pairs_b, q3_walk = framing_b(transitions)
    ke_ke_b = bigrams_b.get(('克', '克'), 0)

    print(f"\n  Q₃ walk length: {len(q3_walk)} steps, {n_pairs_b} consecutive pairs")
    print(f"  克→克 observed: {ke_ke_b}")

    # Full bigram table
    print(f"\n  Bigram table (row=first, col=second):")
    print(f"  {'':>6}", end='')
    for t2 in types:
        print(f"  {t2:>6}", end='')
    print()
    for t1 in types:
        print(f"  {t1:>6}", end='')
        for t2 in types:
            c = bigrams_b.get((t1, t2), 0)
            print(f"  {c:>6}", end='')
        print()

    # Null A
    p_ke_b, exp_b = null_a(q3_walk, n_pairs_b)
    print(f"\n  Null A (independence): P(克)={p_ke_b:.4f}, "
          f"expected 克→克={exp_b:.1f}, observed={ke_ke_b}")
    print(f"    ratio observed/expected = {ke_ke_b/exp_b:.3f}" if exp_b > 0 else "")

    # Null B
    exp_ke_ke_b, p_ke_from = null_b(q3_walk, n_pairs_b)
    print(f"\n  Null B (vertex-conditional): expected 克→克={exp_ke_ke_b:.1f}, "
          f"observed={ke_ke_b}")
    print(f"    ratio observed/expected = {ke_ke_b/exp_ke_ke_b:.3f}"
          if exp_ke_ke_b > 0 else "")
    print(f"    P(next Q₃ edge is 克 | at vertex v):")
    for v in VERTICES:
        print(f"      {v:03b} {REGIMES[v]:>20}: {p_ke_from[v]:.3f}")

    # Null C (walk)
    print(f"\n  Null C (permutation, {N_PERMUTATIONS:,} shuffles)...")
    perm_counts_b, p_val_b = null_c_walk(q3_walk, ke_ke_b)
    print(f"    permutation mean={perm_counts_b.mean():.1f}, "
          f"std={perm_counts_b.std():.1f}")
    print(f"    observed={ke_ke_b}, p-value (≤observed)={p_val_b:.4f}")
    print(f"    {'✓ SUPPRESSED' if p_val_b < 0.05 else '✗ NOT SUPPRESSED'} at α=0.05")

    # ══════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("P₄ PATH ANALYSIS")
    print("=" * 70)

    on_p4, off_p4, details, forbidden, ke_paths = p4_analysis(q3_walk)
    total_ke_ke = on_p4 + off_p4

    print(f"\n  Total 克→克 in Q₃ walk: {total_ke_ke}")
    print(f"    On P₄ paths (GMS-forbidden): {on_p4}")
    print(f"    Off P₄ paths:                {off_p4}")

    print(f"\n  P₄ paths:")
    for i, path in enumerate(ke_paths):
        labels = " →克→ ".join(f"{REGIMES[v]} ({v:03b})" for v in path)
        print(f"    Path {i+1}: {labels}")

    print(f"\n  Forbidden 3-step sequences (克→克 on P₄):")
    for triple in sorted(forbidden):
        a, b, c = triple
        ax1 = flipped_axis(min(a,b), max(a,b))
        ax2 = flipped_axis(min(b,c), max(b,c))
        print(f"    {REGIMES[a]:>20} →克({AXIS_NAMES[ax1]})→ "
              f"{REGIMES[b]} →克({AXIS_NAMES[ax2]})→ {REGIMES[c]}")

    if details:
        print(f"\n  Observed 克→克 detail:")
        for d in details:
            tag = "P₄-FORBIDDEN" if d['on_p4'] else "off-path"
            a, b, c = d['from'], d['via'], d['to']
            print(f"    {a:03b}→{b:03b}→{c:03b}  "
                  f"({REGIMES[a][:12]}→{REGIMES[b][:12]}→{REGIMES[c][:12]})  [{tag}]")
    else:
        print(f"\n  No 克→克 bigrams observed in Q₃ walk.")

    # Note about P₄ interpretation
    if total_ke_ke > 0:
        print(f"\n  NOTE: 克→克 off P₄ paths can occur when the intermediate vertex")
        print(f"  is not on a P₄ (e.g., 克(trend) followed by 克(trend) at a different")
        print(f"  vertex — these are not graph-adjacent 克 steps on the same path).")

    # ══════════════════════════════════════════════════════════════════
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"""
  Dataset: 1h BTC bars, 2025-07-21 to 2026-02-20
  Axes: trend (trend_4h), volatility (realized_vol_4h), liquidity (ob100_ratio_1m)
  Q₃ edges: {n_q3} total, 克={type_counts['克']} ({100*type_counts['克']/n_q3:.1f}%)

  FRAMING A (strict temporal adjacency):
    Adjacent Q₃ pairs: {n_pairs_a}
    克→克 observed: {ke_ke_a}
    Expected (independence): {exp_a:.1f}
    Permutation p-value: {p_val_a:.4f} {'← SUPPRESSED' if p_val_a < 0.05 else '← NOT SUPPRESSED'}

  FRAMING B (Q₃ walk):
    Walk length: {len(q3_walk)} steps, {n_pairs_b} pairs
    克→克 observed: {ke_ke_b}
    Expected (independence): {exp_b:.1f}
    Expected (vertex-conditional): {exp_ke_ke_b:.1f}
    Permutation p-value: {p_val_b:.4f} {'← SUPPRESSED' if p_val_b < 0.05 else '← NOT SUPPRESSED'}

  P₄ PATH:
    克→克 on P₄ (GMS-forbidden): {on_p4}
    克→克 off P₄: {off_p4}

  GMS VERDICT: {'克→克 suppression DETECTED' if p_val_b < 0.05 or p_val_a < 0.05 else 'NO suppression detected — GMS does not hold for this domain'}
""")


if __name__ == '__main__':
    main()
