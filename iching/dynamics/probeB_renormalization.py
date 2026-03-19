"""
Probe B: 互 as Renormalization (with A→B bridge)

Tests whether the 互 map descends to the GMS quotient (=bipartite double cover
relationship from Probe A) and whether it satisfies formal RG properties.
"""

import json
import numpy as np
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"

PHI = (1 + 5**0.5) / 2

# ── Shared helpers ────────────────────────────────────────────────

def load_atlas():
    with open(ATLAS_DIR / "atlas.json") as f:
        return json.load(f)

def get_trigram_elements(atlas):
    elems = {}
    for hex_data in atlas.values():
        for key in ("lower_trigram", "upper_trigram"):
            t = hex_data[key]
            elems[t["val"]] = t["element"]
    return elems

SHENG = {"Wood": "Fire", "Fire": "Earth", "Earth": "Metal", "Metal": "Water", "Water": "Wood"}
KE = {"Wood": "Earth", "Earth": "Water", "Water": "Fire", "Fire": "Metal", "Metal": "Wood"}
GROUP_NAMES = ["比和", "生", "克"]

def wuxing_group(e1, e2):
    if e1 == e2: return "比和"
    if SHENG[e1] == e2 or SHENG[e2] == e1: return "生"
    return "克"

TRIGRAM_NAMES = {0: "Kun☷", 1: "Zhen☳", 2: "Kan☵", 3: "Gen☶",
                 4: "Dui☱", 5: "Li☲", 6: "Xun☴", 7: "Qian☰"}

def hu_formula(h):
    """互 map: bits [1,2,3,2,3,4] of source → bits [0,1,2,3,4,5] of output."""
    b = [(h >> i) & 1 for i in range(6)]
    return b[1] | (b[2] << 1) | (b[3] << 2) | (b[2] << 3) | (b[3] << 4) | (b[4] << 5)

def hamming(a, b):
    return bin(a ^ b).count('1')

def popcount(x):
    return bin(x).count('1')

def bits(h):
    """Return 6-bit list [b0, b1, ..., b5]."""
    return [(h >> i) & 1 for i in range(6)]


# ══════════════════════════════════════════════════════════════════
# PART 1: 互 and P₄ Bipartite Parity (Bridge from Probe A)
# ══════════════════════════════════════════════════════════════════

