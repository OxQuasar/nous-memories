"""
Probe 4: Dark Sector Characterization

Characterize the hex-level eigenvalues that have no trigram-level ancestor.
For each 五行 type (比和, 生, 克), the OR-symmetrized 64×64 matrix has 64
eigenvalues. The "coherent" ones are tensor sums λᵢ + λⱼ of trigram
eigenvalues. The rest — the "dark sector" — are what this probe investigates.
"""

import json
import numpy as np
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
ATLAS_DIR = HERE.parent / "atlas"
DYNAMICS_DIR = HERE.parent / "dynamics"

RELATION_GROUPS = {
    "比和": "比和", "体生用": "生", "生体": "生", "体克用": "克", "克体": "克",
}
GROUP_NAMES = ["比和", "生", "克"]
PHI = (1 + 5**0.5) / 2
EPS = 1e-5

# ── Loading & Matrix Construction ─────────────────────────────────

def load_atlas():
    with open(ATLAS_DIR / "atlas.json") as f:
        return json.load(f)

def load_transitions():
    with open(ATLAS_DIR / "transitions.json") as f:
        return json.load(f)["bian_fan"]

def load_p1_results():
    with open(DYNAMICS_DIR / "p1_results.json") as f:
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

def wuxing_group(e1, e2):
    if e1 == e2: return "比和"
    if SHENG[e1] == e2 or SHENG[e2] == e1: return "生"
    return "克"

def build_directed_matrices(transitions):
    mats = {g: np.zeros((64, 64), dtype=int) for g in GROUP_NAMES}
    for t in transitions:
        g = RELATION_GROUPS[t["tiyong_relation"]]
        mats[g][t["source"], t["destination"]] = 1
    return mats

def build_or_symmetrized(dir_mats):
    return {g: np.maximum(A, A.T) for g, A in dir_mats.items()}

def build_trigram_matrices(trigram_elements):
    mats = {g: np.zeros((8, 8), dtype=int) for g in GROUP_NAMES}
    for a in range(8):
        for bit in range(3):
            b = a ^ (1 << bit)
            if b <= a:
                continue
            g = wuxing_group(trigram_elements[a], trigram_elements[b])
            mats[g][a, b] = 1
            mats[g][b, a] = 1
    return mats

# ── Eigenvalue Identification ─────────────────────────────────────

KNOWN_CONSTANTS = [
    (0, "0"), (1, "1"), (-1, "-1"), (2, "2"), (-2, "-2"),
    (PHI, "φ"), (-PHI, "-φ"), (1/PHI, "1/φ"), (-1/PHI, "-1/φ"),
    (2*PHI, "2φ"), (-2*PHI, "-2φ"), (2/PHI, "2/φ"), (-2/PHI, "-2/φ"),
    (5**0.5, "√5"), (-5**0.5, "-√5"),
    (2**0.5, "√2"), (-2**0.5, "-√2"), (2*2**0.5, "2√2"), (-2*2**0.5, "-2√2"),
    (3, "3"), (-3, "-3"),
]

def identify_value(v):
    for cand, label in KNOWN_CONSTANTS:
        if abs(v - cand) < EPS:
            return label
    return f"{v:.8f}"

# ══════════════════════════════════════════════════════════════════
# STEP 1: Coherent/Dark Sector Separation
# ══════════════════════════════════════════════════════════════════

def compute_coherent_eigenvalues(trig_eigvals):
    """Compute all tensor-sum candidates λᵢ + λⱒ from trigram eigenvalues (with multiplicity)."""
    vals = []
    for v, m in trig_eigvals:
        vals.extend([v] * m)
    sums = sorted([a + b for a in vals for b in vals])
    return sums

