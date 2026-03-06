#!/usr/bin/env python3
"""
Phase 2: n=6 Equivariant Pairing Analysis

Structural decomposition of the equivariant pairing space:

The Z₂² group acts on state orbits independently:
  - 4 palindrome size-2 orbits: self-match (1 way) or inter-pair (2 ways per pair)
  - 4 comp_rev-fixed size-2 orbits: same structure
  - 12 size-4 orbits: self-match (3 ways: comp/rev/cr) or inter-pair (4 ways per pair)

These three groups are INDEPENDENT — no cross-group pairing is possible.
Total = ways(pal) × ways(cr) × ways(size4)

At n=4 this gives 3 × 3 × 13 = 117. ✓

At n=6: 25 × 25 × 2,513,795,337 ≈ 1.57 × 10¹². Too many to enumerate.

Strategy: 
  - Enumerate all 625 size-2 combinations exhaustively
  - Sample size-4 combinations (they dominate the count)
  - Measures decompose additively: S and mask counts are sums over pair-orbits
"""

import math
import time
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np

# ─── Constants ────────────────────────────────────────────────────────────────

N = 6
NUM_STATES = 1 << N  # 64
NUM_PAIRS = NUM_STATES // 2  # 32
MASK_ALL = (1 << N) - 1

POPCOUNT = [bin(x).count('1') for x in range(NUM_STATES)]

def _reverse(x):
    bits = format(x, f'0{N}b')
    return int(bits[::-1], 2)

REVERSE = [_reverse(x) for x in range(NUM_STATES)]
COMPLEMENT = [x ^ MASK_ALL for x in range(NUM_STATES)]
COMP_REV = [COMPLEMENT[REVERSE[x]] for x in range(NUM_STATES)]

def fmt(x):
    return format(x, f'0{N}b')


# ─── Orbit computation ───────────────────────────────────────────────────────

def compute_state_orbits():
    visited = set()
    orbits = []
    for x in range(NUM_STATES):
        if x in visited:
            continue
        orbit = sorted({x, COMPLEMENT[x], REVERSE[x], COMP_REV[x]})
        orbits.append(orbit)
        visited.update(orbit)
    return orbits


def classify_orbits(orbits):
    """Separate orbits into palindrome, cr-fixed, and size-4."""
    pal_orbits = []   # {p, comp(p)} where rev(p)=p
    cr_orbits = []    # {x, comp(x)} where comp_rev(x)=x (i.e., rev(x)=comp(x))
    big_orbits = []   # size 4

    for o in orbits:
        if len(o) == 2:
            a = o[0]
            if REVERSE[a] == a or REVERSE[o[1]] == o[1]:
                pal_orbits.append(o)
            else:
                cr_orbits.append(o)
        else:
            big_orbits.append(o)

    return pal_orbits, cr_orbits, big_orbits


# ─── Pair contributions ──────────────────────────────────────────────────────

def pair_strength(a, b):
    return POPCOUNT[a ^ b]

def pair_data(a, b):
    """Returns (strength, mask, |Δweight|, wa, wb)."""
    xor = a ^ b
    return POPCOUNT[xor], xor, abs(POPCOUNT[a] - POPCOUNT[b]), POPCOUNT[a], POPCOUNT[b]


# ─── Size-2 orbit choices ────────────────────────────────────────────────────

def enumerate_size2_choices(orbit_list):
    """
    Enumerate all valid configurations of size-2 orbits.
    
    Each orbit can be:
      - self-matched: pair the two elements (1 way)
      - linked with another orbit: 2 ways (a↔c or a↔comp(c))
    
    Returns list of configurations, each being a list of (a,b) pairs.
    """
    n = len(orbit_list)
    configs = []

    def recurse(remaining_idx, pairs):
        if not remaining_idx:
            configs.append(pairs[:])
            return

        first = remaining_idx[0]
        rest = remaining_idx[1:]
        a, ca = orbit_list[first]  # a and comp(a)

        # Option 1: self-match
        pairs.append((min(a, ca), max(a, ca)))
        recurse(rest, pairs)
        pairs.pop()

        # Option 2: pair with another orbit
        for i, other in enumerate(rest):
            c, cc = orbit_list[other]
            new_rest = rest[:i] + rest[i+1:]

            # Linking 1: a↔c, comp(a)↔comp(c)
            pairs.append((min(a, c), max(a, c)))
            pairs.append((min(ca, cc), max(ca, cc)))
            recurse(new_rest, pairs)
            pairs.pop()
            pairs.pop()

            # Linking 2: a↔comp(c), comp(a)↔c
            pairs.append((min(a, cc), max(a, cc)))
            pairs.append((min(ca, c), max(ca, c)))
            recurse(new_rest, pairs)
            pairs.pop()
            pairs.pop()

    recurse(list(range(n)), [])
    return configs


