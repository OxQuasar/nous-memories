#!/usr/bin/env python3
"""
Opposition Theory — n=6 Opposition Measures

Computes opposition measures for:
  A. KW pairing (28 reversal + 4 complement for palindromes)
  B. Shao Yong / complement pairing (32 complement pairs)
  C. 100,000 random pairings (uniform random perfect matchings)
  D. Z₂² orbit structure and equivariant pairing analysis

Measures per pairing:
  1. Strength: Σ popcount(a XOR b)
  2. Diversity: Shannon entropy of XOR mask distribution
  4a. Weight tilt: mean |Δ yang-count|
  5. Weight complementarity: Pearson r of yang-counts
"""

import math
import time
from collections import Counter
from pathlib import Path

import numpy as np

# ─── Constants ────────────────────────────────────────────────────────────────

N = 6
NUM_STATES = 1 << N  # 64
NUM_PAIRS = NUM_STATES // 2  # 32
NUM_MASKS = NUM_STATES - 1  # 63 possible nonzero XOR masks
SAMPLE_SIZE = 100_000

# Precompute tables
POPCOUNT = np.array([bin(x).count('1') for x in range(NUM_STATES)], dtype=np.int32)

def _reverse(x):
    bits = format(x, f'0{N}b')
    return int(bits[::-1], 2)

REVERSE = np.array([_reverse(x) for x in range(NUM_STATES)], dtype=np.int32)
COMPLEMENT = np.array([x ^ ((1 << N) - 1) for x in range(NUM_STATES)], dtype=np.int32)
COMP_REV = COMPLEMENT[REVERSE]  # complement(reverse(x))

PALINDROMES = np.array([x for x in range(NUM_STATES) if REVERSE[x] == x], dtype=np.int32)
PALINDROME_SET = set(PALINDROMES)

def fmt(x):
    return format(x, f'0{N}b')


# ─── Measure computation ─────────────────────────────────────────────────────

def compute_measures(pairs):
    """
    Compute opposition measures for a pairing.
    pairs: array of shape (NUM_PAIRS, 2), each row is (a, b).
    Returns: (strength, diversity, weight_tilt, weight_corr)
    """
    a = pairs[:, 0]
    b = pairs[:, 1]
    xor = a ^ b

    # 1. Strength
    strength = int(POPCOUNT[xor].sum())

    # 2. Diversity (entropy of XOR mask distribution)
    mask_counts = Counter(xor.tolist())
    entropy = 0.0
    for c in mask_counts.values():
        p = c / NUM_PAIRS
        entropy -= p * math.log2(p)
    entropy = max(0.0, entropy)

    # 4a. Weight tilt
    wa = POPCOUNT[a]
    wb = POPCOUNT[b]
    weight_tilt = float(np.abs(wa - wb).mean())

    # 5. Weight complementarity
    wa_f = wa.astype(np.float64)
    wb_f = wb.astype(np.float64)
    if wa_f.std() == 0 or wb_f.std() == 0:
        weight_corr = 0.0
    else:
        weight_corr = float(np.corrcoef(wa_f, wb_f)[0, 1])

    return strength, entropy, weight_tilt, weight_corr


def compute_measures_detail(pairs):
    """Same as compute_measures but also returns mask distribution."""
    a = pairs[:, 0]
    b = pairs[:, 1]
    xor = a ^ b
    strength = int(POPCOUNT[xor].sum())
    mask_counts = Counter(xor.tolist())
    entropy = max(0.0, -sum((c/NUM_PAIRS) * math.log2(c/NUM_PAIRS) for c in mask_counts.values()))
    wa = POPCOUNT[a]
    wb = POPCOUNT[b]
    weight_tilt = float(np.abs(wa - wb).mean())
    wa_f, wb_f = wa.astype(float), wb.astype(float)
    weight_corr = float(np.corrcoef(wa_f, wb_f)[0, 1]) if wa_f.std() > 0 and wb_f.std() > 0 else 0.0
    return strength, entropy, weight_tilt, weight_corr, mask_counts