def classify_eigenvalues(hex_vals, coherent_candidates):
    """Match each hex eigenvalue to a coherent candidate. Return (coherent_idx, dark_idx)."""
    remaining = list(coherent_candidates)
    coherent_idx = []
    dark_idx = []

    # Sort hex vals and try greedy matching
    order = np.argsort(hex_vals)
    remaining.sort()

    matched = [False] * len(hex_vals)
    used = [False] * len(remaining)

    # Two-pointer matching on sorted arrays
    i, j = 0, 0
    sorted_hex = hex_vals[order]
    while i < len(sorted_hex) and j < len(remaining):
        if abs(sorted_hex[i] - remaining[j]) < EPS:
            matched[order[i]] = True
            used[j] = True
            i += 1
            j += 1
        elif sorted_hex[i] < remaining[j]:
            i += 1
        else:
            j += 1

    for k in range(len(hex_vals)):
        if matched[k]:
            coherent_idx.append(k)
        else:
            dark_idx.append(k)

    return coherent_idx, dark_idx

def step1(or_mats, trig_mats):
    print("=" * 70)
    print("STEP 1: COHERENT / DARK SECTOR SEPARATION")
    print("=" * 70)

    results = {}
    hex_eigsystems = {}

    for g in GROUP_NAMES:
        print(f"\n── {g} ──")
        # Full eigensystem of OR-symmetrized 64×64
        eigvals, eigvecs = np.linalg.eigh(or_mats[g].astype(float))
        hex_eigsystems[g] = (eigvals, eigvecs)

        # Trigram eigensystem
        trig_vals = np.linalg.eigh(trig_mats[g].astype(float))[0]
        trig_rounded = np.round(trig_vals, 8)
        trig_unique, trig_counts = np.unique(trig_rounded, return_counts=True)
        trig_eig_list = [(float(v), int(c)) for v, c in zip(trig_unique, trig_counts)]

        print(f"  Trigram eigenvalues: {[(identify_value(v), m) for v, m in trig_eig_list]}")

        # Coherent candidates
        coherent_cands = compute_coherent_eigenvalues(trig_eig_list)
        unique_cands = sorted(set(round(c, 8) for c in coherent_cands))
        print(f"  Coherent candidates (distinct values): {[identify_value(v) for v in unique_cands]}")

        # Classify
        coherent_idx, dark_idx = classify_eigenvalues(eigvals, coherent_cands)
        n_coherent = len(coherent_idx)
        n_dark = len(dark_idx)

        # Spectral weight
        weight_coherent = sum(eigvals[i]**2 for i in coherent_idx)
        weight_dark = sum(eigvals[i]**2 for i in dark_idx)
        total_weight = weight_coherent + weight_dark
        frac_coherent = weight_coherent / total_weight if total_weight > 0 else 0
        frac_dark = weight_dark / total_weight if total_weight > 0 else 0

        print(f"  Coherent: {n_coherent} eigenvalues, spectral weight = {weight_coherent:.4f} ({frac_coherent:.1%})")
        print(f"  Dark:     {n_dark} eigenvalues, spectral weight = {weight_dark:.4f} ({frac_dark:.1%})")

        # List coherent eigenvalues
        coh_vals = sorted(eigvals[coherent_idx])
        dark_vals = sorted(eigvals[dark_idx])
        print(f"  Coherent eigenvalues: {[identify_value(v) for v in coh_vals]}")
        print(f"  Dark eigenvalues ({n_dark}):")
        for v in dark_vals:
            print(f"    {v:12.8f}  {identify_value(v)}")

        results[g] = {
            "n_coherent": n_coherent,
            "n_dark": n_dark,
            "weight_coherent": float(weight_coherent),
            "weight_dark": float(weight_dark),
            "frac_coherent": float(frac_coherent),
            "frac_dark": float(frac_dark),
            "coherent_eigenvalues": [float(v) for v in coh_vals],
            "dark_eigenvalues": [float(v) for v in dark_vals],
            "coherent_idx": [int(i) for i in coherent_idx],
            "dark_idx": [int(i) for i in dark_idx],
        }

    return results, hex_eigsystems

# ══════════════════════════════════════════════════════════════════
# STEP 2: Walsh Basis Decomposition of Dark Eigenvectors
# ══════════════════════════════════════════════════════════════════

def build_walsh_hadamard():
    """64×64 Walsh-Hadamard matrix. H[i,j] = (-1)^{⟨i,j⟩} / 8."""
    H = np.zeros((64, 64))
    for i in range(64):
        for j in range(64):
            dot = bin(i & j).count('1')
            H[i, j] = (-1)**dot / 8.0
    return H