# ─── Size-4 orbit choices ────────────────────────────────────────────────────

def size4_intra_options(orbit):
    """Three equivariant matchings within a size-4 orbit."""
    x = orbit[0]
    cx, rx, crx = COMPLEMENT[x], REVERSE[x], COMP_REV[x]
    return [
        [(min(x,cx), max(x,cx)), (min(rx,crx), max(rx,crx))],     # comp
        [(min(x,rx), max(x,rx)), (min(cx,crx), max(cx,crx))],     # rev
        [(min(x,crx), max(x,crx)), (min(cx,rx), max(cx,rx))],     # cr
    ]


def size4_inter_options(orbit_a, orbit_b):
    """Four equivariant inter-orbit matchings for two size-4 orbits."""
    a = orbit_a[0]
    ca, ra, cra = COMPLEMENT[a], REVERSE[a], COMP_REV[a]
    targets = [orbit_b[0], COMPLEMENT[orbit_b[0]],
               REVERSE[orbit_b[0]], COMP_REV[orbit_b[0]]]

    options = []
    for t in targets:
        ct, rt, crt = COMPLEMENT[t], REVERSE[t], COMP_REV[t]
        pairs = [
            (min(a,t), max(a,t)),
            (min(ca,ct), max(ca,ct)),
            (min(ra,rt), max(ra,rt)),
            (min(cra,crt), max(cra,crt)),
        ]
        options.append(sorted(pairs))

    # Deduplicate (in case some options produce the same pairs)
    unique = []
    seen = set()
    for opt in options:
        key = tuple(opt)
        if key not in seen:
            seen.add(key)
            unique.append(opt)
    return unique


def sample_size4_config(big_orbits, rng):
    """
    Sample one random size-4 orbit configuration.
    Returns a list of (a,b) pairs.
    
    Strategy: recursively, for each orbit, randomly choose to self-match
    (3 options) or pair with a remaining orbit (4 options each).
    The probability of self vs inter needs to be weighted correctly for
    uniform sampling.
    """
    n = len(big_orbits)
    # To sample uniformly, we need to weight by the number of downstream configs.
    # count(n) = 3 * count(n-1) + 4 * (n-1) * count(n-2)  for n >= 2
    # count(0) = 1, count(1) = 3
    counts = [0] * (n + 1)
    counts[0] = 1
    if n >= 1:
        counts[1] = 3
    for k in range(2, n + 1):
        counts[k] = 3 * counts[k-1] + 4 * (k-1) * counts[k-2]

    pairs = []
    remaining = list(range(n))

    while remaining:
        k = len(remaining)
        first_idx = remaining[0]

        # Weight of self-match branch
        w_self = 3 * counts[k-1]
        # Weight of each inter-match branch: 4 * counts[k-2] per partner
        w_inter_each = 4 * counts[k-2] if k >= 2 else 0
        w_inter_total = w_inter_each * (k - 1)
        total_w = w_self + w_inter_total

        r = rng.integers(total_w)
        if r < w_self:
            # Self-match: pick one of 3 options
            options = size4_intra_options(big_orbits[first_idx])
            choice = rng.integers(3)
            pairs.extend(options[choice])
            remaining = remaining[1:]
        else:
            # Inter-match: pick partner and one of 4 options
            r -= w_self
            partner_pos = r // (4 * counts[k-2])
            r2 = r % (4 * counts[k-2])
            link_choice = r2 // counts[k-2]

            partner_idx = remaining[1 + partner_pos]
            options = size4_inter_options(big_orbits[first_idx],
                                          big_orbits[partner_idx])
            # options might have < 4 if dedup happened, but should be 4
            pairs.extend(options[link_choice % len(options)])
            remaining = [i for i in remaining
                         if i != first_idx and i != partner_idx]

    return pairs