def part1(atlas, trigram_elements):
    print("\n" + "═" * 70)
    print("PART 1: 互 AND P₄ BIPARTITE PARITY")
    print("═" * 70)
    results = {}

    # The two 克 P₄ paths and their bipartitions:
    # Path 1: Kan(2) — Kun(0) — Zhen(1) — Gen(3)
    #   Bipartition: even-position = {Kan(2), Zhen(1)}, odd-position = {Kun(0), Gen(3)}
    # Path 2: Dui(4) — Xun(6) — Qian(7) — Li(5)
    #   Bipartition: even-position = {Dui(4), Qian(7)}, odd-position = {Xun(6), Li(5)}

    # Assign parity class for each trigram in the 克 graph
    # Even (class 0) = endpoints of path, Odd (class 1) = interior of path
    # Path 1: 2-0-1-3 → positions 0,1,2,3 → parity = position % 2
    path1 = [2, 0, 1, 3]
    path2 = [4, 6, 7, 5]

    parity = {}
    for i, v in enumerate(path1):
        parity[v] = i % 2
    for i, v in enumerate(path2):
        parity[v] = i % 2

    print("\n── 1a. Trigram Bipartition Classes ──")
    class0 = sorted(v for v, p in parity.items() if p == 0)
    class1 = sorted(v for v, p in parity.items() if p == 1)
    print(f"  Class 0 (even): {[f'{v}({TRIGRAM_NAMES[v]},{trigram_elements[v]})' for v in class0]}")
    print(f"  Class 1 (odd):  {[f'{v}({TRIGRAM_NAMES[v]},{trigram_elements[v]})' for v in class1]}")

    results["trigram_parity"] = {str(k): v for k, v in parity.items()}
    results["class0"] = class0
    results["class1"] = class1

    # ── 1b: Trigram-level 互 map ──────────────────────────────────
    print("\n── 1b. Trigram-Level 互 Map ──")
    # The 互 map on trigrams: for a trigram t with bits [b0, b1, b2],
    # the "nuclear" lower trigram = bits [1,2,3] of hex → but at the trigram level,
    # there's no direct analog. Instead, examine the INDUCED map on trigram pairs.
    #
    # A hexagram h has lower trigram L = h & 7 and upper trigram U = (h >> 3) & 7.
    # hu(h) has lower trigram L' and upper trigram U'.
    # What is the relationship (L,U) → (L', U')?

    print("  Hexagram (L,U) → hu → (L', U') mapping:")
    lu_map = {}
    for h in range(64):
        L = h & 7
        U = (h >> 3) & 7
        hh = hu_formula(h)
        L2 = hh & 7
        U2 = (hh >> 3) & 7
        lu_map[(L, U)] = (L2, U2)

    # Check if the map depends only on (L, U) — i.e., is it well-defined on trigram pairs?
    # Yes, because hex = L + 8*U and hu only depends on bits of hex.
    # But let's verify and print a few examples.
    print("  (L, U) → (L', U') for all 64 hexagrams:")
    # Group by (L,U) to verify uniqueness
    for L in range(8):
        for U in range(8):
            h = L + 8 * U
            hh = hu_formula(h)
            L2, U2 = hh & 7, (hh >> 3) & 7
            lu_map[(L, U)] = (L2, U2)

    # Print the explicit formula
    # hu(h): output bit i comes from input bit [1,2,3,2,3,4]
    # So: L' = [b1, b2, b3] and U' = [b2, b3, b4]
    # where b_i are bits of h, L = [b0,b1,b2], U = [b3,b4,b5]
    # L' = [L_b1, L_b2, U_b0] = shift-up of L with U_b0 injected at top
    # U' = [L_b2, U_b0, U_b1] = mixed from both trigrams
    print("\n  Explicit formula:")
    print("    L = [b0, b1, b2], U = [b3, b4, b5]")
    print("    L' = [b1, b2, b3] = [L₁, L₂, U₀]")
    print("    U' = [b2, b3, b4] = [L₂, U₀, U₁]")
    print("    ⟹ 互 shifts the trigram window inward by 1 bit")
    print("    L and U share bits b2 and b3 in the output (the hinge bits)")

    # ── 1c: Parity tracking under 互 ─────────────────────────────
    print("\n── 1c. Parity Tracking Under 互 ──")

    # For each hexagram, classify (lower_parity, upper_parity) → (lower_parity', upper_parity')
    parity_transitions = Counter()
    parity_detail = []
    for h in range(64):
        L, U = h & 7, (h >> 3) & 7
        hh = hu_formula(h)
        L2, U2 = hh & 7, (hh >> 3) & 7

        pL, pU = parity[L], parity[U]
        pL2, pU2 = parity[L2], parity[U2]
        parity_transitions[((pL, pU), (pL2, pU2))] += 1
        parity_detail.append({
            "h": h, "L": L, "U": U, "L'": L2, "U'": U2,
            "parity_in": (pL, pU), "parity_out": (pL2, pU2),
        })

    print("  (pL, pU) → (pL', pU') transition counts:")
    for (pin, pout), count in sorted(parity_transitions.items()):
        preserves = "PRESERVE" if pin == pout else "CHANGE"
        print(f"    {pin} → {pout}: {count:3d} [{preserves}]")

    # Summarize: does 互 respect parity?
    n_preserve = sum(c for (pin, pout), c in parity_transitions.items() if pin == pout)
    n_change = sum(c for (pin, pout), c in parity_transitions.items() if pin != pout)
    print(f"\n  Parity preserving: {n_preserve}/64")
    print(f"  Parity changing:   {n_change}/64")

    preserves_parity = (n_change == 0)
    print(f"  互 preserves bipartite parity: {preserves_parity}")

    results["parity_transitions"] = {str(k): v for k, v in parity_transitions.items()}
    results["preserves_parity"] = preserves_parity
    results["n_preserve"] = n_preserve
    results["n_change"] = n_change

    # ── 1d: Does 互 descend to the GMS quotient? ─────────────────
    print("\n── 1d. GMS Quotient Map ──")

    if preserves_parity:
        print("  互 preserves parity ⟹ it DOES descend to the GMS quotient.")
        print("  Computing the quotient map...")

        # The GMS quotient identifies each trigram with its parity class.
        # Class 0: {2, 1, 4, 7} (Water, Wood, Earth, Metal)
        # Class 1: {0, 3, 6, 5} (Earth, Metal, Wood, Fire)
        # Actually the GMS is on 2 vertices {0, 1} where:
        #   Vertex 0 = class 0, Vertex 1 = class 1

        # The quotient of 互 on (pL, pU) ∈ {0,1}² is a map {0,1}² → {0,1}²
        # which is a 2-bit-to-2-bit map.
        quotient_map = {}
        for (pin, pout), count in parity_transitions.items():
            if pin not in quotient_map:
                quotient_map[pin] = pout
            else:
                if quotient_map[pin] != pout:
                    print(f"  WARNING: non-deterministic quotient at {pin}")

        print("  Quotient map (pL, pU) → (pL', pU'):")
        for pin in sorted(quotient_map.keys()):
            pout = quotient_map[pin]
            print(f"    {pin} → {pout}")

        results["quotient_map"] = {str(k): v for k, v in quotient_map.items()}
    else:
        print("  互 does NOT preserve parity ⟹ it does not descend cleanly to the GMS quotient.")
        print("  Characterizing the parity mixing...")

        # What fraction of each input parity class goes where?
        for pL_in in [0, 1]:
            for pU_in in [0, 1]:
                pin = (pL_in, pU_in)
                total = sum(c for (p, _), c in parity_transitions.items() if p == pin)
                preserving = parity_transitions.get((pin, pin), 0)
                print(f"    Input {pin}: {preserving}/{total} preserve parity ({100*preserving/total:.0f}%)")

        # Deeper: which output parities do we get?
        for pL_in in [0, 1]:
            for pU_in in [0, 1]:
                pin = (pL_in, pU_in)
                outputs = {pout: c for (p, pout), c in parity_transitions.items() if p == pin}
                print(f"    {pin} → {dict(sorted(outputs.items()))}")

        results["quotient_map"] = None

    return results