def walsh_weight(w):
    """Hamming weight of binary vector w (number of 1-bits)."""
    return bin(w).count('1')

def step2(hex_eigsystems, step1_results):
    print("\n" + "=" * 70)
    print("STEP 2: WALSH BASIS DECOMPOSITION OF DARK EIGENVECTORS")
    print("=" * 70)

    H = build_walsh_hadamard()
    results = {}

    for g in GROUP_NAMES:
        print(f"\n── {g} ──")
        eigvals, eigvecs = hex_eigsystems[g]
        dark_idx = step1_results[g]["dark_idx"]

        if not dark_idx:
            print("  No dark sector eigenvalues.")
            results[g] = {"walsh_weight_distribution": {}, "dominant_weights": []}
            continue

        # For each dark eigenvector, project onto Walsh basis
        # Walsh coefficient: c_w = Σ_j H[w,j] * v[j]
        # Energy at Walsh index w: |c_w|²
        # Walsh weight of index w: popcount(w)

        weight_energy = np.zeros(7)  # weights 0..6
        per_eigenvector = []

        for idx in dark_idx:
            v = eigvecs[:, idx]
            # Walsh transform
            c = H @ v  # c[w] = Walsh coefficient at frequency w
            energy = c**2  # real eigenvectors, so no complex conjugate needed

            # Aggregate by Walsh weight
            ev_weight_energy = np.zeros(7)
            for w in range(64):
                wt = walsh_weight(w)
                ev_weight_energy[wt] += energy[w]

            weight_energy += ev_weight_energy
            per_eigenvector.append({
                "eigenvalue": float(eigvals[idx]),
                "walsh_weight_energy": ev_weight_energy.tolist(),
                "dominant_weight": int(np.argmax(ev_weight_energy)),
            })

        # Normalize
        total = weight_energy.sum()
        weight_dist = weight_energy / total if total > 0 else weight_energy

        print(f"  Walsh weight distribution (fraction of dark sector energy):")
        for w in range(7):
            bar = "█" * int(weight_dist[w] * 50)
            print(f"    weight {w}: {weight_dist[w]:.4f} {bar}")

        # Dominant weights
        dominant = [w for w in range(7) if weight_dist[w] > 0.1]
        print(f"  Dominant weights (>10%): {dominant}")

        # Per-eigenvector summary
        print(f"  Per-eigenvector dominant Walsh weight:")
        weight_counts = Counter(ev["dominant_weight"] for ev in per_eigenvector)
        for w in sorted(weight_counts):
            print(f"    weight {w}: {weight_counts[w]} eigenvectors")

        results[g] = {
            "walsh_weight_distribution": {str(w): float(weight_dist[w]) for w in range(7)},
            "weight_energy_raw": weight_energy.tolist(),
            "dominant_weights": dominant,
            "per_eigenvector_dominant": dict(weight_counts),
        }

    return results

# ══════════════════════════════════════════════════════════════════
# STEP 3: Automorphism Orbits / Symmetry Classification
# ══════════════════════════════════════════════════════════════════

def complement(h):
    """Complement involution: flip all bits."""
    return 63 - h

def trigram_swap(h):
    """Swap upper and lower trigrams."""
    return ((h & 7) << 3) | ((h >> 3) & 7)

