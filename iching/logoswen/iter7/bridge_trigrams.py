"""
Round 2: Bridge trigram analysis — the 9 preserving bridges and the continuity gradient.

Tasks:
  A. Meaning characterization of 9 preserving bridges (data support)
  B. Continuity gradient for all 31 bridges
  C. Statistical significance tests
  D. Cross-tabulation: bridge trigrams × algebraic properties
  E. Cross-tabulation: bridge trigrams × meaning confidence
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, TRIGRAMS

RNG = np.random.default_rng(42)
N_TRIALS = 100_000

# ── Trigram constants ────────────────────────────────────────────────────────

TRIGRAM_INFO = {
    "111": ("Qian",  "☰", "Heaven",  "Father",           "Creative"),
    "000": ("Kun",   "☷", "Earth",   "Mother",            "Receptive"),
    "100": ("Zhen",  "☳", "Thunder", "Eldest Son",        "Arousing"),
    "010": ("Kan",   "☵", "Water",   "Middle Son",        "Abysmal"),
    "001": ("Gen",   "☶", "Mountain","Youngest Son",       "Keeping Still"),
    "011": ("Xun",   "☴", "Wind",    "Eldest Daughter",   "Gentle"),
    "101": ("Li",    "☲", "Fire",    "Middle Daughter",   "Clinging"),
    "110": ("Dui",   "☱", "Lake",    "Youngest Daughter", "Joyous"),
}

GEN_SIGNATURES = {
    (0,0,0): "id", (1,0,0): "O", (0,1,0): "M", (0,0,1): "I",
    (1,1,0): "OM", (1,0,1): "OI", (0,1,1): "MI", (1,1,1): "OMI",
}

# Mirror-pair generators: which bits they flip (0-indexed)
GENERATORS = {
    "id": [], "O": [0,5], "M": [1,4], "I": [2,3],
    "OM": [0,1,4,5], "OI": [0,2,3,5], "MI": [1,2,3,4], "OMI": [0,1,2,3,4,5],
}


# ── Utility ──────────────────────────────────────────────────────────────────

def tri_name(s): return TRIGRAM_INFO.get(s, ("?",))[0]
def tri_sym(s): return TRIGRAM_INFO.get(s, ("?","?"))[1]
def bits(idx): return [int(b) for b in KING_WEN[idx][2]]
def xor_sig(h): return (h[0]^h[5], h[1]^h[4], h[2]^h[3])

def hamming3(a, b):
    """Hamming distance between two 3-char strings."""
    return sum(c1 != c2 for c1, c2 in zip(a, b))

def kernel_dressing(xor_mask):
    """Decompose a 6-bit XOR mask into kernel (palindromic) and orbit-delta components.
    Kernel generators: for each mirror pair, if BOTH bits flip, that generator is in the kernel.
    The orbit delta is the remaining asymmetric flips."""
    # Mirror pairs: (0,5), (1,4), (2,3)
    kernel = []
    orbit_delta = []
    labels = ['O', 'M', 'I']
    for i, (a, b) in enumerate([(0,5), (1,4), (2,3)]):
        if xor_mask[a] == 1 and xor_mask[b] == 1:
            kernel.append(labels[i])
        else:
            if xor_mask[a] == 1: orbit_delta.append(f'L{a+1}')
            if xor_mask[b] == 1: orbit_delta.append(f'L{b+1}')
    k_str = ''.join(kernel) if kernel else 'id'
    d_str = '+'.join(orbit_delta) if orbit_delta else 'none'
    return k_str, d_str

def s_value(pair_idx):
    """Compute S-value for a pair (number of axes that improve when flipping)."""
    # S = number of distributional axes where the reversed orientation scores better
    # From the investigation: S=0 means KW dominates on all axes
    # We approximate: S is related to the kernel dressing
    # Actually, let's compute it properly from the pair mask
    a = bits(2 * pair_idx)
    b = bits(2 * pair_idx + 1)
    xor = tuple(a[i] ^ b[i] for i in range(6))
    sig = xor_sig(a)
    return sig  # Return orbit signature; actual S needs more infrastructure


# ── Build bridge data ────────────────────────────────────────────────────────

def build_bridges():
    """Build all 31 bridges with trigram decomposition."""
    bridges = []
    for k in range(31):
        exit_idx = 2*k + 1    # second hex of pair k
        entry_idx = 2*k + 2   # first hex of pair k+1

        exit_bin = KING_WEN[exit_idx][2]
        entry_bin = KING_WEN[entry_idx][2]

        exit_lo, exit_up = exit_bin[:3], exit_bin[3:]
        entry_lo, entry_up = entry_bin[:3], entry_bin[3:]

        lo_dist = hamming3(exit_lo, entry_lo)
        up_dist = hamming3(exit_up, entry_up)
        total_dist = lo_dist + up_dist

        # XOR mask
        xor = tuple(int(exit_bin[i]) ^ int(entry_bin[i]) for i in range(6))
        k_dress, o_delta = kernel_dressing(xor)

        # Exit pair's orbit signature and entry pair's
        exit_pair_first = bits(2*k)
        entry_pair_first = bits(2*(k+1))
        exit_orbit = GEN_SIGNATURES.get(xor_sig(exit_pair_first), "?")
        entry_orbit = GEN_SIGNATURES.get(xor_sig(entry_pair_first), "?")

        bridges.append({
            'k': k,           # bridge index (0-based)
            'b_num': k + 1,   # bridge number (1-based)
            'exit_idx': exit_idx,
            'entry_idx': entry_idx,
            'exit_num': KING_WEN[exit_idx][0],
            'entry_num': KING_WEN[entry_idx][0],
            'exit_name': KING_WEN[exit_idx][1],
            'entry_name': KING_WEN[entry_idx][1],
            'exit_lo': exit_lo,
            'exit_up': exit_up,
            'entry_lo': entry_lo,
            'entry_up': entry_up,
            'lo_dist': lo_dist,
            'up_dist': up_dist,
            'total_dist': total_dist,
            'min_dist': min(lo_dist, up_dist),
            'lo_shared': (lo_dist == 0),
            'up_shared': (up_dist == 0),
            'xor': xor,
            'kernel_dressing': k_dress,
            'orbit_delta': o_delta,
            'hamming': sum(xor),
            'exit_orbit': exit_orbit,
            'entry_orbit': entry_orbit,
        })
    return bridges


# ══════════════════════════════════════════════════════════════════════════════
# TASK A: Meaning characterization support data
# ══════════════════════════════════════════════════════════════════════════════

def task_a(bridges):
    print("=" * 90)
    print("TASK A: THE 9 PRESERVING BRIDGES — TRIGRAM DATA")
    print("=" * 90)

    preserving = [b for b in bridges if b['lo_shared'] or b['up_shared']]

    for b in preserving:
        which = "LOWER" if b['lo_shared'] else "UPPER"
        preserved = b['exit_lo'] if b['lo_shared'] else b['exit_up']
        changed_from = b['exit_up'] if b['lo_shared'] else b['exit_lo']
        changed_to = b['entry_up'] if b['lo_shared'] else b['entry_lo']

        print(f"\n  B{b['b_num']:2d}: #{b['exit_num']} {b['exit_name']:12s} → "
              f"#{b['entry_num']} {b['entry_name']:12s}")
        print(f"       Exit: {tri_name(b['exit_lo']):>8s}{tri_sym(b['exit_lo'])} / "
              f"{tri_name(b['exit_up']):>8s}{tri_sym(b['exit_up'])}")
        print(f"       Entry: {tri_name(b['entry_lo']):>8s}{tri_sym(b['entry_lo'])} / "
              f"{tri_name(b['entry_up']):>8s}{tri_sym(b['entry_up'])}")
        print(f"       Preserved: {which} = {tri_name(preserved)}{tri_sym(preserved)} "
              f"({TRIGRAM_INFO[preserved][2]}, {TRIGRAM_INFO[preserved][3]}, "
              f"{TRIGRAM_INFO[preserved][4]})")
        print(f"       Changed: {tri_name(changed_from)}{tri_sym(changed_from)} → "
              f"{tri_name(changed_to)}{tri_sym(changed_to)}")

        # Context: which pairs does this bridge connect?
        exit_pair = b['k']  # 0-indexed
        entry_pair = b['k'] + 1
        ep_first = KING_WEN[2*exit_pair]
        ep_second = KING_WEN[2*exit_pair+1]
        np_first = KING_WEN[2*entry_pair]
        np_second = KING_WEN[2*entry_pair+1]
        print(f"       Connects: Pair {exit_pair+1} ({ep_first[1]}/{ep_second[1]}) → "
              f"Pair {entry_pair+1} ({np_first[1]}/{np_second[1]})")

    # Summary of which trigrams are preserved
    print(f"\n  --- Summary of preserved trigrams ---")
    lo_preserved = [b for b in preserving if b['lo_shared']]
    up_preserved = [b for b in preserving if b['up_shared']]

    print(f"  Lower preserved ({len(lo_preserved)} bridges):")
    for b in lo_preserved:
        t = b['exit_lo']
        print(f"    B{b['b_num']:2d}: {tri_name(t):>8s}{tri_sym(t)} "
              f"({TRIGRAM_INFO[t][2]}, {TRIGRAM_INFO[t][3]})")

    print(f"  Upper preserved ({len(up_preserved)} bridges):")
    for b in up_preserved:
        t = b['exit_up']
        print(f"    B{b['b_num']:2d}: {tri_name(t):>8s}{tri_sym(t)} "
              f"({TRIGRAM_INFO[t][2]}, {TRIGRAM_INFO[t][3]})")

    # Which trigrams appear?
    lo_tris = Counter(tri_name(b['exit_lo']) for b in lo_preserved)
    up_tris = Counter(tri_name(b['exit_up']) for b in up_preserved)
    print(f"\n  Lower preserved trigram frequency: {dict(lo_tris)}")
    print(f"  Upper preserved trigram frequency: {dict(up_tris)}")
    all_tris = Counter()
    for b in lo_preserved: all_tris[tri_name(b['exit_lo'])] += 1
    for b in up_preserved: all_tris[tri_name(b['exit_up'])] += 1
    print(f"  Combined: {dict(all_tris)}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK B: Continuity gradient
# ══════════════════════════════════════════════════════════════════════════════

def task_b(bridges):
    print("\n" + "=" * 90)
    print("TASK B: THE CONTINUITY GRADIENT — ALL 31 BRIDGES")
    print("=" * 90)

    # Sort by total displacement
    sorted_bridges = sorted(bridges, key=lambda b: (b['total_dist'], b['min_dist']))

    print(f"\n  {'B':>3s}  {'Exit':>4s}→{'Entry':>4s}  {'Exit Lo':>8s} {'Exit Up':>8s} → "
          f"{'Entry Lo':>8s} {'Entry Up':>8s}  "
          f"{'Lo Δ':>4s} {'Up Δ':>4s} {'Tot':>4s} {'Min':>4s}  "
          f"{'Shared':>10s}")
    print("  " + "-" * 105)

    for b in sorted_bridges:
        shared = ""
        if b['lo_shared']: shared = f"LO={tri_name(b['exit_lo'])}"
        elif b['up_shared']: shared = f"UP={tri_name(b['exit_up'])}"

        print(f"  {b['b_num']:3d}  {b['exit_num']:4d}→{b['entry_num']:4d}  "
              f"{tri_name(b['exit_lo']):>8s} {tri_name(b['exit_up']):>8s} → "
              f"{tri_name(b['entry_lo']):>8s} {tri_name(b['entry_up']):>8s}  "
              f"{b['lo_dist']:4d} {b['up_dist']:4d} {b['total_dist']:4d} {b['min_dist']:4d}  "
              f"{shared:>10s}")

    # Distribution statistics
    print(f"\n  --- Displacement Distribution ---")
    total_dist_counter = Counter(b['total_dist'] for b in bridges)
    min_dist_counter = Counter(b['min_dist'] for b in bridges)
    lo_dist_counter = Counter(b['lo_dist'] for b in bridges)
    up_dist_counter = Counter(b['up_dist'] for b in bridges)

    print(f"  Total displacement: {dict(sorted(total_dist_counter.items()))}")
    print(f"  Min displacement:   {dict(sorted(min_dist_counter.items()))}")
    print(f"  Lower Hamming:      {dict(sorted(lo_dist_counter.items()))}")
    print(f"  Upper Hamming:      {dict(sorted(up_dist_counter.items()))}")

    mean_total = np.mean([b['total_dist'] for b in bridges])
    mean_lo = np.mean([b['lo_dist'] for b in bridges])
    mean_up = np.mean([b['up_dist'] for b in bridges])
    print(f"\n  Mean total displacement: {mean_total:.3f}")
    print(f"  Mean lower Hamming:      {mean_lo:.3f}")
    print(f"  Mean upper Hamming:      {mean_up:.3f}")

    # Near-preserving: min_dist = 1
    near_preserving = [b for b in bridges if b['min_dist'] == 1]
    print(f"\n  Near-preserving bridges (min_dist = 1): {len(near_preserving)}/31")
    for b in near_preserving:
        lo_or_up = "lo≈" if b['lo_dist'] == 1 and b['up_dist'] > 1 else (
            "up≈" if b['up_dist'] == 1 and b['lo_dist'] > 1 else "both≈1")
        print(f"    B{b['b_num']:2d}: lo_dist={b['lo_dist']} up_dist={b['up_dist']} {lo_or_up}")

    # Gaps in the distribution
    print(f"\n  Gradient structure:")
    for t in range(7):
        count = total_dist_counter.get(t, 0)
        bar = "█" * count
        print(f"    total_dist={t}: {count:2d} {bar}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK C: Statistical significance
# ══════════════════════════════════════════════════════════════════════════════

def task_c(bridges):
    print("\n" + "=" * 90)
    print("TASK C: STATISTICAL SIGNIFICANCE")
    print("=" * 90)

    kw_preserving = sum(1 for b in bridges if b['min_dist'] == 0)
    kw_mean_total = np.mean([b['total_dist'] for b in bridges])

    # Build pair data for simulation
    pair_data = []
    for k in range(32):
        a = KING_WEN[2*k][2]
        b = KING_WEN[2*k+1][2]
        pair_data.append((a, b))

    # ── Test 1: Random pair orderings ──
    print(f"\n  --- Test 1: Random pair orderings ({N_TRIALS} trials) ---")
    print(f"  (Preserve pairing and internal orientation, shuffle pair order)")

    null_preserving = []
    null_mean_total = []

    for _ in range(N_TRIALS):
        perm = RNG.permutation(32)
        shuffled = [pair_data[i] for i in perm]

        pres_count = 0
        total_disps = []
        for j in range(31):
            exit_hex = shuffled[j][1]  # second hex of pair j
            entry_hex = shuffled[j+1][0]  # first hex of pair j+1
            lo_d = hamming3(exit_hex[:3], entry_hex[:3])
            up_d = hamming3(exit_hex[3:], entry_hex[3:])
            if lo_d == 0 or up_d == 0:
                pres_count += 1
            total_disps.append(lo_d + up_d)

        null_preserving.append(pres_count)
        null_mean_total.append(np.mean(total_disps))

    null_preserving = np.array(null_preserving)
    null_mean_total = np.array(null_mean_total)

    pct_pres = np.mean(null_preserving >= kw_preserving) * 100
    p_pres = np.mean(null_preserving >= kw_preserving)
    pct_total = np.mean(null_mean_total <= kw_mean_total) * 100
    p_total = np.mean(null_mean_total <= kw_mean_total)

    print(f"  KW preserving bridges: {kw_preserving}")
    print(f"  Null mean: {np.mean(null_preserving):.2f} ± {np.std(null_preserving):.2f}")
    print(f"  Null range: [{null_preserving.min()}, {null_preserving.max()}]")
    print(f"  p(≥{kw_preserving}): {p_pres:.4f}  (KW percentile: {100-pct_pres:.1f}%)")
    print(f"  Distribution: {dict(sorted(Counter(null_preserving).items()))}")

    print(f"\n  KW mean total displacement: {kw_mean_total:.3f}")
    print(f"  Null mean: {np.mean(null_mean_total):.3f} ± {np.std(null_mean_total):.3f}")
    print(f"  p(≤{kw_mean_total:.3f}): {p_total:.4f}")

    # ── Test 2: Random orientations (same pair ordering) ──
    print(f"\n  --- Test 2: Random orientations, same pair ordering ({N_TRIALS} trials) ---")
    print(f"  (Preserve pair order, randomly flip orientation within each pair)")

    # Identify S2 pairs (those that can't be flipped)
    # S2 pairs: where orbit sig = id (complement pairs) are self-reversing,
    # so flipping them changes the sequence. Actually S2 constraint is more nuanced.
    # S2 pairs from alignment-map: pairs 14,15,21,27,29,31 (1-indexed)
    s2_pair_indices = {13, 14, 20, 26, 28, 30}  # 0-indexed

    null_pres_orient = []
    null_mean_orient = []

    for _ in range(N_TRIALS):
        flipped = []
        for k in range(32):
            a, b = pair_data[k]
            if k in s2_pair_indices:
                # S2-constrained: keep as is
                flipped.append((a, b))
            else:
                # Randomly flip
                if RNG.random() < 0.5:
                    flipped.append((b, a))
                else:
                    flipped.append((a, b))

        pres_count = 0
        total_disps = []
        for j in range(31):
            exit_hex = flipped[j][1]
            entry_hex = flipped[j+1][0]
            lo_d = hamming3(exit_hex[:3], entry_hex[:3])
            up_d = hamming3(exit_hex[3:], entry_hex[3:])
            if lo_d == 0 or up_d == 0:
                pres_count += 1
            total_disps.append(lo_d + up_d)

        null_pres_orient.append(pres_count)
        null_mean_orient.append(np.mean(total_disps))

    null_pres_orient = np.array(null_pres_orient)
    null_mean_orient = np.array(null_mean_orient)

    pct2 = np.mean(null_pres_orient >= kw_preserving) * 100
    p2 = np.mean(null_pres_orient >= kw_preserving)

    print(f"  KW preserving bridges: {kw_preserving}")
    print(f"  Null mean: {np.mean(null_pres_orient):.2f} ± {np.std(null_pres_orient):.2f}")
    print(f"  p(≥{kw_preserving}): {p2:.4f}")
    print(f"  Distribution: {dict(sorted(Counter(null_pres_orient).items()))}")

    p2_total = np.mean(null_mean_orient <= kw_mean_total)
    print(f"\n  KW mean total displacement: {kw_mean_total:.3f}")
    print(f"  Null mean: {np.mean(null_mean_orient):.3f} ± {np.std(null_mean_orient):.3f}")
    print(f"  p(≤{kw_mean_total:.3f}): {p2_total:.4f}")

    # ── Test 3: Which-trigram distribution ──
    print(f"\n  --- Test 3: Which trigrams are preserved ---")
    preserved_trigrams = []
    for b in bridges:
        if b['lo_shared']:
            preserved_trigrams.append(('lower', tri_name(b['exit_lo'])))
        elif b['up_shared']:
            preserved_trigrams.append(('upper', tri_name(b['exit_up'])))

    all_preserved = [t[1] for t in preserved_trigrams]
    print(f"  Preserved trigram identities: {all_preserved}")
    print(f"  Frequency: {dict(Counter(all_preserved))}")

    # Under random pair orderings, which trigrams get preserved?
    null_tri_counts = defaultdict(list)
    for _ in range(min(N_TRIALS, 10000)):
        perm = RNG.permutation(32)
        shuffled = [pair_data[i] for i in perm]
        tri_counter = Counter()
        for j in range(31):
            exit_hex = shuffled[j][1]
            entry_hex = shuffled[j+1][0]
            if exit_hex[:3] == entry_hex[:3]:
                tri_counter[tri_name(exit_hex[:3])] += 1
            if exit_hex[3:] == entry_hex[3:]:
                tri_counter[tri_name(exit_hex[3:])] += 1
        for tn in ["Qian", "Kun", "Zhen", "Kan", "Gen", "Xun", "Li", "Dui"]:
            null_tri_counts[tn].append(tri_counter.get(tn, 0))

    print(f"\n  Trigram preservation frequency (KW vs random ordering):")
    kw_tri_freq = Counter(all_preserved)
    for tn in ["Qian", "Kun", "Zhen", "Kan", "Gen", "Xun", "Li", "Dui"]:
        kw_count = kw_tri_freq.get(tn, 0)
        null_arr = np.array(null_tri_counts[tn])
        null_mean = np.mean(null_arr)
        p_val = np.mean(null_arr >= kw_count) if kw_count > 0 else 1.0
        print(f"    {tn:>8s}: KW={kw_count}, null_mean={null_mean:.2f}, p(≥KW)={p_val:.4f}")

    # ── Test 4: Position clustering ──
    print(f"\n  --- Test 4: Position of preserving bridges ---")
    pres_positions = [b['b_num'] for b in bridges if b['min_dist'] == 0]
    print(f"  Preserving bridge positions: {pres_positions}")
    gaps = [pres_positions[i+1] - pres_positions[i] for i in range(len(pres_positions)-1)]
    print(f"  Gaps between consecutive preserving bridges: {gaps}")
    print(f"  Mean gap: {np.mean(gaps):.1f}")
    print(f"  In upper canon (B1-B15): {sum(1 for p in pres_positions if p <= 15)}")
    print(f"  In lower canon (B16-B31): {sum(1 for p in pres_positions if p > 15)}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK D: Bridge trigrams × algebraic properties
# ══════════════════════════════════════════════════════════════════════════════

def task_d(bridges):
    print("\n" + "=" * 90)
    print("TASK D: BRIDGE TRIGRAMS × ALGEBRAIC PROPERTIES")
    print("=" * 90)

    # Full table
    print(f"\n  {'B':>3s}  {'Exit→Entry':>14s}  "
          f"{'Lo Δ':>4s} {'Up Δ':>4s} {'Tot':>4s}  "
          f"{'Lo?':>3s} {'Up?':>3s}  "
          f"{'Kernel':>6s}  {'Orb Δ':>10s}  "
          f"{'H':>2s}  "
          f"{'Exit orb':>8s} {'Entry orb':>9s}")
    print("  " + "-" * 100)

    for b in bridges:
        lo_sh = "✓" if b['lo_shared'] else " "
        up_sh = "✓" if b['up_shared'] else " "

        print(f"  {b['b_num']:3d}  {b['exit_num']:4d}→{b['entry_num']:4d}      "
              f"{b['lo_dist']:4d} {b['up_dist']:4d} {b['total_dist']:4d}  "
              f"{lo_sh:>3s} {up_sh:>3s}  "
              f"{b['kernel_dressing']:>6s}  {b['orbit_delta']:>10s}  "
              f"{b['hamming']:2d}  "
              f"{b['exit_orbit']:>8s} {b['entry_orbit']:>9s}")

    # Cross-tabulation: preserving vs kernel dressing
    print(f"\n  --- Kernel dressing × trigram preservation ---")
    preserving = [b for b in bridges if b['min_dist'] == 0]
    non_preserving = [b for b in bridges if b['min_dist'] > 0]

    pres_kernels = Counter(b['kernel_dressing'] for b in preserving)
    nonpres_kernels = Counter(b['kernel_dressing'] for b in non_preserving)
    all_kernels = sorted(set(b['kernel_dressing'] for b in bridges))

    print(f"  {'Kernel':>8s}  {'Preserving':>10s}  {'Non-pres':>10s}  {'Total':>6s}")
    for k in all_kernels:
        p = pres_kernels.get(k, 0)
        n = nonpres_kernels.get(k, 0)
        print(f"  {k:>8s}  {p:>10d}  {n:>10d}  {p+n:>6d}")

    # Which trigram preserved × kernel dressing
    print(f"\n  --- Which trigram preserved × kernel dressing ---")
    lo_kernels = Counter(b['kernel_dressing'] for b in preserving if b['lo_shared'])
    up_kernels = Counter(b['kernel_dressing'] for b in preserving if b['up_shared'])
    print(f"  Lower preserved: {dict(lo_kernels)}")
    print(f"  Upper preserved: {dict(up_kernels)}")

    # Preserving vs Hamming distance
    print(f"\n  --- Preservation × total Hamming distance ---")
    pres_h = Counter(b['hamming'] for b in preserving)
    nonpres_h = Counter(b['hamming'] for b in non_preserving)
    print(f"  Preserving Hamming: {dict(sorted(pres_h.items()))}")
    print(f"  Non-preserving Hamming: {dict(sorted(nonpres_h.items()))}")

    # Orbit transitions at preserving bridges
    print(f"\n  --- Orbit transitions at preserving bridges ---")
    for b in preserving:
        print(f"    B{b['b_num']:2d}: {b['exit_orbit']:>4s} → {b['entry_orbit']:>4s}  "
              f"kernel={b['kernel_dressing']}")

    # kac contribution analysis
    print(f"\n  --- kac contribution: preserving vs non-preserving ---")
    # kac = kernel autocorrelation at offset 1
    # At each bridge, the kernel dressing represents the palindromic structure
    # We can measure the correlation between consecutive bridge kernel dressings
    # But actually kac is about pair-level kernel, not bridge-level

    # Instead: for the pairs adjacent to preserving bridges, compute their
    # kernel (pair mask) properties
    print(f"\n  Pairs adjacent to preserving bridges:")
    for b in preserving:
        exit_pair = b['k']
        entry_pair = b['k'] + 1
        a1 = bits(2*exit_pair)
        b1 = bits(2*exit_pair+1)
        xor1 = tuple(a1[i]^b1[i] for i in range(6))
        k1, _ = kernel_dressing(xor1)

        a2 = bits(2*entry_pair)
        b2 = bits(2*entry_pair+1)
        xor2 = tuple(a2[i]^b2[i] for i in range(6))
        k2, _ = kernel_dressing(xor2)

        match = "MATCH" if k1 == k2 else ""
        print(f"    B{b['b_num']:2d}: pair {exit_pair+1} kernel={k1:>4s} → "
              f"pair {entry_pair+1} kernel={k2:>4s}  {match}")


# ══════════════════════════════════════════════════════════════════════════════
# TASK E: Bridge trigrams × meaning confidence
# ══════════════════════════════════════════════════════════════════════════════

def task_e(bridges):
    print("\n" + "=" * 90)
    print("TASK E: BRIDGE TRIGRAMS × MEANING CONFIDENCE")
    print("=" * 90)

    # Meaning confidence from iter6 alignment-map.md (1-indexed pair numbers)
    meaning_conf = {
        1: 'Clear', 2: 'Clear', 3: 'Suggestive', 4: 'Clear', 5: 'Suggestive',
        6: 'Clear', 7: 'Clear', 8: 'Clear', 9: 'Clear', 10: 'Clear',
        11: 'Suggestive', 12: 'Clear', 13: 'Suggestive', 14: 'Suggestive',
        15: 'Suggestive', 16: 'Clear', 17: 'Suggestive', 18: 'Clear',
        19: 'Clear', 20: 'Clear', 21: 'Clear', 22: 'Clear',
        23: 'Clear', 24: 'Suggestive', 25: 'Clear', 26: 'Clear',
        27: 'Suggestive', 28: 'Clear', 29: 'Suggestive', 30: 'Clear',
        31: 'Suggestive', 32: 'Clear',
    }

    # M-type from alignment map
    m_type = {
        1: 'complement', 2: 'conform', 3: 'non-dec', 4: 'excep', 5: 'non-dec',
        6: 'excep', 7: 'conform', 8: 'non-dec', 9: 'non-dec', 10: 'excep',
        11: 'non-dec', 12: 'non-dec', 13: 'conform', 14: 'complement',
        15: 'complement', 16: 'conform', 17: 'conform', 18: 'non-dec',
        19: 'conform', 20: 'conform', 21: 'excep', 22: 'non-dec',
        23: 'conform', 24: 'non-dec', 25: 'conform', 26: 'non-dec',
        27: 'conform', 28: 'non-dec', 29: 'non-dec', 30: 'non-dec',
        31: 'complement', 32: 'complement',
    }

    # Fragility class (0-indexed pair)
    s2_pairs = {13, 14, 20, 26, 28, 30}  # 0-indexed
    kw_dom_bits = [0,1,2,4,7,8,13,18,19,22,25]  # free bit indices
    free_pairs = [i for i in range(32) if i not in s2_pairs]
    kw_dom_pairs = set()
    tradeoff_pairs = set()
    for bit_idx, pair_idx in enumerate(free_pairs):
        if bit_idx in kw_dom_bits:
            kw_dom_pairs.add(pair_idx)
        else:
            tradeoff_pairs.add(pair_idx)

    def fragility(pair_0idx):
        if pair_0idx in s2_pairs: return 'S2'
        if pair_0idx in kw_dom_pairs: return 'KW-dom'
        return 'trade-off'

    # Full table
    print(f"\n  {'B':>3s}  {'ExitP':>5s}→{'EntryP':>6s}  "
          f"{'Lo Δ':>4s} {'Up Δ':>4s}  "
          f"{'ExConf':>8s} {'EnConf':>8s}  "
          f"{'ExFrag':>9s} {'EnFrag':>9s}  "
          f"{'Shared':>10s}")
    print("  " + "-" * 95)

    for b in bridges:
        exit_pair_1 = b['k'] + 1
        entry_pair_1 = b['k'] + 2
        ex_conf = meaning_conf.get(exit_pair_1, '?')
        en_conf = meaning_conf.get(entry_pair_1, '?')
        ex_frag = fragility(b['k'])
        en_frag = fragility(b['k'] + 1)

        shared = ""
        if b['lo_shared']: shared = f"LO={tri_name(b['exit_lo'])}"
        elif b['up_shared']: shared = f"UP={tri_name(b['exit_up'])}"

        print(f"  {b['b_num']:3d}  P{exit_pair_1:2d}→P{entry_pair_1:2d}      "
              f"{b['lo_dist']:4d} {b['up_dist']:4d}  "
              f"{ex_conf:>8s} {en_conf:>8s}  "
              f"{ex_frag:>9s} {en_frag:>9s}  "
              f"{shared:>10s}")

    # Cross-tabulation: preserving bridges × meaning confidence
    print(f"\n  --- Meaning confidence adjacent to preserving bridges ---")
    preserving = [b for b in bridges if b['min_dist'] == 0]
    non_preserving = [b for b in bridges if b['min_dist'] > 0]

    # For each bridge, count the confidence of adjacent pairs
    def adjacent_confs(bridge_set):
        confs = []
        for b in bridge_set:
            confs.append(meaning_conf.get(b['k'] + 1, '?'))
            confs.append(meaning_conf.get(b['k'] + 2, '?'))
        return Counter(confs)

    pres_confs = adjacent_confs(preserving)
    nonpres_confs = adjacent_confs(non_preserving)

    print(f"  Preserving bridges ({len(preserving)}) — adjacent pairs:")
    print(f"    Clear: {pres_confs.get('Clear', 0)}, Suggestive: {pres_confs.get('Suggestive', 0)}")
    total_p = pres_confs.get('Clear', 0) + pres_confs.get('Suggestive', 0)
    if total_p > 0:
        print(f"    Clear rate: {100*pres_confs.get('Clear', 0)/total_p:.0f}%")

    print(f"  Non-preserving bridges ({len(non_preserving)}) — adjacent pairs:")
    print(f"    Clear: {nonpres_confs.get('Clear', 0)}, Suggestive: {nonpres_confs.get('Suggestive', 0)}")
    total_n = nonpres_confs.get('Clear', 0) + nonpres_confs.get('Suggestive', 0)
    if total_n > 0:
        print(f"    Clear rate: {100*nonpres_confs.get('Clear', 0)/total_n:.0f}%")

    # Cross-tabulation: preserving bridges × fragility
    print(f"\n  --- Fragility class adjacent to preserving bridges ---")
    def adjacent_frags(bridge_set):
        frags = []
        for b in bridge_set:
            frags.append(fragility(b['k']))
            frags.append(fragility(b['k'] + 1))
        return Counter(frags)

    pres_frags = adjacent_frags(preserving)
    nonpres_frags = adjacent_frags(non_preserving)

    print(f"  Preserving bridges — adjacent pair fragility:")
    for f in ['KW-dom', 'trade-off', 'S2']:
        print(f"    {f}: {pres_frags.get(f, 0)}")

    print(f"  Non-preserving bridges — adjacent pair fragility:")
    for f in ['KW-dom', 'trade-off', 'S2']:
        print(f"    {f}: {nonpres_frags.get(f, 0)}")

    # Overall rates
    total_pres = sum(pres_frags.values())
    total_nonpres = sum(nonpres_frags.values())
    if total_pres > 0:
        print(f"\n  Preserving: KW-dom rate = {100*pres_frags.get('KW-dom',0)/total_pres:.0f}%, "
              f"trade-off rate = {100*pres_frags.get('trade-off',0)/total_pres:.0f}%")
    if total_nonpres > 0:
        print(f"  Non-preserving: KW-dom rate = {100*nonpres_frags.get('KW-dom',0)/total_nonpres:.0f}%, "
              f"trade-off rate = {100*nonpres_frags.get('trade-off',0)/total_nonpres:.0f}%")

    # Position × meaning: are preserving bridges between Clear-Clear, Clear-Sugg, etc?
    print(f"\n  --- Preserving bridge confidence pairs ---")
    for b in preserving:
        p1 = b['k'] + 1
        p2 = b['k'] + 2
        c1 = meaning_conf.get(p1, '?')
        c2 = meaning_conf.get(p2, '?')
        shared = "LO" if b['lo_shared'] else "UP"
        tri = tri_name(b['exit_lo'] if b['lo_shared'] else b['exit_up'])
        print(f"    B{b['b_num']:2d}: P{p1}({c1[0]}) → P{p2}({c2[0]})  "
              f"shared={shared}:{tri}")


# ══════════════════════════════════════════════════════════════════════════════
# ADDITIONAL: The 22 non-preserving bridges detail
# ══════════════════════════════════════════════════════════════════════════════

def task_c_nonpreserving(bridges):
    print("\n" + "=" * 90)
    print("THE 22 NON-PRESERVING BRIDGES — TRIGRAM CHANGE DETAIL")
    print("=" * 90)

    non_pres = [b for b in bridges if b['min_dist'] > 0]

    # Which bits change in lower and upper trigram
    print(f"\n  {'B':>3s}  {'Exit→Entry':>14s}  "
          f"{'Lo Δ':>4s} {'Up Δ':>4s}  "
          f"{'Lo bits':>10s}  {'Up bits':>10s}  "
          f"{'Exit Lo':>8s}→{'Entry Lo':>8s}  "
          f"{'Exit Up':>8s}→{'Entry Up':>8s}")
    print("  " + "-" * 110)

    for b in non_pres:
        lo_bits = []
        up_bits = []
        for i in range(3):
            if b['exit_lo'][i] != b['entry_lo'][i]:
                lo_bits.append(f'L{i+1}')
            if b['exit_up'][i] != b['entry_up'][i]:
                up_bits.append(f'L{i+4}')

        print(f"  {b['b_num']:3d}  {b['exit_num']:4d}→{b['entry_num']:4d}      "
              f"{b['lo_dist']:4d} {b['up_dist']:4d}  "
              f"{','.join(lo_bits):>10s}  {','.join(up_bits):>10s}  "
              f"{tri_name(b['exit_lo']):>8s}→{tri_name(b['entry_lo']):>8s}  "
              f"{tri_name(b['exit_up']):>8s}→{tri_name(b['entry_up']):>8s}")

    # Distribution of (lo_dist, up_dist) pairs
    print(f"\n  (lo_dist, up_dist) distribution for non-preserving bridges:")
    dist_pairs = Counter((b['lo_dist'], b['up_dist']) for b in non_pres)
    for dp, cnt in sorted(dist_pairs.items()):
        print(f"    ({dp[0]}, {dp[1]}): {cnt}")

    # Preferred direction: which specific lines change most often?
    line_freq = Counter()
    for b in non_pres:
        for i in range(3):
            if b['exit_lo'][i] != b['entry_lo'][i]:
                line_freq[f'L{i+1}'] += 1
            if b['exit_up'][i] != b['entry_up'][i]:
                line_freq[f'L{i+4}'] += 1

    print(f"\n  Line change frequency across 22 non-preserving bridges:")
    for line in ['L1', 'L2', 'L3', 'L4', 'L5', 'L6']:
        print(f"    {line}: {line_freq.get(line, 0)}/22")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    bridges = build_bridges()

    task_a(bridges)
    task_b(bridges)
    task_c(bridges)
    task_d(bridges)
    task_e(bridges)
    task_c_nonpreserving(bridges)

    print("\n" + "=" * 90)
    print("BRIDGE TRIGRAM ANALYSIS COMPLETE")
    print("=" * 90)