# ─── Measures ─────────────────────────────────────────────────────────────────

def compute_measures(pairs):
    """Returns (strength, diversity, weight_tilt, weight_corr)."""
    strength = sum(POPCOUNT[a ^ b] for a, b in pairs)

    masks = [a ^ b for a, b in pairs]
    mask_counts = Counter(masks)
    entropy = max(0.0, -sum((c/NUM_PAIRS) * math.log2(c/NUM_PAIRS)
                             for c in mask_counts.values()))

    abs_diffs = [abs(POPCOUNT[a] - POPCOUNT[b]) for a, b in pairs]
    weight_tilt = sum(abs_diffs) / NUM_PAIRS

    wa = np.array([POPCOUNT[a] for a, b in pairs], dtype=float)
    wb = np.array([POPCOUNT[b] for a, b in pairs], dtype=float)
    if wa.std() == 0 or wb.std() == 0:
        weight_corr = 0.0
    else:
        weight_corr = float(np.corrcoef(wa, wb)[0, 1])

    return strength, round(entropy, 6), round(weight_tilt, 4), round(weight_corr, 6)


def compute_measures_detail(pairs):
    """Like compute_measures but also returns mask_counts."""
    s, d, wt, wc = compute_measures(pairs)
    mask_counts = Counter(a ^ b for a, b in pairs)
    return s, d, wt, wc, mask_counts


# ─── Named pairings ──────────────────────────────────────────────────────────

def make_kw_pairing():
    palindrome_set = {x for x in range(NUM_STATES) if REVERSE[x] == x}
    pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        partner = COMPLEMENT[x] if x in palindrome_set else REVERSE[x]
        pairs.append((min(x, partner), max(x, partner)))
        seen.update((x, partner))
    return sorted(pairs)


def make_complement_pairing():
    pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        c = COMPLEMENT[x]
        pairs.append((min(x, c), max(x, c)))
        seen.update((x, c))
    return sorted(pairs)