def step3(hex_eigsystems, step1_results):
    print("\n" + "=" * 70)
    print("STEP 3: SYMMETRY CLASSIFICATION OF DARK SECTOR")
    print("=" * 70)

    # Build permutation matrices for complement and trigram_swap
    P_comp = np.zeros((64, 64))
    P_swap = np.zeros((64, 64))
    for h in range(64):
        P_comp[complement(h), h] = 1
        P_swap[trigram_swap(h), h] = 1

    results = {}

    for g in GROUP_NAMES:
        print(f"\n── {g} ──")
        eigvals, eigvecs = hex_eigsystems[g]
        dark_idx = step1_results[g]["dark_idx"]
        coherent_idx = step1_results[g]["coherent_idx"]

        if not dark_idx:
            print("  No dark sector.")
            results[g] = {}
            continue

        # Complement parity: v is symmetric if P_comp @ v ≈ v, antisymmetric if ≈ -v
        print(f"\n  Complement parity (h ↔ 63-h):")
        comp_sym = []
        comp_anti = []
        comp_mixed = []
        for idx in dark_idx:
            v = eigvecs[:, idx]
            Pv = P_comp @ v
            # Check overlap
            overlap = np.dot(v, Pv)
            if abs(overlap - 1) < EPS:
                comp_sym.append(idx)
            elif abs(overlap + 1) < EPS:
                comp_anti.append(idx)
            else:
                comp_mixed.append((idx, float(overlap)))

        print(f"    Symmetric (+1): {len(comp_sym)}")
        print(f"    Antisymmetric (-1): {len(comp_anti)}")
        print(f"    Mixed: {len(comp_mixed)}")
        if comp_mixed:
            print(f"    Mixed overlaps: {[(identify_value(eigvals[i]), f'{o:.4f}') for i, o in comp_mixed[:10]]}")

        # Same for coherent sector
        coh_sym = sum(1 for i in coherent_idx if abs(np.dot(eigvecs[:, i], P_comp @ eigvecs[:, i]) - 1) < EPS)
        coh_anti = sum(1 for i in coherent_idx if abs(np.dot(eigvecs[:, i], P_comp @ eigvecs[:, i]) + 1) < EPS)
        print(f"    (Coherent: {coh_sym} sym, {coh_anti} anti)")

        # Trigram swap parity
        print(f"\n  Trigram swap parity (upper ↔ lower):")
        swap_sym = []
        swap_anti = []
        swap_mixed = []
        for idx in dark_idx:
            v = eigvecs[:, idx]
            Sv = P_swap @ v
            overlap = np.dot(v, Sv)
            if abs(overlap - 1) < EPS:
                swap_sym.append(idx)
            elif abs(overlap + 1) < EPS:
                swap_anti.append(idx)
            else:
                swap_mixed.append((idx, float(overlap)))

        print(f"    Symmetric (+1): {len(swap_sym)}")
        print(f"    Antisymmetric (-1): {len(swap_anti)}")
        print(f"    Mixed: {len(swap_mixed)}")
        if swap_mixed:
            print(f"    Mixed overlaps: {[(identify_value(eigvals[i]), f'{o:.4f}') for i, o in swap_mixed[:10]]}")

        # Combined (complement, swap) parity for dark eigenvectors
        print(f"\n  Combined parity classes (complement, swap):")
        parity_classes = Counter()
        for idx in dark_idx:
            v = eigvecs[:, idx]
            c_overlap = np.dot(v, P_comp @ v)
            s_overlap = np.dot(v, P_swap @ v)
            c_sign = "+1" if abs(c_overlap - 1) < EPS else ("-1" if abs(c_overlap + 1) < EPS else "mixed")
            s_sign = "+1" if abs(s_overlap - 1) < EPS else ("-1" if abs(s_overlap + 1) < EPS else "mixed")
            parity_classes[(c_sign, s_sign)] += 1

        for (c, s), count in sorted(parity_classes.items()):
            print(f"    (comp={c}, swap={s}): {count}")

        # Do dark eigenvalues come in ± pairs?
        print(f"\n  ± pairing of dark eigenvalues:")
        dark_vals = sorted(eigvals[dark_idx])
        paired = 0
        unpaired_vals = []
        used = set()
        for i, v in enumerate(dark_vals):
            if i in used:
                continue
            # Look for -v
            found = False
            for j in range(i + 1, len(dark_vals)):
                if j in used:
                    continue
                if abs(dark_vals[j] + v) < EPS:
                    paired += 2
                    used.add(i)
                    used.add(j)
                    found = True
                    break
            if not found:
                unpaired_vals.append(v)
                used.add(i)

        print(f"    Paired: {paired}, Unpaired: {len(unpaired_vals)}")
        if unpaired_vals:
            print(f"    Unpaired values: {[identify_value(v) for v in unpaired_vals]}")

        results[g] = {
            "complement": {"symmetric": len(comp_sym), "antisymmetric": len(comp_anti), "mixed": len(comp_mixed)},
            "trigram_swap": {"symmetric": len(swap_sym), "antisymmetric": len(swap_anti), "mixed": len(swap_mixed)},
            "parity_classes": {f"({c},{s})": count for (c, s), count in parity_classes.items()},
            "pm_pairs": {"paired": paired, "unpaired": len(unpaired_vals),
                         "unpaired_values": [float(v) for v in unpaired_vals]},
        }

    return results