# ─── Named pairings ──────────────────────────────────────────────────────────

def make_kw_pairing():
    """KW rule: reversal for non-palindromes, complement for palindromes."""
    pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        if x in PALINDROME_SET:
            partner = int(COMPLEMENT[x])
        else:
            partner = int(REVERSE[x])
        pairs.append((min(x, partner), max(x, partner)))
        seen.update((x, partner))
    return np.array(sorted(pairs), dtype=np.int32)


def make_complement_pairing():
    """Shao Yong: all complement pairs."""
    pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        c = int(COMPLEMENT[x])
        pairs.append((min(x, c), max(x, c)))
        seen.update((x, c))
    return np.array(sorted(pairs), dtype=np.int32)


def random_pairing(rng):
    """Generate a uniform random perfect matching: shuffle and pair consecutive."""
    perm = rng.permutation(NUM_STATES)
    a = perm[0::2]
    b = perm[1::2]
    pairs = np.column_stack([np.minimum(a, b), np.maximum(a, b)])
    return pairs


# ─── Z₂² orbit structure ─────────────────────────────────────────────────────

def compute_orbits():
    """Orbits under Z₂² = {id, complement, reversal, comp∘rev}."""
    visited = set()
    orbits = []
    for x in range(NUM_STATES):
        if x in visited:
            continue
        orbit = {x, int(COMPLEMENT[x]), int(REVERSE[x]), int(COMP_REV[x])}
        orbits.append(sorted(orbit))
        visited |= orbit
    return orbits


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = Path(__file__).parent
    rng = np.random.default_rng(42)

    print("=" * 70)
    print("n=6 OPPOSITION MEASURES")
    print("=" * 70)

    # ── Verify palindromes ──
    print(f"\n## Palindromes at n=6")
    print(f"Count: {len(PALINDROMES)} (expected 2^(6/2) = 8)")
    for p in PALINDROMES:
        print(f"  {fmt(p)}  (yang={POPCOUNT[p]})")
    assert len(PALINDROMES) == 8

    # ── Z₂² orbits ──
    orbits = compute_orbits()
    size_dist = Counter(len(o) for o in orbits)
    print(f"\n## Z₂² Orbit Structure")
    print(f"Total orbits: {len(orbits)}")
    print(f"Size distribution: {dict(size_dist)}")

    # Fixed points
    rev_fixed = [x for x in range(NUM_STATES) if REVERSE[x] == x]
    cr_fixed = [x for x in range(NUM_STATES) if COMP_REV[x] == x]
    comp_fixed = [x for x in range(NUM_STATES) if COMPLEMENT[x] == x]
    print(f"Reversal-fixed (palindromes): {len(rev_fixed)}")
    print(f"Comp∘rev-fixed: {len(cr_fixed)}")
    print(f"Complement-fixed: {len(comp_fixed)}")
    if cr_fixed:
        print(f"  comp∘rev fixed points: {', '.join(fmt(x) for x in cr_fixed)}")

    # ── A. KW pairing ──
    print(f"\n{'='*70}")
    print("A. KING WEN PAIRING")
    print(f"{'='*70}")

    kw_pairs = make_kw_pairing()
    assert kw_pairs.shape == (NUM_PAIRS, 2)

    # Verify structure: count complement vs reversal pairs
    n_comp = sum(1 for a, b in kw_pairs if int(COMPLEMENT[a]) == b)
    n_rev = sum(1 for a, b in kw_pairs if int(REVERSE[a]) == b or int(REVERSE[b]) == a)
    n_pal_comp = sum(1 for a, b in kw_pairs
                     if int(COMPLEMENT[a]) == b and (a in PALINDROME_SET or b in PALINDROME_SET))
    n_accidental = n_comp - n_pal_comp  # non-palindromes where rev(x) == comp(x)
    print(f"Complement pairs: {n_comp} total")
    print(f"  from palindromes: {n_pal_comp}")
    print(f"  accidental (rev=comp, comp∘rev-fixed states): {n_accidental}")
    print(f"Reversal pairs: {n_rev} (includes {n_accidental} that are also complement)")
    print(f"Pure reversal (rev≠comp): {n_rev - n_accidental}")
    assert n_pal_comp == 4, f"Expected 4 palindrome complement pairs, got {n_pal_comp}"

    s, d, wt, wc, masks = compute_measures_detail(kw_pairs)
    print(f"\nMeasures:")
    print(f"  Strength:          {s}")
    print(f"  Diversity:         {d:.6f}")
    print(f"  Weight Tilt:       {wt:.4f}")
    print(f"  Weight Correlation:{wc:+.6f}")

    # Mask analysis
    print(f"\nMask distribution ({len(masks)} distinct masks):")
    for mask, count in sorted(masks.items(), key=lambda x: -x[1])[:15]:
        print(f"  {fmt(mask)} (dist={POPCOUNT[mask]}): {count}")
    if len(masks) > 15:
        print(f"  ... and {len(masks) - 15} more")

    # Distance distribution
    dists = POPCOUNT[kw_pairs[:, 0] ^ kw_pairs[:, 1]]
    dist_counts = Counter(dists.tolist())
    print(f"\nHamming distance distribution:")
    for d_val in sorted(dist_counts):
        print(f"  dist={d_val}: {dist_counts[d_val]} pairs")

    kw_measures = (s, d, wt, wc)

    # Print some example pairs
    print(f"\nAll 32 KW pairs:")
    for a, b in kw_pairs:
        xor = a ^ b
        ptype = "comp" if int(COMPLEMENT[a]) == b else "rev"
        print(f"  {fmt(a)} ↔ {fmt(b)}  XOR={fmt(xor)} dist={POPCOUNT[xor]} "
              f"Δw={abs(int(POPCOUNT[a])-int(POPCOUNT[b]))} [{ptype}]")

    # ── B. Shao Yong pairing ──
    print(f"\n{'='*70}")
    print("B. SHAO YONG (COMPLEMENT) PAIRING")
    print(f"{'='*70}")

    sy_pairs = make_complement_pairing()
    s, d, wt, wc, masks = compute_measures_detail(sy_pairs)
    print(f"\nMeasures:")
    print(f"  Strength:          {s}")
    print(f"  Diversity:         {d:.6f}")
    print(f"  Weight Tilt:       {wt:.4f}")
    print(f"  Weight Correlation:{wc:+.6f}")
    print(f"  Distinct masks:    {len(masks)}")

    sy_measures = (s, d, wt, wc)

    # ── Comparison table ──
    print(f"\n{'='*70}")
    print("COMPARISON: KW vs SHAO YONG")
    print(f"{'='*70}")
    print(f"{'Measure':<25} {'KW':>12} {'Shao Yong':>12}")
    print(f"{'-'*25} {'-'*12} {'-'*12}")
    labels = ['Strength', 'Diversity', 'Weight Tilt', 'Weight Corr']
    for label, kv, sv in zip(labels, kw_measures, sy_measures):
        if isinstance(kv, int):
            print(f"{label:<25} {kv:>12} {sv:>12}")
        else:
            print(f"{label:<25} {kv:>12.6f} {sv:>12.6f}")

    # ── C. Random sample ──
    print(f"\n{'='*70}")
    print(f"C. RANDOM SAMPLE ({SAMPLE_SIZE:,} pairings)")
    print(f"{'='*70}")

    t0 = time.time()
    strengths = np.empty(SAMPLE_SIZE, dtype=np.int32)
    diversities = np.empty(SAMPLE_SIZE, dtype=np.float64)
    weight_tilts = np.empty(SAMPLE_SIZE, dtype=np.float64)
    weight_corrs = np.empty(SAMPLE_SIZE, dtype=np.float64)

    for i in range(SAMPLE_SIZE):
        pairs = random_pairing(rng)
        s, d, wt, wc = compute_measures(pairs)
        strengths[i] = s
        diversities[i] = d
        weight_tilts[i] = wt
        weight_corrs[i] = wc

        if (i + 1) % 25_000 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            print(f"  {i+1:>8,} / {SAMPLE_SIZE:,} ({100*(i+1)/SAMPLE_SIZE:.0f}%)  "
                  f"{rate:.0f}/s")

    t_sample = time.time() - t0
    print(f"  Sampling time: {t_sample:.1f}s")

    # ── Sample statistics ──
    print(f"\n## Sample Statistics")
    for name, arr in [("Strength", strengths), ("Diversity", diversities),
                      ("Weight Tilt", weight_tilts), ("Weight Corr", weight_corrs)]:
        print(f"\n  {name}:")
        print(f"    range: [{arr.min():.4f}, {arr.max():.4f}]")
        print(f"    mean:  {arr.mean():.4f}  std: {arr.std():.4f}")

    # ── r(S, D) ──
    r_sd = np.corrcoef(strengths.astype(float), diversities)[0, 1]
    r_sw = np.corrcoef(strengths.astype(float), weight_corrs)[0, 1]
    r_dw = np.corrcoef(diversities, weight_corrs)[0, 1]
    r_st = np.corrcoef(strengths.astype(float), weight_tilts)[0, 1]
    r_dt = np.corrcoef(diversities, weight_tilts)[0, 1]
    r_tw = np.corrcoef(weight_tilts, weight_corrs)[0, 1]

    print(f"\n## Inter-Measure Correlations (from sample)")
    print(f"  Strength ↔ Diversity:    r = {r_sd:+.6f}")
    print(f"  Strength ↔ Weight Tilt:  r = {r_st:+.6f}")
    print(f"  Strength ↔ Weight Corr:  r = {r_sw:+.6f}")
    print(f"  Diversity ↔ Weight Tilt: r = {r_dt:+.6f}")
    print(f"  Diversity ↔ Weight Corr: r = {r_dw:+.6f}")
    print(f"  Wt Tilt ↔ Weight Corr:   r = {r_tw:+.6f}")

    # ── KW percentiles ──
    print(f"\n## KW Position in Random Distribution")
    kw_s, kw_d, kw_wt, kw_wc = kw_measures
    for name, kw_val, arr in [
        ("Strength", kw_s, strengths),
        ("Diversity", kw_d, diversities),
        ("Weight Tilt", kw_wt, weight_tilts),
        ("Weight Corr", kw_wc, weight_corrs),
    ]:
        pct = 100 * np.mean(arr <= kw_val)
        print(f"  {name:<20}: KW={kw_val:>10.4f}  "
              f"sample=[{arr.min():.4f}, {arr.max():.4f}]  "
              f"percentile={pct:.2f}%")

    # Also report Shao Yong percentiles
    print(f"\n## Shao Yong Position in Random Distribution")
    sy_s, sy_d, sy_wt, sy_wc = sy_measures
    for name, sy_val, arr in [
        ("Strength", sy_s, strengths),
        ("Diversity", sy_d, diversities),
        ("Weight Tilt", sy_wt, weight_tilts),
        ("Weight Corr", sy_wc, weight_corrs),
    ]:
        pct = 100 * np.mean(arr <= sy_val)
        print(f"  {name:<20}: SY={sy_val:>10.4f}  "
              f"percentile={pct:.2f}%")

    # ── Strength distribution ──
    print(f"\n## Strength Distribution (sample)")
    s_vals, s_counts = np.unique(strengths, return_counts=True)
    for v, c in zip(s_vals, s_counts):
        if c >= 10:
            bar = '█' * max(1, int(50 * c / s_counts.max()))
            print(f"  S={v:3d}: {c:>6,} {bar}")

    # ── Does max diversity constrain with strength? ──
    print(f"\n## Strength-Diversity Boundary (sample)")
    s_unique = sorted(set(strengths))
    for sv in s_unique:
        mask = strengths == sv
        if mask.sum() >= 5:
            print(f"  S={sv:3d}: n={mask.sum():>6,}  "
                  f"D=[{diversities[mask].min():.4f}, {diversities[mask].max():.4f}]  "
                  f"mean_D={diversities[mask].mean():.4f}")

    # ── D. Z₂² equivariant analysis ──
    print(f"\n{'='*70}")
    print("D. Z₂² EQUIVARIANCE ANALYSIS")
    print(f"{'='*70}")

    # Check equivariance of named pairings
    def is_equivariant(pairs_arr, op):
        """Check if applying op to both members preserves the pairing."""
        pair_set = set()
        for a, b in pairs_arr:
            pair_set.add((min(a, b), max(a, b)))
        for a, b in pairs_arr:
            oa, ob = int(op[a]), int(op[b])
            if (min(oa, ob), max(oa, ob)) not in pair_set:
                return False
        return True

    print(f"\n  KW pairing equivariance:")
    print(f"    under complement: {is_equivariant(kw_pairs, COMPLEMENT)}")
    print(f"    under reversal:   {is_equivariant(kw_pairs, REVERSE)}")
    print(f"    under comp∘rev:   {is_equivariant(kw_pairs, COMP_REV)}")

    print(f"\n  Shao Yong pairing equivariance:")
    print(f"    under complement: {is_equivariant(sy_pairs, COMPLEMENT)}")
    print(f"    under reversal:   {is_equivariant(sy_pairs, REVERSE)}")
    print(f"    under comp∘rev:   {is_equivariant(sy_pairs, COMP_REV)}")

    print(f"\n  Equivariant fraction estimation (fresh 10K sample):")
    rng2 = np.random.default_rng(123)
    eq_counts = {'complement': 0, 'reversal': 0, 'comp_rev': 0, 'all': 0}
    EST_N = 10_000
    for i in range(EST_N):
        pairs = random_pairing(rng2)
        c = is_equivariant(pairs, COMPLEMENT)
        r = is_equivariant(pairs, REVERSE)
        cr = is_equivariant(pairs, COMP_REV)
        if c: eq_counts['complement'] += 1
        if r: eq_counts['reversal'] += 1
        if cr: eq_counts['comp_rev'] += 1
        if c and r and cr: eq_counts['all'] += 1

    for op_name, count in eq_counts.items():
        print(f"    {op_name:>12}: {count}/{EST_N} = {100*count/EST_N:.4f}%")

    # ── Save data ──
    save_path = out_dir / 'sample_measures.npz'
    np.savez_compressed(save_path,
        strengths=strengths,
        diversities=diversities,
        weight_tilts=weight_tilts,
        weight_corrs=weight_corrs,
    )
    print(f"\nSaved sample data to {save_path}")
    print(f"File size: {save_path.stat().st_size / 1024:.1f} KB")

    # Save summary as JSON
    import json
    summary = {
        'kw_pairing': {
            'strength': int(kw_measures[0]),
            'diversity': round(kw_measures[1], 6),
            'weight_tilt': round(kw_measures[2], 4),
            'weight_corr': round(kw_measures[3], 6),
        },
        'shao_yong_pairing': {
            'strength': int(sy_measures[0]),
            'diversity': round(sy_measures[1], 6),
            'weight_tilt': round(sy_measures[2], 4),
            'weight_corr': round(sy_measures[3], 6),
        },
        'sample_correlations': {
            'strength_diversity': round(float(r_sd), 6),
            'strength_weight_corr': round(float(r_sw), 6),
            'strength_weight_tilt': round(float(r_st), 6),
            'diversity_weight_corr': round(float(r_dw), 6),
            'diversity_weight_tilt': round(float(r_dt), 6),
        },
        'sample_size': SAMPLE_SIZE,
        'n_orbits': len(orbits),
        'orbit_sizes': dict(size_dist),
        'palindromes': [fmt(p) for p in PALINDROMES],
    }
    json_path = out_dir / 'summary.json'
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Saved summary to {json_path}")


if __name__ == '__main__':
    main()