def make_cr_pairing():
    """Pair each x with comp_rev(x). Invalid if comp_rev has fixed points."""
    pairs = []
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        y = COMP_REV[x]
        if y == x:
            return None
        pairs.append((min(x, y), max(x, y)))
        seen.update((x, y))
    return sorted(pairs)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = Path(__file__).parent
    lines = []

    def pr(s=""):
        print(s)
        lines.append(s)

    pr("=" * 70)
    pr("PHASE 2: n=6 EQUIVARIANT PAIRING ANALYSIS")
    pr("=" * 70)

    # ── Orbit structure ──
    state_orbits = compute_state_orbits()
    pal_orbits, cr_orbits, big_orbits = classify_orbits(state_orbits)

    pr(f"\nOrbit decomposition:")
    pr(f"  Palindrome orbits (size 2): {len(pal_orbits)}")
    for o in pal_orbits:
        pr(f"    {[fmt(x) for x in o]}")
    pr(f"  Comp-rev-fixed orbits (size 2): {len(cr_orbits)}")
    for o in cr_orbits:
        pr(f"    {[fmt(x) for x in o]}")
    pr(f"  Size-4 orbits: {len(big_orbits)}")
    for o in big_orbits:
        pr(f"    {[fmt(x) for x in o]}")

    # ── Counting ──
    pr(f"\n{'='*70}")
    pr("EQUIVARIANT PAIRING COUNT")
    pr(f"{'='*70}")

    # Count formulas
    def count_size2_configs(n):
        """Configs for n size-2 orbits with 1 self + 2 inter options."""
        if n == 0: return 1
        if n == 1: return 1
        c = [0] * (n + 1)
        c[0] = 1
        c[1] = 1
        for k in range(2, n + 1):
            c[k] = c[k-1] + 2 * (k-1) * c[k-2]
        return c[n]

    def count_size4_configs(n):
        """Configs for n size-4 orbits with 3 self + 4 inter options."""
        if n == 0: return 1
        if n == 1: return 3
        c = [0] * (n + 1)
        c[0] = 1
        c[1] = 3
        for k in range(2, n + 1):
            c[k] = 3 * c[k-1] + 4 * (k-1) * c[k-2]
        return c[n]

    n_pal = count_size2_configs(len(pal_orbits))
    n_cr = count_size2_configs(len(cr_orbits))
    n_big = count_size4_configs(len(big_orbits))

    pr(f"\n  Palindrome orbit configs: {n_pal}")
    pr(f"  CR-fixed orbit configs: {n_cr}")
    pr(f"  Size-4 orbit configs: {n_big:,}")
    pr(f"  Total equivariant pairings: {n_pal} × {n_cr} × {n_big:,} = {n_pal * n_cr * n_big:,}")

    # Verify at n=4
    pr(f"\n  Verification at n=4: {count_size2_configs(2)} × {count_size2_configs(2)} × {count_size4_configs(2)}"
       f" = {count_size2_configs(2) * count_size2_configs(2) * count_size4_configs(2)} (expected 117)")

    total_eq = n_pal * n_cr * n_big

    # ── Enumerate size-2 configs ──
    pr(f"\n{'='*70}")
    pr("SIZE-2 ORBIT CONFIGURATIONS")
    pr(f"{'='*70}")

    pal_configs = enumerate_size2_choices(pal_orbits)
    cr_configs = enumerate_size2_choices(cr_orbits)
    pr(f"\n  Palindrome configs enumerated: {len(pal_configs)} (expected {n_pal})")
    pr(f"  CR-fixed configs enumerated: {len(cr_configs)} (expected {n_cr})")

    # Compute strength contribution from each size-2 config
    pr(f"\n  Palindrome config strengths:")
    pal_strengths = []
    for cfg in pal_configs:
        s = sum(pair_strength(a, b) for a, b in cfg)
        pal_strengths.append(s)
    for s_val, cnt in sorted(Counter(pal_strengths).items()):
        pr(f"    S_pal={s_val}: {cnt} configs")

    pr(f"\n  CR-fixed config strengths:")
    cr_strengths = []
    for cfg in cr_configs:
        s = sum(pair_strength(a, b) for a, b in cfg)
        cr_strengths.append(s)
    for s_val, cnt in sorted(Counter(cr_strengths).items()):
        pr(f"    S_cr={s_val}: {cnt} configs")

    # ── Size-4 intra-orbit analysis ──
    pr(f"\n{'='*70}")
    pr("SIZE-4 ORBIT INTRA-MATCH OPTIONS")
    pr(f"{'='*70}")

    for i, orb in enumerate(big_orbits):
        x = orb[0]
        options = size4_intra_options(orb)
        pr(f"\n  Orbit {i}: {[fmt(s) for s in orb]}")
        for label, opt in zip(['comp', 'rev', 'cr'], options):
            s_contrib = sum(pair_strength(a, b) for a, b in opt)
            masks = [a ^ b for a, b in opt]
            pr(f"    {label:4s}: S={s_contrib}, masks={[fmt(m) for m in masks]}")

    # ── Named pairings ──
    pr(f"\n{'='*70}")
    pr("NAMED PAIRING DECOMPOSITION")
    pr(f"{'='*70}")

    kw_pairing = make_kw_pairing()
    comp_pairing = make_complement_pairing()

    # Decompose KW into orbit choices
    orbit_map = {}
    for i, orb in enumerate(pal_orbits):
        for x in orb:
            orbit_map[x] = ('pal', i)
    for i, orb in enumerate(cr_orbits):
        for x in orb:
            orbit_map[x] = ('cr', i)
    for i, orb in enumerate(big_orbits):
        for x in orb:
            orbit_map[x] = ('big', i)

    def decompose_pairing(pairing, label):
        pr(f"\n  {label}:")
        pal_pairs = []
        cr_pairs = []
        big_pairs = []

        for a, b in pairing:
            otype, oidx = orbit_map[a]
            if otype == 'pal':
                pal_pairs.append((a, b))
            elif otype == 'cr':
                cr_pairs.append((a, b))
            else:
                big_pairs.append((a, b))

        s, d, wt, wc = compute_measures(pairing)
        pr(f"    Total measures: S={s}, D={d:.6f}, WT={wt:.4f}, WC={wc:+.6f}")
        pr(f"    Pairs: {len(pal_pairs)} pal + {len(cr_pairs)} cr + {len(big_pairs)} big = {len(pairing)}")

        # Size-4 orbit choices
        big_by_orbit = {}
        for a, b in big_pairs:
            _, oidx = orbit_map[a]
            if oidx not in big_by_orbit:
                big_by_orbit[oidx] = []
            big_by_orbit[oidx].append((a, b))

        # Check if each size-4 orbit is intra-matched
        for oidx, pairs in sorted(big_by_orbit.items()):
            if len(pairs) == 2:
                # Intra-orbit: which type?
                a1, b1 = pairs[0]
                if COMPLEMENT[a1] == b1 or COMPLEMENT[b1] == a1:
                    ptype = 'comp'
                elif REVERSE[a1] == b1 or REVERSE[b1] == a1:
                    ptype = 'rev'
                else:
                    ptype = 'cr'
                pr(f"    Big orbit {oidx}: intra-{ptype}")
            else:
                pr(f"    Big orbit {oidx}: inter ({len(pairs)} pairs)")

        return s, d, wt, wc

    kw_s, kw_d, kw_wt, kw_wc = decompose_pairing(kw_pairing, "KW pairing")
    comp_s, comp_d, comp_wt, comp_wc = decompose_pairing(comp_pairing, "Complement pairing")

    # ── Sample equivariant pairings ──
    pr(f"\n{'='*70}")
    pr("SAMPLING EQUIVARIANT PAIRINGS")
    pr(f"{'='*70}")

    SAMPLE_SIZE = 500_000
    rng = np.random.default_rng(42)

    pr(f"\n  Sampling {SAMPLE_SIZE:,} equivariant pairings...")
    t0 = time.time()

    strengths = np.empty(SAMPLE_SIZE, dtype=np.int32)
    diversities = np.empty(SAMPLE_SIZE, dtype=np.float64)
    weight_tilts = np.empty(SAMPLE_SIZE, dtype=np.float64)
    weight_corrs = np.empty(SAMPLE_SIZE, dtype=np.float64)

    n_pal_cfgs = len(pal_configs)
    n_cr_cfgs = len(cr_configs)

    for i in range(SAMPLE_SIZE):
        # Random size-2 configs (uniform over 25 × 25 = 625)
        pal_cfg = pal_configs[rng.integers(n_pal_cfgs)]
        cr_cfg = cr_configs[rng.integers(n_cr_cfgs)]

        # Random size-4 config (weighted uniform)
        big_cfg = sample_size4_config(big_orbits, rng)

        # Combine
        all_pairs = pal_cfg + cr_cfg + big_cfg
        assert len(all_pairs) == NUM_PAIRS, f"Got {len(all_pairs)} pairs"

        s, d, wt, wc = compute_measures(all_pairs)
        strengths[i] = s
        diversities[i] = d
        weight_tilts[i] = wt
        weight_corrs[i] = wc

        if (i + 1) % 100_000 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            pr(f"    {i+1:>8,} / {SAMPLE_SIZE:,} ({rate:.0f}/s)")

    t_sample = time.time() - t0
    pr(f"  Sampling complete: {t_sample:.1f}s")

    # ── Sample statistics ──
    pr(f"\n{'='*70}")
    pr("EQUIVARIANT SAMPLE STATISTICS")
    pr(f"{'='*70}")

    for name, arr in [("Strength", strengths), ("Diversity", diversities),
                      ("Weight Tilt", weight_tilts), ("Weight Corr", weight_corrs)]:
        pr(f"\n  {name}:")
        pr(f"    range: [{arr.min():.4f}, {arr.max():.4f}]")
        pr(f"    mean:  {arr.mean():.4f}  std: {arr.std():.4f}")

    # Strength distribution
    pr(f"\n  Strength distribution:")
    s_vals, s_counts = np.unique(strengths, return_counts=True)
    for v, c in zip(s_vals, s_counts):
        bar = '█' * max(1, int(40 * c / s_counts.max()))
        pr(f"    S={v:3d}: {c:>7,} ({100*c/SAMPLE_SIZE:.2f}%) {bar}")

    # Diversity distribution at key S levels
    pr(f"\n  D distribution at high-S levels:")
    for s_thresh in sorted(set(strengths), reverse=True)[:10]:
        mask = strengths == s_thresh
        n = mask.sum()
        if n > 0:
            pr(f"    S={s_thresh:3d}: n={n:>7,}, "
               f"D=[{diversities[mask].min():.4f}, {diversities[mask].max():.4f}], "
               f"mean={diversities[mask].mean():.4f}")

    # ── KW position ──
    pr(f"\n{'='*70}")
    pr("KW POSITION IN EQUIVARIANT DISTRIBUTION")
    pr(f"{'='*70}")

    for name, kw_val, arr in [
        ("Strength", kw_s, strengths),
        ("Diversity", kw_d, diversities),
        ("Weight Tilt", kw_wt, weight_tilts),
        ("Weight Corr", kw_wc, weight_corrs),
    ]:
        pct = 100 * np.mean(arr <= kw_val)
        exceed = np.sum(arr > kw_val)
        pr(f"  {name:<15}: KW={kw_val:>10.4f}  percentile={pct:>6.2f}%  "
           f"exceeds KW: {exceed:,}")

    pr(f"\n  Pairings with S >= {kw_s}: {np.sum(strengths >= kw_s):,} "
       f"({100*np.mean(strengths >= kw_s):.2f}%)")
    pr(f"  Pairings with S >= {kw_s} AND D >= {kw_d}: "
       f"{np.sum((strengths >= kw_s) & (diversities >= kw_d)):,}")

    # ── Dominance analysis ──
    pr(f"\n  Dominates KW (S > {kw_s} AND D > {kw_d:.4f}): "
       f"{np.sum((strengths > kw_s) & (diversities > kw_d)):,}")
    pr(f"  Weakly dominates KW: "
       f"{np.sum(((strengths > kw_s) & (diversities >= kw_d)) | ((strengths >= kw_s) & (diversities > kw_d))):,}")

    # ── Pareto frontier ──
    pr(f"\n{'='*70}")
    pr("2D PARETO FRONTIER (S, D) — EQUIVARIANT")
    pr(f"{'='*70}")

    # Find Pareto-optimal (S, D) from the sample
    sd_pairs = list(zip(strengths.tolist(), [round(d, 6) for d in diversities.tolist()]))
    unique_sd = sorted(set(sd_pairs), key=lambda x: (-x[0], -x[1]))

    pareto = []
    max_d_seen = -1.0
    for s, d in unique_sd:
        if d > max_d_seen:
            pareto.append((s, d))
            max_d_seen = d

    pr(f"\n  Pareto-optimal (S, D) levels from sample:")
    kw_on_pareto = False
    for s, d in pareto:
        n = sum(1 for ss, dd in sd_pairs if ss == s and dd == d)
        tag = ""
        if s == kw_s and abs(d - kw_d) < 0.0001:
            tag = " ← KW"
            kw_on_pareto = True
        if s == comp_s and abs(d - comp_d) < 0.0001:
            tag += " ← COMP"
        pr(f"    S={s:3d}, D={d:.6f} ({n:>6,} samples){tag}")

    pr(f"\n  KW on equivariant Pareto frontier: {kw_on_pareto}")

    # ── Inter-measure correlations within equivariant set ──
    pr(f"\n{'='*70}")
    pr("INTER-MEASURE CORRELATIONS (equivariant)")
    pr(f"{'='*70}")

    for n1, a1, n2, a2 in [
        ("S", strengths.astype(float), "D", diversities),
        ("S", strengths.astype(float), "WT", weight_tilts),
        ("S", strengths.astype(float), "WC", weight_corrs),
        ("D", diversities, "WT", weight_tilts),
        ("D", diversities, "WC", weight_corrs),
        ("WT", weight_tilts, "WC", weight_corrs),
    ]:
        r = np.corrcoef(a1, a2)[0, 1]
        pr(f"  {n1:>3} ↔ {n2:<3}: r = {r:+.6f}")

    # ── Compare with random distribution ──
    pr(f"\n{'='*70}")
    pr("EQUIVARIANT vs RANDOM DISTRIBUTION")
    pr(f"{'='*70}")

    sample_path = Path(__file__).parent.parent / 'n6' / 'sample_measures.npz'
    if sample_path.exists():
        data = np.load(sample_path)
        rand_s = data['strengths']
        rand_d = data['diversities']

        pr(f"\n  {'':>20} {'Equivariant':>15} {'Random':>15}")
        pr(f"  {'S mean':>20} {strengths.mean():>15.2f} {rand_s.mean():>15.2f}")
        pr(f"  {'S std':>20} {strengths.std():>15.2f} {rand_s.std():>15.2f}")
        pr(f"  {'S range':>20} {f'[{strengths.min()},{strengths.max()}]':>15} {f'[{rand_s.min()},{rand_s.max()}]':>15}")
        pr(f"  {'D mean':>20} {diversities.mean():>15.4f} {rand_d.mean():>15.4f}")
        pr(f"  {'D std':>20} {diversities.std():>15.4f} {rand_d.std():>15.4f}")
        pr(f"  {'D range':>20} {f'[{diversities.min():.3f},{diversities.max():.3f}]':>15} "
           f"{f'[{rand_d.min():.3f},{rand_d.max():.3f}]':>15}")

    # ── Summary ──
    pr(f"\n{'='*70}")
    pr("SUMMARY")
    pr(f"{'='*70}")

    pr(f"\n  Total Z₂²-equivariant pairings: {total_eq:,}")
    pr(f"    = {n_pal} (pal) × {n_cr} (cr) × {n_big:,} (size-4)")
    pr(f"  Sample size: {SAMPLE_SIZE:,}")
    pr(f"  S range (sampled): [{strengths.min()}, {strengths.max()}]")
    pr(f"  D range (sampled): [{diversities.min():.6f}, {diversities.max():.6f}]")
    pr(f"\n  KW: S={kw_s}, D={kw_d:.6f}")
    pr(f"  Complement: S={comp_s}, D={comp_d:.6f}")
    pr(f"  KW on equivariant Pareto (S,D): {kw_on_pareto}")
    pr(f"  KW S-percentile among equivariant: "
       f"{100*np.mean(strengths <= kw_s):.2f}%")
    pr(f"  KW D-percentile among equivariant: "
       f"{100*np.mean(diversities <= kw_d):.2f}%")

    # ── Key finding ──
    s_exceed = np.sum(strengths > kw_s)
    d_exceed = np.sum(diversities > kw_d)
    both_exceed = np.sum((strengths > kw_s) & (diversities > kw_d))
    pr(f"\n  KEY FINDINGS:")
    pr(f"  - Complement is unique S-maximizer: {np.sum(strengths >= comp_s) == np.sum(strengths == comp_s)}")
    pr(f"  - Fraction with S > KW: {100*s_exceed/SAMPLE_SIZE:.2f}%")
    pr(f"  - Fraction with D > KW: {100*d_exceed/SAMPLE_SIZE:.2f}%")
    pr(f"  - Fraction dominating KW on both S and D: {100*both_exceed/SAMPLE_SIZE:.4f}%")

    # ── Save ──
    md_path = out_dir / 'n6_equivariant_results.md'
    with open(md_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    pr(f"\nSaved to {md_path}")

    # Save sample data
    np.savez_compressed(out_dir / 'n6_eq_sample.npz',
        strengths=strengths, diversities=diversities,
        weight_tilts=weight_tilts, weight_corrs=weight_corrs)


if __name__ == '__main__':
    main()