# ══════════════════════════════════════════════════════════════════
# STEP 4: Algebraic Structure of Dark Eigenvalues
# ══════════════════════════════════════════════════════════════════

def step4(hex_eigsystems, step1_results):
    print("\n" + "=" * 70)
    print("STEP 4: ALGEBRAIC STRUCTURE OF DARK EIGENVALUES")
    print("=" * 70)

    results = {}

    for g in GROUP_NAMES:
        print(f"\n── {g} ──")
        eigvals = hex_eigsystems[g][0]
        dark_idx = step1_results[g]["dark_idx"]

        if not dark_idx:
            print("  No dark sector.")
            results[g] = {}
            continue

        dark_vals = sorted(eigvals[dark_idx])

        # Check membership in Q(φ) = Q(√5)
        # A value v is in Q(√5) if v = a + b√5 for rational a,b
        # Check: for each v, can we find integers p,q,r,s such that v ≈ p/q + (r/s)√5?
        sqrt5 = 5**0.5
        sqrt2 = 2**0.5

        print(f"  Testing algebraic form of dark eigenvalues:")
        in_q_phi = 0
        in_q_sqrt2 = 0
        algebraic_forms = []

        for v in dark_vals:
            # Try v = a + b√5 with a,b rational (denominators up to 20)
            found_phi = False
            found_sqrt2 = False
            best_form = None

            for denom in range(1, 21):
                # v = p/denom + (q/denom)√5
                for q in range(-20, 21):
                    remainder = v - q * sqrt5 / denom
                    p = round(remainder * denom)
                    if abs(p / denom + q * sqrt5 / denom - v) < 1e-8:
                        found_phi = True
                        if best_form is None or denom < best_form[2]:
                            best_form = (p, q, denom, "√5")
                        break
                if found_phi:
                    break

            if not found_phi:
                # Try v = a + b√2
                for denom in range(1, 21):
                    for q in range(-20, 21):
                        remainder = v - q * sqrt2 / denom
                        p = round(remainder * denom)
                        if abs(p / denom + q * sqrt2 / denom - v) < 1e-8:
                            found_sqrt2 = True
                            best_form = (p, q, denom, "√2")
                            break
                    if found_sqrt2:
                        break

            if found_phi:
                in_q_phi += 1
            elif found_sqrt2:
                in_q_sqrt2 += 1

            if best_form:
                p, q, d, radical = best_form
                if d == 1:
                    form_str = f"{p} + {q}{radical}" if q >= 0 else f"{p} - {-q}{radical}"
                else:
                    form_str = f"{p}/{d} + {q}/{d}·{radical}"
                algebraic_forms.append((v, form_str))
                print(f"    {v:12.8f} = {form_str}")
            else:
                algebraic_forms.append((v, "unknown"))
                print(f"    {v:12.8f} = ???")

        print(f"\n  In Q(√5): {in_q_phi}/{len(dark_vals)}")
        print(f"  In Q(√2): {in_q_sqrt2}/{len(dark_vals)}")
        print(f"  Unidentified: {len(dark_vals) - in_q_phi - in_q_sqrt2}/{len(dark_vals)}")

        # Check: does the characteristic polynomial factor over Q(√5)?
        # Use the actual eigenvalues to find minimal polynomials
        print(f"\n  Eigenvalue clusters (by minimal polynomial):")
        # Group eigenvalues that share a minimal polynomial
        # For eigenvalues over Q(√5), conjugates under √5 → -√5 should appear together
        # For eigenvalues over Q(√2), conjugates under √2 → -√2 should appear together
        clusters = []
        used = set()
        for i, v in enumerate(dark_vals):
            if i in used:
                continue
            cluster = [v]
            used.add(i)
            # Look for algebraic conjugate: replace √5 by -√5 in the form
            for j in range(i + 1, len(dark_vals)):
                if j in used:
                    continue
                # Check if v and dark_vals[j] are conjugates
                # They satisfy the same minimal polynomial if they're roots of x² - (v+w)x + vw
                # where v+w and vw are both rational
                w = dark_vals[j]
                s = v + w
                p = v * w
                if abs(s - round(s)) < 1e-6 and abs(p - round(p)) < 1e-6:
                    cluster.append(w)
                    used.add(j)
            if len(cluster) > 1:
                s = sum(cluster)
                p_val = 1
                for c in cluster:
                    p_val *= c
                print(f"    Cluster: {[f'{c:.6f}' for c in cluster]}, sum={s:.6f}, product={p_val:.6f}")
            clusters.append(cluster)

        results[g] = {
            "in_q_sqrt5": in_q_phi,
            "in_q_sqrt2": in_q_sqrt2,
            "unidentified": len(dark_vals) - in_q_phi - in_q_sqrt2,
            "algebraic_forms": [(float(v), f) for v, f in algebraic_forms],
            "n_clusters": len(clusters),
        }

    return results