# ══════════════════════════════════════════════════════════════════
# PART 2: Formal RG Properties
# ══════════════════════════════════════════════════════════════════

def part2(atlas):
    print("\n" + "═" * 70)
    print("PART 2: FORMAL RG PROPERTIES")
    print("═" * 70)
    results = {}

    hu_map = {h: hu_formula(h) for h in range(64)}

    # ── 2a: Semigroup property ────────────────────────────────────
    print("\n── 2a. Semigroup Structure ──")

    # Compute iterated maps
    def apply_n(h, n):
        for _ in range(n):
            h = hu_map[h]
        return h

    # Find distinct maps in {hu, hu², hu³, ...}
    maps = {}
    for n in range(1, 10):
        m = tuple(apply_n(h, n) for h in range(64))
        maps[n] = m
        # Check if this equals a previously seen map
        is_new = True
        for prev_n, prev_m in list(maps.items()):
            if prev_n < n and prev_m == m:
                is_new = False
                print(f"  hu^{n} = hu^{prev_n}")
                break
        if is_new and n <= 5:
            image_size = len(set(m))
            print(f"  hu^{n}: image size = {image_size}")

    distinct_maps = {}
    for n, m in maps.items():
        if m not in distinct_maps.values():
            distinct_maps[n] = m
    print(f"\n  Distinct maps in {{hu^n : n ≥ 1}}: {len(distinct_maps)}")
    print(f"  Stabilizes at: hu^{max(distinct_maps.keys())} (hu^n = hu^{max(distinct_maps.keys())} for n ≥ {max(distinct_maps.keys())})")

    # Verify semigroup: hu^a ∘ hu^b should be in the set
    print("\n  Semigroup composition table (showing hu^(a+b)):")
    print(f"    {'':>5} | " + " ".join(f"hu^{b}" for b in range(1, 5)))
    for a in range(1, 5):
        row = []
        for b in range(1, 5):
            composed = tuple(apply_n(h, a + b) for h in range(64))
            # Find which power this equals
            for n, m in maps.items():
                if composed == m:
                    row.append(f"hu^{n}")
                    break
            else:
                row.append("???")
        print(f"    hu^{a} | " + "  ".join(f"{r:>4}" for r in row))

    # Key test: hu² ∘ hu² = hu⁴ = hu² (if stabilized at 2)
    hu2_composed = tuple(apply_n(apply_n(h, 2), 2) for h in range(64))
    hu2_idem = hu2_composed == maps[2]
    print(f"\n  hu² ∘ hu² = hu²: {hu2_idem}")
    print(f"  hu² is idempotent: {hu2_idem}")

    results["2a"] = {
        "distinct_maps": len(distinct_maps),
        "stabilizes_at": max(distinct_maps.keys()),
        "hu2_idempotent": hu2_idem,
    }

    # ── 2b: Entropy monotonicity ──────────────────────────────────
    print("\n── 2b. Entropy Monotonicity ──")

    def shannon_entropy(counts):
        """Shannon entropy from count dict."""
        total = sum(counts.values())
        if total == 0:
            return 0.0
        ent = 0.0
        for c in counts.values():
            if c > 0:
                p = c / total
                ent -= p * np.log2(p)
        return ent

    # Start with uniform distribution on 64 states
    print("  Push-forward of uniform distribution under iterated 互:")
    print(f"  {'n':>3} | {'Support':>8} | {'H (bits)':>10} | {'H_type (bits)':>14}")

    def vtype(h):
        rel = atlas[str(h)]["surface_relation"]
        return {"比和": "比和", "体生用": "生", "生体": "生", "体克用": "克", "克体": "克"}[rel]

    entropy_sequence = []
    type_entropy_sequence = []

    for n in range(0, 6):
        # Push forward: count how many inputs land on each output after n steps
        output_counts = Counter()
        type_counts = Counter()
        for h in range(64):
            out = apply_n(h, n)
            output_counts[out] += 1
            type_counts[vtype(out)] += 1

        H = shannon_entropy(output_counts)
        H_type = shannon_entropy(type_counts)
        support = len(output_counts)
        entropy_sequence.append(H)
        type_entropy_sequence.append(H_type)

        print(f"  {n:>3} | {support:>8} | {H:>10.4f} | {H_type:>14.4f}")

    # Monotonicity check
    h_monotone = all(entropy_sequence[i] >= entropy_sequence[i+1]
                     for i in range(len(entropy_sequence)-1))
    ht_monotone = all(type_entropy_sequence[i] >= type_entropy_sequence[i+1]
                      for i in range(len(type_entropy_sequence)-1))
    print(f"\n  State entropy monotonically decreasing: {h_monotone}")
    print(f"  Type entropy monotonically decreasing: {ht_monotone}")

    # Final type distribution
    final_types = Counter(vtype(apply_n(h, 5)) for h in range(64))
    print(f"  Final type distribution (n=5): {dict(sorted(final_types.items()))}")

    results["2b"] = {
        "entropy_sequence": entropy_sequence,
        "type_entropy_sequence": type_entropy_sequence,
        "h_monotone": h_monotone,
        "ht_monotone": ht_monotone,
    }

    # ── 2c: What is preserved? ────────────────────────────────────
    print("\n── 2c. Conserved Quantities Under 互 ──")

    # Test various functions f(h): does Σ f(h) change under hu pushforward?
    # Here the pushforward maps the multiset {h} to {hu(h)}.
    # We test: does Σ_{h∈S} f(h) = Σ_{h∈S} f(hu(h)) for S = all 64?

    tests = {
        "popcount": lambda h: popcount(h),
        "weight_0122_10": lambda h: sum(w * b for w, b in zip([0, 1, 2, 2, 1, 0], bits(h))),
        "hamming_to_0": lambda h: hamming(h, 0),
        "hamming_to_63": lambda h: hamming(h, 63),
        "bit2": lambda h: (h >> 2) & 1,
        "bit3": lambda h: (h >> 3) & 1,
        "hinge_pair": lambda h: ((h >> 2) & 1) + ((h >> 3) & 1),
        "complement_indicator": lambda h: 1 if h ^ 63 == h else 0,  # trivially 0
        "xor_complement": lambda h: h ^ (63 - h),
    }

    print(f"  {'Function':>25} | {'Σf(h)':>8} | {'Σf(hu(h))':>10} | {'Preserved?':>10}")
    print(f"  {'-'*25}-+-{'-'*8}-+-{'-'*10}-+-{'-'*10}")

    conserved = {}
    for name, f in tests.items():
        sum_orig = sum(f(h) for h in range(64))
        sum_hu = sum(f(hu_map[h]) for h in range(64))
        preserved = sum_orig == sum_hu
        conserved[name] = {"original": sum_orig, "hu": sum_hu, "preserved": preserved}
        print(f"  {name:>25} | {sum_orig:>8} | {sum_hu:>10} | {'✓' if preserved else '✗':>10}")

    # Mean Hamming distance preservation (R261 finding)
    print("\n  Mean Hamming distance (pairwise):")
    sum_d_orig = sum(hamming(x, y) for x in range(64) for y in range(x+1, 64))
    sum_d_hu = sum(hamming(hu_map[x], hu_map[y]) for x in range(64) for y in range(x+1, 64))
    mean_d_orig = sum_d_orig / (64 * 63 / 2)
    mean_d_hu = sum_d_hu / (64 * 63 / 2)
    print(f"    Original: {mean_d_orig:.6f}")
    print(f"    After hu: {mean_d_hu:.6f}")
    print(f"    Preserved: {abs(mean_d_orig - mean_d_hu) < 1e-10}")
    conserved["mean_hamming"] = {"original": mean_d_orig, "hu": mean_d_hu,
                                  "preserved": abs(mean_d_orig - mean_d_hu) < 1e-10}

    # Walsh coefficient test
    print("\n  Walsh coefficients:")
    # Walsh function W_k(h) = (-1)^{popcount(h & k)}
    # The Walsh transform of f(h) = Σ_h f(h) W_k(h)
    # For f = indicator of {h}, the Walsh transform is W_k(h).
    # For the uniform measure, Σ_h W_k(h) = 64 if k=0, else 0.
    # Under hu pushforward: Σ_h W_k(hu(h)) ?= Σ_h W_k(h)
    walsh_preserved = []
    for k in range(64):
        orig = sum((-1)**popcount(h & k) for h in range(64))
        after = sum((-1)**popcount(hu_map[h] & k) for h in range(64))
        if orig != after:
            walsh_preserved.append((k, orig, after))
    if not walsh_preserved:
        print("    All 64 Walsh coefficients preserved under hu!")
    else:
        print(f"    {64 - len(walsh_preserved)}/64 Walsh coefficients preserved")
        print(f"    Changed coefficients (first 10):")
        for k, o, a in walsh_preserved[:10]:
            print(f"      W_{k} ({format(k, '06b')}): {o} → {a}")

    conserved["walsh_preserved"] = 64 - len(walsh_preserved)
    conserved["walsh_changed"] = len(walsh_preserved)

    results["2c"] = conserved

    # ── 2d: Fixed-point structure ─────────────────────────────────
    print("\n── 2d. Fixed-Point Structure ──")

    fixed_points = [h for h in range(64) if hu_map[h] == h]
    print(f"  Fixed points of hu: {fixed_points} = {[format(h, '06b') for h in fixed_points]}")

    fixed_hu2 = [h for h in range(64) if apply_n(h, 2) == h]
    print(f"  Fixed points of hu²: {fixed_hu2} = {[format(h, '06b') for h in fixed_hu2]}")

    period2 = [h for h in fixed_hu2 if h not in fixed_points]
    print(f"  Period-2 orbits (fixed by hu² but not hu): {period2}")

    # Linearize hu near each fixed point
    print("\n  Linearization near fixed points:")
    ATTRACTORS = [0, 21, 42, 63]

    for fp in ATTRACTORS:
        print(f"\n  Fixed point {fp} ({format(fp, '06b')}):")
        # Compute Jacobian: dhu_i/db_j
        # hu is a Boolean function, so the "Jacobian" is the matrix of partial derivatives
        # over GF(2), but we can also look at real perturbations.
        # More useful: for each of the 6 single-bit perturbations, where does it go?
        perturbations = {}
        for bit in range(6):
            perturbed = fp ^ (1 << bit)
            output = hu_map[perturbed]
            delta_out = output ^ fp  # which bits changed in output
            perturbations[bit] = {
                "input": perturbed,
                "output": output,
                "delta_out_bits": [b for b in range(6) if (delta_out >> b) & 1],
                "delta_out": delta_out,
                "hamming_growth": hamming(output, fp),
            }
            print(f"    Flip bit {bit}: {format(perturbed, '06b')} → {format(output, '06b')}, "
                  f"Δout = {format(delta_out, '06b')} (Hamming = {hamming(output, fp)})")

        # After iteration: does the perturbation grow or shrink?
        print(f"    After hu²:")
        for bit in range(6):
            perturbed = fp ^ (1 << bit)
            out2 = apply_n(perturbed, 2)
            fp2 = apply_n(fp, 2)  # should be fp since it's a fixed point of hu²
            d2 = hamming(out2, fp2)
            direction = "RELEVANT (grows)" if d2 > 0 else "IRRELEVANT (dies)"
            print(f"      Flip bit {bit}: d(hu²(x), hu²(fp)) = {d2} — {direction}")

        results[f"linearization_{fp}"] = perturbations

    # Classify bits as relevant/irrelevant at the identity fixed point (0)
    print("\n  Summary: Relevant vs Irrelevant perturbations at fp=0:")
    for fp in ATTRACTORS:
        relevant = []
        irrelevant = []
        for bit in range(6):
            perturbed = fp ^ (1 << bit)
            out2 = apply_n(perturbed, 2)
            fp2 = apply_n(fp, 2)
            if hamming(out2, fp2) > 0:
                relevant.append(bit)
            else:
                irrelevant.append(bit)
        print(f"    fp={fp} ({format(fp, '06b')}): relevant bits = {relevant}, irrelevant = {irrelevant}")
        results[f"relevant_bits_{fp}"] = relevant
        results[f"irrelevant_bits_{fp}"] = irrelevant

    return results


