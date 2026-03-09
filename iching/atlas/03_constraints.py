#!/usr/bin/env python3
"""
MI matrix, joint constraints, and minimal identification analysis.

Loads atlas.json, extracts 13 coordinate vectors, computes:
  1. Pairwise MI matrix (+ NMI)
  2. Residual ambiguity: H(hexagram | full profile)
  3. Minimal identification subsets
  4. Forbidden combinations
  5. Dependency DAG (functional dependencies)

Writes: constraints.json
"""

import json
from math import log2
from pathlib import Path
from collections import Counter
from itertools import combinations


# ─── Entropy primitives ──────────────────────────────────────────────────────

N = 64  # equiprobable hexagrams


def entropy(labels):
    """Shannon entropy in bits over N=64 equiprobable items."""
    counts = Counter(labels)
    return -sum((c / N) * log2(c / N) for c in counts.values() if c > 0)


def joint_entropy(labels_a, labels_b):
    counts = Counter(zip(labels_a, labels_b))
    return -sum((c / N) * log2(c / N) for c in counts.values() if c > 0)


def mi(labels_a, labels_b):
    return entropy(labels_a) + entropy(labels_b) - joint_entropy(labels_a, labels_b)


def joint_entropy_multi(label_lists):
    """Joint entropy of multiple coordinate vectors."""
    tuples = list(zip(*label_lists))
    counts = Counter(tuples)
    return -sum((c / N) * log2(c / N) for c in counts.values() if c > 0)


def n_unique(label_lists):
    """Number of unique joint values."""
    return len(set(zip(*label_lists)))


# ─── Extract coordinates ─────────────────────────────────────────────────────

def extract_coordinates(atlas):
    """Extract 13 coordinate vectors from atlas, each length 64."""
    coords = {}
    for name, key_fn in COORD_DEFS.items():
        coords[name] = [key_fn(atlas[str(h)]) for h in range(N)]
    return coords


COORD_DEFS = {
    "surface_cell":     lambda e: tuple(e["surface_cell"]),
    "hu_cell":          lambda e: tuple(e["hu_cell"]),
    "surface_relation": lambda e: e["surface_relation"],
    "hu_relation":      lambda e: e["hu_relation"],
    "basin":            lambda e: e["basin"],
    "depth":            lambda e: e["depth"],
    "palace":           lambda e: e["palace"],
    "palace_element":   lambda e: e["palace_element"],
    "rank":             lambda e: e["rank"],
    "i_component":      lambda e: e["i_component"],
    "hu_attractor":     lambda e: e["hu_attractor"],
    "inner_val":        lambda e: e["inner_val"],
    "liuqin_word":      lambda e: tuple(e["liuqin_word"]),
}

COORD_NAMES = list(COORD_DEFS.keys())


# ─── Part 1: MI matrix ──────────────────────────────────────────────────────

def compute_mi_matrix(coords):
    names = COORD_NAMES
    n = len(names)

    # Entropies
    H = {name: entropy(coords[name]) for name in names}

    # MI matrix
    mi_mat = {}
    nmi_mat = {}
    for a in names:
        mi_mat[a] = {}
        nmi_mat[a] = {}
        for b in names:
            v = mi(coords[a], coords[b])
            mi_mat[a][b] = round(v, 6)
            denom = min(H[a], H[b])
            nmi_mat[a][b] = round(v / denom, 6) if denom > 1e-12 else 0.0

    return H, mi_mat, nmi_mat


def print_mi_matrix(H, mi_mat, nmi_mat):
    names = COORD_NAMES
    short = [n[:10] for n in names]

    print("=" * 70)
    print("PART 1: MUTUAL INFORMATION MATRIX")
    print("=" * 70)

    # Entropies
    print("\nEntropies (bits):")
    for name in names:
        n_vals = len(set(COORD_DEFS[name]({"surface_cell": ["a","b"], "hu_cell": ["a","b"],
            "surface_relation": "x", "hu_relation": "x", "basin": "x", "depth": 0,
            "palace": "x", "palace_element": "x", "rank": 0, "i_component": 0,
            "hu_attractor": 0, "inner_val": 0, "liuqin_word": ["a"]*6})
            for _ in "x"))  # dummy — just use actual H
        print(f"  {name:20s}: H = {H[name]:.4f} bits")

    # MI matrix (condensed)
    print(f"\nMI matrix (bits):")
    header = f"{'':20s} " + " ".join(f"{s:>10s}" for s in short)
    print(header)
    for a in names:
        row = " ".join(f"{mi_mat[a][b]:10.4f}" for b in names)
        print(f"{a:20s} {row}")

    # NMI matrix (condensed)
    print(f"\nNMI matrix (MI / min(H(X), H(Y))):")
    print(header)
    for a in names:
        row = " ".join(f"{nmi_mat[a][b]:10.4f}" for b in names)
        print(f"{a:20s} {row}")

    # High MI pairs (off-diagonal)
    print(f"\nTop MI pairs (NMI > 0.3, off-diagonal):")
    pairs = []
    for i, a in enumerate(names):
        for j, b in enumerate(names):
            if j > i and nmi_mat[a][b] > 0.3:
                pairs.append((nmi_mat[a][b], mi_mat[a][b], a, b))
    for nmi_v, mi_v, a, b in sorted(pairs, reverse=True):
        print(f"  NMI={nmi_v:.4f}  MI={mi_v:.4f}  {a} × {b}")