# ══════════════════════════════════════════════════════════════════
# STEP 5: Dominance Crossover Time
# ══════════════════════════════════════════════════════════════════

def step5(or_mats, hex_eigsystems, step1_results):
    print("\n" + "=" * 70)
    print("STEP 5: DOMINANCE CROSSOVER TIME")
    print("=" * 70)

    results = {}

    for g in GROUP_NAMES:
        print(f"\n── {g} ──")
        A = or_mats[g].astype(float)
        eigvals, eigvecs = hex_eigsystems[g]
        coherent_idx = step1_results[g]["coherent_idx"]
        dark_idx = step1_results[g]["dark_idx"]

        if not dark_idx:
            print("  No dark sector — coherent sector always dominates.")
            results[g] = {"crossover_time": None, "reason": "no dark sector"}
            continue

        # Project initial conditions onto eigenbasis
        # Use hexagram 0 (Kun/Kun) as canonical initial condition
        e0 = np.zeros(64)
        e0[0] = 1.0

        # Coefficients in eigenbasis: c_k = v_k · e0
        coeffs = eigvecs.T @ e0

        # At step n, state = Σ c_k λ_k^n v_k
        # Coherent norm² at step n: Σ_{k∈coherent} |c_k|² |λ_k|^{2n}
        # Dark norm² at step n: Σ_{k∈dark} |c_k|² |λ_k|^{2n}

        max_steps = 100
        crossover = None
        print(f"  Initial condition: hexagram 0")
        print(f"  {'step':>6} {'coherent':>12} {'dark':>12} {'dark_frac':>10}")

        for n in range(max_steps + 1):
            coh_norm2 = sum(coeffs[k]**2 * eigvals[k]**(2*n) for k in coherent_idx)
            dark_norm2 = sum(coeffs[k]**2 * eigvals[k]**(2*n) for k in dark_idx)
            total = coh_norm2 + dark_norm2
            dark_frac = dark_norm2 / total if total > 0 else 0

            if n <= 10 or n % 10 == 0:
                print(f"  {n:>6} {coh_norm2:>12.4f} {dark_norm2:>12.4f} {dark_frac:>10.4f}")

            if crossover is None and dark_frac > 0.5:
                crossover = n

        print(f"  Crossover time (hex 0): {crossover}")

        # Average over all 64 basis vectors
        crossover_times = []
        for h in range(64):
            e_h = np.zeros(64)
            e_h[h] = 1.0
            c = eigvecs.T @ e_h
            for n in range(max_steps + 1):
                coh = sum(c[k]**2 * eigvals[k]**(2*n) for k in coherent_idx)
                dark = sum(c[k]**2 * eigvals[k]**(2*n) for k in dark_idx)
                total = coh + dark
                if total > 0 and dark / total > 0.5:
                    crossover_times.append(n)
                    break
            else:
                crossover_times.append(None)

        valid = [t for t in crossover_times if t is not None]
        avg_crossover = np.mean(valid) if valid else None
        min_crossover = min(valid) if valid else None
        max_crossover = max(valid) if valid else None
        never_cross = sum(1 for t in crossover_times if t is None)

        print(f"\n  Over all 64 basis vectors:")
        print(f"    Average crossover: {avg_crossover}")
        print(f"    Min crossover: {min_crossover}")
        print(f"    Max crossover: {max_crossover}")
        print(f"    Never cross (within {max_steps} steps): {never_cross}")

        # Spectral radius comparison
        coh_rho = max(abs(eigvals[k]) for k in coherent_idx) if coherent_idx else 0
        dark_rho = max(abs(eigvals[k]) for k in dark_idx) if dark_idx else 0
        print(f"    Coherent spectral radius: {coh_rho:.6f}")
        print(f"    Dark spectral radius: {dark_rho:.6f}")
        print(f"    Dark dominates asymptotically: {dark_rho > coh_rho + EPS}")

        results[g] = {
            "crossover_hex0": crossover,
            "avg_crossover": float(avg_crossover) if avg_crossover is not None else None,
            "min_crossover": min_crossover,
            "max_crossover": max_crossover,
            "never_cross": never_cross,
            "coherent_spectral_radius": float(coh_rho),
            "dark_spectral_radius": float(dark_rho),
            "dark_dominates_asymptotically": bool(dark_rho > coh_rho + EPS),
        }

    return results