# ══════════════════════════════════════════════════════════════════
# PART 3: Bit Weights as Decimation Kernel
# ══════════════════════════════════════════════════════════════════

def part3():
    print("\n" + "═" * 70)
    print("PART 3: BIT WEIGHTS AS DECIMATION KERNEL")
    print("═" * 70)
    results = {}

    # ── 3a: Compare to known decimation schemes ───────────────────
    print("\n── 3a. Kernel Comparison ──")

    kernel = np.array([0, 1, 2, 2, 1, 0])
    print(f"  互 kernel weights: {kernel.tolist()}")
    print(f"  Sum: {kernel.sum()}")

    # Normalized
    k_norm = kernel / kernel.sum()
    print(f"  Normalized: {[round(x, 4) for x in k_norm]}")

    # Compare to standard kernels
    # Simple decimation: keep every other bit → [0,1,0,1,0,1] or [1,0,1,0,1,0]
    decimation = np.array([0, 1, 0, 1, 0, 0])
    print(f"\n  Simple decimation (bits 1,3): {decimation.tolist()}")
    print(f"  互 differs: 互 uses bits 1,2,3,4 with weights, not just alternating")

    # Majority rule on blocks of 3: [bits 0-2] → majority, [bits 3-5] → majority
    print(f"  Majority rule on 3-blocks: applies to pairs of 3-bit groups")
    print(f"  互 differs: overlapping windows, not disjoint blocks")

    # The key structure: 互 uses a sliding window of width 4 (bits 1-4)
    # with an internal overlap (bits 2,3 appear twice in the output)
    print(f"\n  互 as sliding window:")
    print(f"    Input bits:  [b0, b1, b2, b3, b4, b5]")
    print(f"    Output bits: [b1, b2, b3, b2, b3, b4]")
    print(f"    Window: bits 1-4 (width 4), centered on hinge (bits 2-3)")
    print(f"    Duplication: bits 2,3 appear in BOTH lower and upper trigram of output")
    print(f"    Discarded: bits 0, 5 (outer shell)")

    results["3a"] = {
        "kernel": kernel.tolist(),
        "window": "bits 1-4",
        "duplicated": "bits 2-3",
        "discarded": "bits 0, 5",
    }

    # ── 3b: Kernel as convolution ─────────────────────────────────
    print("\n── 3b. Kernel as Convolution ──")

    # Is [0,1,2,2,1,0] the convolution of simpler kernels?
    # Convolution of [0,1,1] with [1,1,0] = [0,1,2,1,0] (length 5, wrong)
    # Convolution of [1,1] with [0,1,1,0] = [0,1,2,1,0] (length 5, wrong)
    # Try: [0,1,1] * [1,1] = [0,1,2,1] (length 4)

    # Actually this kernel is NOT a convolution of the weights.
    # It's a BIT DUPLICATION map, not a linear filter.
    # The "weights" [0,1,2,2,1,0] count how many times each input bit appears in output.
    # Bit 0: appears 0 times in output
    # Bit 1: appears 1 time (output bit 0)
    # Bit 2: appears 2 times (output bits 1 and 3)
    # Bit 3: appears 2 times (output bits 2 and 4)
    # Bit 4: appears 1 time (output bit 5)
    # Bit 5: appears 0 times

    print("  The 'kernel' [0,1,2,2,1,0] is not a convolution filter.")
    print("  It's a multiplicity count: how many times each input bit appears in output.")
    print("  The actual map is a BIT ROUTING (copying, not arithmetic):")
    print("    output[0] = input[1]")
    print("    output[1] = input[2]")
    print("    output[2] = input[3]")
    print("    output[3] = input[2]  ← duplicate!")
    print("    output[4] = input[3]  ← duplicate!")
    print("    output[5] = input[4]")
    print()
    print("  Matrix form (6×6 routing matrix R, where output = R × input over GF(2)):")
    R = np.array([
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
    ])
    print(f"    R = {R.tolist()}")

    # Verify
    for h in range(64):
        b_in = np.array(bits(h))
        b_out = R @ b_in  # This is integer arithmetic, same as GF(2) since entries are 0/1
        h_out = sum(int(b_out[i]) * (1 << i) for i in range(6))
        assert h_out == hu_formula(h), f"Routing mismatch at {h}"
    print("    ✓ Verified: R × input = hu(input) for all 64 hexagrams")

    # Column sums = kernel weights
    print(f"    Column sums of R: {R.sum(axis=0).tolist()} = kernel weights ✓")

    # R is rank-deficient: rank = 4 (only 4 independent bits in output)
    rank_R = np.linalg.matrix_rank(R.astype(float))
    print(f"    Rank of R: {rank_R} (6→4 dimension reduction)")

    # What is R²?
    R2 = R @ R
    print(f"\n  R² (iterate the routing):")
    print(f"    R² = {R2.tolist()}")
    print(f"    Column sums of R²: {R2.sum(axis=0).tolist()}")
    print(f"    Rank of R²: {np.linalg.matrix_rank(R2.astype(float))}")

    # R³
    R3 = R2 @ R
    print(f"\n  R³:")
    print(f"    Column sums of R³: {R3.sum(axis=0).tolist()}")
    print(f"    Rank of R³: {np.linalg.matrix_rank(R3.astype(float))}")

    # What's the stable R^∞?
    Rn = R.copy()
    for _ in range(10):
        Rn = Rn @ R
    print(f"\n  R^∞ (stable):")
    print(f"    R^∞ = {Rn.tolist()}")
    print(f"    Rank of R^∞: {np.linalg.matrix_rank(Rn.astype(float))}")

    results["3b"] = {
        "routing_matrix": R.tolist(),
        "rank": int(rank_R),
        "R2_rank": int(np.linalg.matrix_rank(R2.astype(float))),
        "R_inf_rank": int(np.linalg.matrix_rank(Rn.astype(float))),
    }

    # ── 3c: Layer structure ───────────────────────────────────────
    print("\n── 3c. Concentric Layer Structure ──")

    # Three concentric bit-pairs:
    # Outer: bits 0,5 — survive 0 iterations (discarded immediately)
    # Middle: bits 1,4 — survive 1 iteration (become outer after one step)
    # Hinge: bits 2,3 — survive 2+ iterations (become middle, then outer)

    print("  Layer structure under iterated 互:")
    print("    Layer   | Bits | Survives | Role after hu | Role after hu²")
    print("    --------|------|----------|---------------|---------------")
    print("    Outer   | 0, 5 | 0 steps  | gone          | gone")
    print("    Middle  | 1, 4 | 1 step   | outer (0', 5')| gone")
    print("    Hinge   | 2, 3 | 2 steps  | middle (1',4')| outer → gone at hu³")

    # Verify by tracking which bits of input survive in output
    print("\n  Bit survival matrix (which input bit contributes to output at step n):")
    Rn = np.eye(6, dtype=int)
    for n in range(4):
        Rn = Rn if n == 0 else Rn @ R
        surviving_bits = [i for i in range(6) if Rn[:, i].sum() > 0]
        print(f"    Step {n}: surviving input bits = {surviving_bits}, "
              f"contributions = {Rn.sum(axis=0).tolist()}")

    # Transfer matrix for each layer
    # Layer = pair of bits. We can track the information content of each layer.
    # Outer layer (bits 0,5): 4 possible states (00, 01, 10, 11)
    # But under hu, this layer is discarded. So no transfer matrix — it's a projection.
    # Instead, characterize what happens to the 2-bit state of each layer.

    print("\n  Layer evolution under hu:")
    for h in range(64):
        b = bits(h)
        bh = bits(hu_formula(h))
        outer_in = (b[0], b[5])
        middle_in = (b[1], b[4])
        hinge_in = (b[2], b[3])
        outer_out = (bh[0], bh[5])
        middle_out = (bh[1], bh[4])
        hinge_out = (bh[2], bh[3])
        # Check: outer_out should be middle_in, middle_out should be hinge_in
        if h < 4:  # just show a few examples
            print(f"    h={h:2d}: outer {outer_in}→{outer_out}, "
                  f"middle {middle_in}→{middle_out}, hinge {hinge_in}→{hinge_out}")

    # Systematic check
    outer_from_middle = 0
    middle_from_hinge = 0
    hinge_self = 0
    for h in range(64):
        b = bits(h)
        bh = bits(hu_formula(h))
        # outer_out = (bh[0], bh[5]) = (b[1], b[4]) = middle_in
        if (bh[0], bh[5]) == (b[1], b[4]):
            outer_from_middle += 1
        # middle_out = (bh[1], bh[4]) = (b[2], b[3]) = hinge_in
        if (bh[1], bh[4]) == (b[2], b[3]):
            middle_from_hinge += 1
        # hinge_out = (bh[2], bh[3]) = (b[3], b[2]) = swapped hinge_in!
        if (bh[2], bh[3]) == (b[3], b[2]):
            hinge_self += 1

    print(f"\n  Layer shift verification (all 64 hexagrams):")
    print(f"    outer_out = middle_in:       {outer_from_middle}/64")
    print(f"    middle_out = hinge_in:       {middle_from_hinge}/64")
    print(f"    hinge_out = swap(hinge_in):  {hinge_self}/64")

    # Check the actual hinge transformation
    print(f"\n  Hinge bit transformation:")
    print(f"    Input hinge:  (b2, b3)")
    print(f"    Output hinge: (bh[2], bh[3]) = (b3, b2) — SWAP!")
    # Verify
    hinge_swap_count = 0
    hinge_identity_count = 0
    for h in range(64):
        b = bits(h)
        bh = bits(hu_formula(h))
        if (bh[2], bh[3]) == (b[3], b[2]):
            hinge_swap_count += 1
        if (bh[2], bh[3]) == (b[2], b[3]):
            hinge_identity_count += 1
    print(f"    Hinge is swapped: {hinge_swap_count}/64")
    print(f"    Hinge is identity: {hinge_identity_count}/64")

    # So the full layer dynamics:
    # Each layer shifts inward by one level, with the hinge SWAPPING
    print(f"\n  LAYER DYNAMICS SUMMARY:")
    print(f"    outer → discarded")
    print(f"    middle → outer")
    print(f"    hinge → middle (with swap: (b2,b3) → (b3,b2))")
    print(f"    This is a 3-level conveyor belt with a swap at the core.")
    print(f"    After hu²: hinge becomes outer, and the swap is applied TWICE (= identity).")
    print(f"    hu² on hinge bits: (b2,b3) → swap → swap = (b2,b3) but now at outer position.")
    print(f"    ⟹ After 2 steps, all information about the original outer and middle is lost.")
    print(f"    ⟹ Only the hinge bits (2,3) determine the eventual attractor. (= R261 finding)")

    results["3c"] = {
        "outer_from_middle": outer_from_middle,
        "middle_from_hinge": middle_from_hinge,
        "hinge_swap": hinge_swap_count,
        "hinge_identity": hinge_identity_count,
        "dynamics": "3-level conveyor belt with swap at core",
    }

    return results


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════