# ─── Part 2: Residual ambiguity ─────────────────────────────────────────────

def compute_residual(coords):
    all_labels = [coords[name] for name in COORD_NAMES]
    h_joint = joint_entropy_multi(all_labels)
    h_hex = log2(N)  # 6.0
    n_distinct = n_unique(all_labels)
    return h_hex, h_joint, h_hex - h_joint, n_distinct


def print_residual(h_hex, h_joint, residual, n_distinct):
    print("\n" + "=" * 70)
    print("PART 2: RESIDUAL AMBIGUITY")
    print("=" * 70)
    print(f"  H(hexagram)     = {h_hex:.4f} bits")
    print(f"  H(full profile) = {h_joint:.4f} bits")
    print(f"  Residual        = {residual:.4f} bits")
    print(f"  Distinct joint profiles: {n_distinct} / 64")
    if n_distinct == 64:
        print("  → Full profile uniquely identifies every hexagram.")
    else:
        print(f"  → {64 - n_distinct} collisions remain.")


# ─── Part 3: Minimal identification sets ─────────────────────────────────────

def test_identification(coords, subset_names):
    """Return number of distinct joint values for a subset of coordinates."""
    labels = [coords[name] for name in subset_names]
    return n_unique(labels)


def find_minimal_sets(coords):
    names = COORD_NAMES
    results = []

    # Test singletons
    for name in names:
        n = test_identification(coords, [name])
        if n == 64:
            results.append(([name], n, "singleton"))

    # Test specified pairs
    test_pairs = [
        ["liuqin_word", "surface_cell"],
        ["liuqin_word", "basin"],
        ["liuqin_word", "i_component"],
        ["surface_cell", "inner_val"],
        ["surface_cell", "hu_cell"],
        ["surface_cell", "palace"],
        ["surface_cell", "rank"],
        ["palace", "rank"],
        ["liuqin_word", "hu_cell"],
        ["liuqin_word", "depth"],
    ]
    for pair in test_pairs:
        n = test_identification(coords, pair)
        results.append((pair, n, "specified"))

    # Exhaustive search for all identifying pairs
    identifying_pairs = []
    for a, b in combinations(names, 2):
        if test_identification(coords, [a, b]) == 64:
            identifying_pairs.append([a, b])

    # Find all identifying triples (only if no identifying pairs exist... but let's report both)
    # Just find a few triples from non-identifying pairs
    non_id_pairs = []
    for a, b in combinations(names, 2):
        if test_identification(coords, [a, b]) < 64:
            non_id_pairs.append((a, b))

    identifying_triples = []
    for a, b in non_id_pairs[:20]:  # sample
        for c in names:
            if c != a and c != b:
                if test_identification(coords, [a, b, c]) == 64:
                    triple = sorted([a, b, c])
                    if triple not in identifying_triples:
                        identifying_triples.append(triple)

    return results, identifying_pairs, identifying_triples


def print_minimal_sets(results, id_pairs, id_triples):
    print("\n" + "=" * 70)
    print("PART 3: MINIMAL IDENTIFICATION SETS")
    print("=" * 70)

    print("\nSpecified tests:")
    for subset, n, tag in results:
        status = "✓ IDENTIFIES" if n == 64 else f"  {n}/64"
        print(f"  {status}  {' + '.join(subset)}")

    print(f"\nAll identifying pairs ({len(id_pairs)}):")
    for pair in sorted(id_pairs):
        print(f"  ✓ {' + '.join(pair)}")

    if id_triples:
        print(f"\nSample identifying triples ({len(id_triples)} found):")
        for triple in sorted(id_triples)[:10]:
            print(f"  ✓ {' + '.join(triple)}")


# ─── Part 4: Forbidden combinations ─────────────────────────────────────────

def cross_tab(coords, name_a, name_b):
    """Return (realized set, possible set, empty set)."""
    vals_a = sorted(set(coords[name_a]), key=str)
    vals_b = sorted(set(coords[name_b]), key=str)
    possible = {(a, b) for a in vals_a for b in vals_b}
    realized = set(zip(coords[name_a], coords[name_b]))
    empty = possible - realized
    return realized, possible, empty