# ══════════════════════════════════════════════════════════════════
# STEP 6: Summary
# ══════════════════════════════════════════════════════════════════

def step6(s1, s2, s3, s5):
    print("\n" + "=" * 70)
    print("STEP 6: SUMMARY")
    print("=" * 70)

    summary = {}
    for g in GROUP_NAMES:
        r1 = s1[g]
        r2 = s2[g]
        r5 = s5[g]

        print(f"\n── {g} ──")
        print(f"  Coherent: {r1['n_coherent']} eigenvalues, {r1['frac_coherent']:.1%} spectral weight")
        print(f"  Dark:     {r1['n_dark']} eigenvalues, {r1['frac_dark']:.1%} spectral weight")

        if r2.get("dominant_weights"):
            print(f"  Dominant Walsh weights: {r2['dominant_weights']}")

        if isinstance(r5, dict) and "dark_dominates_asymptotically" in r5:
            print(f"  Dark dominates asymptotically: {r5['dark_dominates_asymptotically']}")
            if r5["avg_crossover"] is not None:
                print(f"  Average crossover time: {r5['avg_crossover']:.1f} steps")

        summary[g] = {
            "n_coherent": r1["n_coherent"],
            "n_dark": r1["n_dark"],
            "frac_coherent": r1["frac_coherent"],
            "frac_dark": r1["frac_dark"],
            "dominant_walsh_weights": r2.get("dominant_weights", []),
            "crossover_time": r5.get("avg_crossover") if isinstance(r5, dict) else None,
        }

    return summary

# ── Main ──────────────────────────────────────────────────────────

def main():
    atlas = load_atlas()
    transitions = load_transitions()

    dir_mats = build_directed_matrices(transitions)
    or_mats = build_or_symmetrized(dir_mats)
    trig_elems = get_trigram_elements(atlas)
    trig_mats = build_trigram_matrices(trig_elems)

    s1, hex_eigsystems = step1(or_mats, trig_mats)
    s2 = step2(hex_eigsystems, s1)
    s3 = step3(hex_eigsystems, s1)
    s4 = step4(hex_eigsystems, s1)
    s5 = step5(or_mats, hex_eigsystems, s1)
    s6 = step6(s1, s2, s3, s5)

    all_results = {
        "step1_sector_separation": s1,
        "step2_walsh_decomposition": s2,
        "step3_symmetry_classification": s3,
        "step4_algebraic_structure": s4,
        "step5_dominance_crossover": s5,
        "step6_summary": s6,
    }

    out_path = HERE / "dark_sector_results.json"
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