def main():
    atlas = load_atlas()
    trigram_elements = get_trigram_elements(atlas)

    print("=" * 70)
    print("PROBE B: 互 AS RENORMALIZATION (WITH A→B BRIDGE)")
    print("=" * 70)

    r1 = part1(atlas, trigram_elements)
    r2 = part2(atlas)
    r3 = part3()

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "═" * 70)
    print("SUMMARY")
    print("═" * 70)

    parity_status = "YES" if r1["preserves_parity"] else "NO"
    print(f"""
  1. PARITY DESCENT: Does 互 respect P₄ bipartite parity?
     → {parity_status} ({r1['n_preserve']}/64 preserve, {r1['n_change']}/64 change)
""")

    if r1["preserves_parity"]:
        print("     互 descends to a well-defined map on the GMS quotient {0,1}².")
        if r1.get("quotient_map"):
            print("     Quotient map:")
            for k, v in r1["quotient_map"].items():
                print(f"       {k} → {v}")
    else:
        print("     互 does NOT cleanly descend to the GMS quotient.")
        print("     It couples the GMS and anti-GMS sectors.")

    print(f"""
  2. FORMAL RG PROPERTIES:
     a) Semigroup: hu² is idempotent (hu²∘hu² = hu²). {r2['2a']['distinct_maps']} distinct maps.
     b) Entropy: State entropy monotonically decreasing: {r2['2b']['h_monotone']}
        Sequence: {[round(x, 2) for x in r2['2b']['entropy_sequence']]}
     c) Conserved: popcount, mean Hamming preserved? See details above.
     d) Fixed points: 4 attractors {{0,21,42,63}}, bits 2,3 are the relevant directions.

  3. BIT-WEIGHT KERNEL:
     The 互 map is a BIT ROUTING (not arithmetic): output[i] = input[σ(i)]
     with σ = [1,2,3,2,3,4] (hinge bits 2,3 duplicated).
     Routing matrix R has rank 4 (6→4 effective dimension reduction).
     Layer dynamics: 3-level conveyor belt, outer→discarded, middle→outer,
     hinge→middle (with swap). After 2 steps only hinge bits survive.
""")

    # Save results
    all_results = {
        "part1_parity": r1,
        "part2_rg_properties": r2,
        "part3_kernel": r3,
    }

    out_path = HERE / "probeB_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"Results saved to {out_path}")


if __name__ == "__main__":
    main()