def print_forbidden(coords):
    print("\n" + "=" * 70)
    print("PART 4: FORBIDDEN COMBINATIONS")
    print("=" * 70)

    pairs_to_check = [
        ("surface_relation", "hu_relation"),
        ("surface_relation", "basin"),
        ("hu_relation", "basin"),
        ("surface_cell", "hu_cell"),
    ]

    forbidden_data = {}
    for a, b in pairs_to_check:
        realized, possible, empty = cross_tab(coords, a, b)
        print(f"\n  {a} × {b}:")
        print(f"    Possible: {len(possible)}, Realized: {len(realized)}, "
              f"Forbidden: {len(empty)}")

        if len(empty) <= 30:
            print(f"    Empty cells:")
            for va, vb in sorted(empty, key=str):
                print(f"      ({va}, {vb})")

        # Also print the cross-tab
        vals_a = sorted(set(coords[a]), key=str)
        vals_b = sorted(set(coords[b]), key=str)
        counts = Counter(zip(coords[a], coords[b]))

        # Compact table
        if len(vals_a) <= 8 and len(vals_b) <= 8:
            col_w = max(len(str(v)) for v in vals_b)
            col_w = max(col_w, 4)
            header = f"    {'':20s} " + " ".join(f"{str(v):>{col_w}s}" for v in vals_b)
            print(header)
            for va in vals_a:
                row = " ".join(f"{counts.get((va, vb), 0):>{col_w}d}" for vb in vals_b)
                print(f"    {str(va):20s} {row}")

        forbidden_data[f"{a}_x_{b}"] = {
            "possible": len(possible),
            "realized": len(realized),
            "forbidden": len(empty),
            "empty_cells": [list(map(str, cell)) for cell in sorted(empty, key=str)],
        }

    return forbidden_data


# ─── Part 5: Dependency graph ────────────────────────────────────────────────

def compute_dependencies(H, mi_mat):
    """Find functional dependencies: X → Y iff MI(X,Y) ≈ H(Y)."""
    edges = []
    EPS = 1e-6
    for a in COORD_NAMES:
        for b in COORD_NAMES:
            if a == b:
                continue
            # X determines Y iff MI(X,Y) = H(Y)
            if abs(mi_mat[a][b] - H[b]) < EPS:
                edges.append((a, b))
    return edges


def print_dependencies(edges, H):
    print("\n" + "=" * 70)
    print("PART 5: DEPENDENCY GRAPH (functional: X → Y iff MI = H(Y))")
    print("=" * 70)

    # Group by source
    from collections import defaultdict
    by_src = defaultdict(list)
    for a, b in edges:
        by_src[a].append(b)

    # Remove transitive edges for display
    # (If A→B and B→C, don't show A→C)
    direct_targets = defaultdict(set)
    for a, targets in by_src.items():
        direct_targets[a] = set(targets)

    # Simple transitive reduction
    for a in COORD_NAMES:
        if a not in direct_targets:
            continue
        # For each target t of a, remove anything that t determines
        to_remove = set()
        for t in direct_targets[a]:
            if t in direct_targets:
                to_remove |= direct_targets[t]
        direct_targets[a] -= to_remove

    print("\nFull edges:")
    for a, b in sorted(edges):
        print(f"  {a} → {b}")

    print(f"\nReduced DAG (transitive reduction):")
    for a in COORD_NAMES:
        if a in direct_targets and direct_targets[a]:
            targets = sorted(direct_targets[a])
            print(f"  {a} → {', '.join(targets)}")

    # Who is determined by whom?
    print(f"\nDetermination summary:")
    for b in COORD_NAMES:
        determiners = [a for a, t in edges if t == b]
        if determiners:
            print(f"  {b} (H={H[b]:.3f}) ← determined by: {', '.join(sorted(determiners))}")
        else:
            print(f"  {b} (H={H[b]:.3f}) ← independent (no single determiner)")

    return {a: sorted(v) for a, v in direct_targets.items() if v}


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    atlas_path = Path(__file__).parent / "atlas.json"
    with open(atlas_path, encoding='utf-8') as f:
        atlas = json.load(f)

    coords = extract_coordinates(atlas)

    # Part 1
    H, mi_mat, nmi_mat = compute_mi_matrix(coords)
    print_mi_matrix(H, mi_mat, nmi_mat)

    # Part 2
    h_hex, h_joint, residual, n_distinct = compute_residual(coords)
    print_residual(h_hex, h_joint, residual, n_distinct)

    # Part 3
    results, id_pairs, id_triples = find_minimal_sets(coords)
    print_minimal_sets(results, id_pairs, id_triples)

    # Part 4
    forbidden_data = print_forbidden(coords)

    # Part 5
    edges = compute_dependencies(H, mi_mat)
    dag = print_dependencies(edges, H)

    # ── Write JSON ──
    out = {
        "entropies": {k: round(v, 6) for k, v in H.items()},
        "mi_matrix": mi_mat,
        "nmi_matrix": nmi_mat,
        "residual": {
            "h_hexagram": round(h_hex, 6),
            "h_joint_profile": round(h_joint, 6),
            "residual_bits": round(residual, 6),
            "distinct_profiles": n_distinct,
        },
        "identifying_pairs": [sorted(p) for p in id_pairs],
        "identifying_triples_sample": [sorted(t) for t in id_triples[:20]],
        "forbidden_combinations": forbidden_data,
        "dependency_edges": [(a, b) for a, b in sorted(edges)],
        "dependency_dag_reduced": dag,
    }

    out_path = Path(__file__).parent / "constraints.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()
