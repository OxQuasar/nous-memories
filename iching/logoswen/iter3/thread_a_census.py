"""
Thread A: Orientation Census

For each of the 32 King Wen pairs, characterize which hexagram comes first
in four frames: inversion, weight, binary, orbit position.

Encode each frame as a 32-bit string. Compute balance, run-length structure,
autocorrelation, spectral content. Compare against 10,000 random orientations.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')
sys.path.insert(0, '/home/quasar/nous/logoswen/iter2')

import numpy as np
from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
from analysis_utils import VALID_MASKS, xor_sig, xor_tuple, hamming

DIMS = 6
N_PAIRS = 32
N_TRIALS = 10000
RNG = np.random.default_rng(42)

M = [tuple(h) for h in all_bits()]

# ─── Build pairs ────────────────────────────────────────────────────────────

pairs = []
for k in range(N_PAIRS):
    a = M[2 * k]
    b = M[2 * k + 1]
    mask = xor_tuple(a, b)
    pairs.append({
        'idx': k,
        'a': a, 'b': b,
        'num_a': KING_WEN[2 * k][0],
        'num_b': KING_WEN[2 * k + 1][0],
        'name_a': KING_WEN[2 * k][1],
        'name_b': KING_WEN[2 * k + 1][1],
        'mask': mask,
        'sig': xor_sig(a),
    })


# ─── Helper functions ───────────────────────────────────────────────────────

def reverse_bits(h):
    """Inversion: read hexagram upside-down (reverse bit order)."""
    return tuple(h[5-i] for i in range(DIMS))

def complement(h):
    """Complement: flip all lines."""
    return tuple(1 - x for x in h)

def weight(h):
    """Yang count (number of 1s)."""
    return sum(h)

def to_int(h):
    """Binary value (bit 0 = MSB convention, i.e. as-written)."""
    val = 0
    for bit in h:
        val = val * 2 + bit
    return val

def is_palindrome(h):
    """Whether hexagram reads same upside-down."""
    return h == reverse_bits(h)


# ─── 1. Classify pair types and build orientation in each frame ─────────────

def build_orientation_frames():
    """
    For each pair, determine orientation bit in multiple frames.
    Returns dict of frame_name -> 32-element list of 0/1.
    """
    frames = {
        'inversion': [],     # 1 = first hex is the "original" (first == reverse(second))
        'weight': [],        # 1 = first hex has higher weight (more yang)
        'binary': [],        # 1 = first hex has higher binary value
    }
    
    pair_types = []  # 'inversion' or 'complement' (for palindromic)
    
    for p in pairs:
        a, b = p['a'], p['b']
        
        # Determine pair type
        if reverse_bits(a) == b:
            ptype = 'inversion'
            # "Original" is a, "inverted" is b → orientation = 1
            frames['inversion'].append(1)
        elif reverse_bits(b) == a:
            ptype = 'inversion'
            # "Original" is b, "inverted" is a → orientation = 0
            frames['inversion'].append(0)
        elif is_palindrome(a) and is_palindrome(b):
            # Both palindromes — paired by complement
            ptype = 'complement'
            # Convention: "original" is the one that comes first (by complement rule)
            # For palindromes, inversion is identity, so use complement frame
            if complement(a) == b:
                frames['inversion'].append(1)  # a → complement → b
            elif complement(b) == a:
                frames['inversion'].append(0)
            else:
                frames['inversion'].append(-1)  # shouldn't happen
                print(f"  WARNING: pair {p['idx']+1} neither inversion nor complement!")
        else:
            ptype = 'unknown'
            frames['inversion'].append(-1)
            print(f"  WARNING: pair {p['idx']+1} unknown type: "
                  f"{p['name_a']}-{p['name_b']}")
        
        pair_types.append(ptype)
        
        # Weight frame
        wa, wb = weight(a), weight(b)
        if wa > wb:
            frames['weight'].append(1)
        elif wa < wb:
            frames['weight'].append(0)
        else:
            frames['weight'].append(-1)  # equal weight
        
        # Binary frame
        va, vb = to_int(a), to_int(b)
        if va > vb:
            frames['binary'].append(1)
        elif va < vb:
            frames['binary'].append(0)
        else:
            frames['binary'].append(-1)  # equal (shouldn't happen for distinct hexagrams)
    
    return frames, pair_types


def print_pair_table(frames, pair_types):
    """Print the full pair table with orientation in each frame."""
    print("=" * 90)
    print("ORIENTATION CENSUS — PAIR TABLE")
    print("=" * 90)
    print(f"{'Pair':>4s}  {'#A':>3s} {'#B':>3s}  {'Hex A':>6s} {'Hex B':>6s}  "
          f"{'Type':>10s}  {'Inv':>3s} {'Wt':>3s} {'Bin':>3s}  Names")
    print("-" * 90)
    
    for i, p in enumerate(pairs):
        a_str = ''.join(map(str, p['a']))
        b_str = ''.join(map(str, p['b']))
        inv = frames['inversion'][i]
        wt = frames['weight'][i]
        bn = frames['binary'][i]
        inv_s = str(inv) if inv >= 0 else '='
        wt_s = str(wt) if wt >= 0 else '='
        bn_s = str(bn) if bn >= 0 else '='
        print(f"  {i+1:3d}  {p['num_a']:3d} {p['num_b']:3d}  {a_str} {b_str}  "
              f"{pair_types[i]:>10s}  {inv_s:>3s} {wt_s:>3s} {bn_s:>3s}  "
              f"{p['name_a']}-{p['name_b']}")


# ─── 2. Orientation string statistics ───────────────────────────────────────

def analyze_bitstring(bits, name, exclude_val=-1):
    """Analyze a 32-element orientation bitstring."""
    # Filter out ambiguous positions
    valid_mask = [b != exclude_val for b in bits]
    valid_bits = [b for b in bits if b != exclude_val]
    n_valid = len(valid_bits)
    n_excluded = N_PAIRS - n_valid
    
    print(f"\n  Frame: {name}")
    print(f"    Valid positions: {n_valid}/32 (excluded: {n_excluded})")
    
    if n_valid == 0:
        return {}
    
    # Balance
    ones = sum(valid_bits)
    zeros = n_valid - ones
    print(f"    Balance: {ones} ones, {zeros} zeros "
          f"(ratio: {ones/n_valid:.3f})")
    
    # Bitstring display
    bit_str = ''.join(str(b) if b >= 0 else '.' for b in bits)
    print(f"    Bitstring: {bit_str}")
    
    # Run-length structure (on full 32-bit including ambiguous as-is)
    full_bits = bits  # use as-is for run analysis
    runs = []
    if len(full_bits) > 0:
        current = full_bits[0]
        length = 1
        for b in full_bits[1:]:
            if b == current:
                length += 1
            else:
                runs.append((current, length))
                current = b
                length = 1
        runs.append((current, length))
    
    print(f"    Number of runs: {len(runs)}")
    print(f"    Run lengths: {[r[1] for r in runs]}")
    print(f"    Max run: {max(r[1] for r in runs)}")
    print(f"    Mean run: {np.mean([r[1] for r in runs]):.2f}")
    
    # Autocorrelation (on the full 32-bit string, treating -1 as 0.5)
    arr = np.array([b if b >= 0 else 0.5 for b in bits], dtype=float)
    arr_centered = arr - np.mean(arr)
    var = np.var(arr)
    
    print(f"    Autocorrelation:")
    autocorr = {}
    for lag in [1, 2, 4, 8, 16]:
        if lag < N_PAIRS and var > 0:
            c = np.mean(arr_centered[:N_PAIRS-lag] * arr_centered[lag:]) / var
            autocorr[lag] = c
            print(f"      lag {lag:2d}: {c:+.3f}")
    
    # FFT (spectral analysis)
    if n_valid >= 8:
        fft_vals = np.fft.rfft(arr - np.mean(arr))
        power = np.abs(fft_vals) ** 2
        top_freqs = np.argsort(power[1:])[::-1][:5] + 1  # exclude DC
        print(f"    Top spectral peaks (frequency index): {list(top_freqs)}")
        print(f"    Power at those peaks: {[f'{power[f]:.2f}' for f in top_freqs]}")
    
    return {
        'n_valid': n_valid,
        'balance': ones / n_valid,
        'n_runs': len(runs),
        'max_run': max(r[1] for r in runs),
        'autocorr': autocorr,
    }


def monte_carlo_comparison(bits, name, exclude_val=-1):
    """Compare orientation bitstring against random orientations."""
    valid_bits = [b for b in bits if b != exclude_val]
    n_valid = len(valid_bits)
    
    if n_valid < 16:
        print(f"\n  Monte Carlo for {name}: too few valid bits ({n_valid})")
        return
    
    # Actual statistics
    actual_ones = sum(valid_bits)
    
    # Run count on valid bits
    runs = 1
    for i in range(1, len(valid_bits)):
        if valid_bits[i] != valid_bits[i-1]:
            runs += 1
    actual_runs = runs
    
    # Autocorrelation at lag 1 on valid bits
    arr = np.array(valid_bits, dtype=float)
    arr_c = arr - np.mean(arr)
    var = np.var(arr)
    actual_ac1 = np.mean(arr_c[:-1] * arr_c[1:]) / var if var > 0 else 0
    
    # Monte Carlo
    mc_ones = []
    mc_runs = []
    mc_ac1 = []
    
    for _ in range(N_TRIALS):
        rand = RNG.integers(0, 2, size=n_valid)
        mc_ones.append(sum(rand))
        
        r = 1
        for i in range(1, n_valid):
            if rand[i] != rand[i-1]:
                r += 1
        mc_runs.append(r)
        
        r_arr = rand.astype(float)
        r_c = r_arr - np.mean(r_arr)
        v = np.var(r_arr)
        mc_ac1.append(np.mean(r_c[:-1] * r_c[1:]) / v if v > 0 else 0)
    
    mc_ones = np.array(mc_ones)
    mc_runs = np.array(mc_runs)
    mc_ac1 = np.array(mc_ac1)
    
    print(f"\n  Monte Carlo for {name} ({N_TRIALS} trials):")
    
    # Balance test
    p_ones = np.mean(np.abs(mc_ones - n_valid/2) >= abs(actual_ones - n_valid/2))
    print(f"    Balance: actual={actual_ones}/{n_valid}, "
          f"p(as extreme)={p_ones:.4f}")
    
    # Runs test
    p_runs_low = np.mean(mc_runs <= actual_runs)
    p_runs_high = np.mean(mc_runs >= actual_runs)
    print(f"    Runs: actual={actual_runs}, "
          f"random mean={np.mean(mc_runs):.1f}±{np.std(mc_runs):.1f}, "
          f"p(≤actual)={p_runs_low:.4f}, p(≥actual)={p_runs_high:.4f}")
    
    # Autocorrelation test
    p_ac1 = np.mean(np.abs(mc_ac1) >= abs(actual_ac1))
    print(f"    Lag-1 autocorr: actual={actual_ac1:+.3f}, "
          f"p(|r|≥|actual|)={p_ac1:.4f}")


# ─── 3. Cross-frame correlation ────────────────────────────────────────────

def cross_frame_analysis(frames):
    """Analyze correlation between different orientation frames."""
    print("\n" + "=" * 70)
    print("CROSS-FRAME CORRELATION")
    print("=" * 70)
    
    frame_names = list(frames.keys())
    for i in range(len(frame_names)):
        for j in range(i+1, len(frame_names)):
            fi, fj = frame_names[i], frame_names[j]
            bi, bj = frames[fi], frames[fj]
            
            # Only compare positions where both are valid
            valid = [(bi[k], bj[k]) for k in range(N_PAIRS) 
                     if bi[k] >= 0 and bj[k] >= 0]
            
            if len(valid) < 8:
                continue
            
            agree = sum(1 for a, b in valid if a == b)
            disagree = len(valid) - agree
            
            print(f"\n  {fi} vs {fj}:")
            print(f"    Valid positions: {len(valid)}")
            print(f"    Agree: {agree}, Disagree: {disagree}")
            
            if len(valid) > 0:
                match_rate = agree / len(valid)
                print(f"    Match rate: {match_rate:.3f}")
                
                # Compute correlation
                a_arr = np.array([v[0] for v in valid], dtype=float)
                b_arr = np.array([v[1] for v in valid], dtype=float)
                if np.std(a_arr) > 0 and np.std(b_arr) > 0:
                    corr = np.corrcoef(a_arr, b_arr)[0, 1]
                    print(f"    Pearson r: {corr:+.3f}")


# ─── 4. Orbit position frame ───────────────────────────────────────────────

def orbit_position_analysis():
    """
    In the factored basis (ō,m̄,ī,o,m,i), each hexagram has orbit coords
    (ō,m̄,ī) = xor_sig and position coords (o,m,i) within the orbit.
    
    Within a pair, both hexagrams share the same orbit. The mask = sig means
    the position coordinates flip by the mask's orbit-space representation.
    
    Characterize which position comes first.
    """
    print("\n" + "=" * 70)
    print("ORBIT POSITION ANALYSIS")
    print("=" * 70)
    
    GEN_BITS_6 = {
        'O':   (1,0,0,0,0,1),
        'M':   (0,1,0,0,1,0),
        'I':   (0,0,1,1,0,0),
    }
    
    # Decompose each hexagram into orbit + position
    # The orbit signature is (L1⊕L6, L2⊕L5, L3⊕L4)
    # The position within orbit is determined by a choice of coset representative
    # A natural representative: the lower 3 bits of the position coordinates
    # Since orbit = (L1⊕L6, L2⊕L5, L3⊕L4), we need coordinates orthogonal to this
    
    # Simple position: (L1, L2, L3) — the "lower half"
    # This is one of 8 possible representatives within each orbit
    # The mask acts on this as: position XOR (mask's lower-half projection)
    
    print("\n  Per-pair position analysis:")
    print(f"  {'Pair':>4s}  {'Orbit':>7s}  {'Mask':>6s}  {'Pos A':>5s} {'Pos B':>5s}  "
          f"{'Wt_A':>4s} {'Wt_B':>4s}  {'First heavier?':>14s}")
    
    position_bits = []  # For each pair: which of the two positions comes first
    
    for p in pairs:
        a, b = p['a'], p['b']
        sig = p['sig']
        mask = p['mask']
        
        # Position = lower 3 bits (L1, L2, L3)
        pos_a = a[:3]
        pos_b = b[:3]
        
        # Weight comparison
        wa, wb = weight(a), weight(b)
        heavier = 'A' if wa > wb else ('B' if wb > wa else '=')
        
        mask_str = ''.join(map(str, mask))
        sig_str = ''.join(map(str, sig))
        pos_a_str = ''.join(map(str, pos_a))
        pos_b_str = ''.join(map(str, pos_b))
        
        print(f"  {p['idx']+1:4d}  {sig_str:>7s}  {mask_str}  "
              f"{pos_a_str:>5s} {pos_b_str:>5s}  "
              f"{wa:4d} {wb:4d}  {heavier:>14s}")
        
        # Orientation bit: which position has lower binary value?
        va = to_int(pos_a)
        vb = to_int(pos_b)
        position_bits.append(1 if va < vb else 0)
    
    # Group by orbit
    print("\n  Orientation by orbit:")
    orbit_groups = defaultdict(list)
    for i, p in enumerate(pairs):
        orbit_groups[p['sig']].append((i, position_bits[i]))
    
    for sig in sorted(orbit_groups.keys()):
        items = orbit_groups[sig]
        bit_str = ''.join(str(b) for _, b in items)
        print(f"    Orbit {sig}: positions {[i+1 for i,_ in items]}, "
              f"orientation: {bit_str}")
    
    return position_bits


# ─── 5. Palindrome analysis ────────────────────────────────────────────────

def palindrome_analysis():
    """Special analysis for the 8 palindromic pairs (paired by complement)."""
    print("\n" + "=" * 70)
    print("PALINDROMIC (COMPLEMENT) PAIRS")
    print("=" * 70)
    
    pal_pairs = []
    for p in pairs:
        a, b = p['a'], p['b']
        if is_palindrome(a) and is_palindrome(b):
            pal_pairs.append(p)
        elif is_palindrome(a) or is_palindrome(b):
            # One palindrome, one not — shouldn't happen with mask=sig
            print(f"  WARNING: mixed palindrome pair {p['idx']+1}")
    
    print(f"\n  Number of palindromic pairs: {len(pal_pairs)}")
    print(f"\n  {'Pair':>4s}  {'#A':>3s} {'#B':>3s}  {'Hex A':>6s} {'Hex B':>6s}  "
          f"{'Wt A':>4s} {'Wt B':>4s}  {'Heavier first':>13s}  Names")
    
    heavier_first = 0
    lighter_first = 0
    
    for p in pal_pairs:
        a, b = p['a'], p['b']
        wa, wb = weight(a), weight(b)
        a_str = ''.join(map(str, a))
        b_str = ''.join(map(str, b))
        
        if wa > wb:
            hf = 'Yes'
            heavier_first += 1
        elif wb > wa:
            hf = 'No'
            lighter_first += 1
        else:
            hf = 'Equal'
        
        print(f"  {p['idx']+1:4d}  {p['num_a']:3d} {p['num_b']:3d}  {a_str} {b_str}  "
              f"{wa:4d} {wb:4d}  {hf:>13s}  {p['name_a']}-{p['name_b']}")
    
    print(f"\n  Heavier first: {heavier_first}/{len(pal_pairs)}")
    print(f"  Lighter first: {lighter_first}/{len(pal_pairs)}")
    
    # These pairs have mask = (1,1,1,1,1,1) = OMI (complement)
    # Weight of complement = 6 - weight, so they always have different weight
    # unless weight = 3

    return pal_pairs


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("THREAD A: ORIENTATION CENSUS")
    print("=" * 90)
    
    # Build frames
    frames, pair_types = build_orientation_frames()
    
    # Print pair table
    print_pair_table(frames, pair_types)
    
    # Type summary
    type_counts = Counter(pair_types)
    print(f"\n  Pair type summary: {dict(type_counts)}")
    
    # Analyze each frame
    print("\n" + "=" * 70)
    print("ORIENTATION FRAME ANALYSIS")
    print("=" * 70)
    
    stats = {}
    for fname, fbits in frames.items():
        s = analyze_bitstring(fbits, fname)
        stats[fname] = s
    
    # Monte Carlo comparison for each frame
    print("\n" + "=" * 70)
    print("MONTE CARLO COMPARISON")
    print("=" * 70)
    
    for fname, fbits in frames.items():
        monte_carlo_comparison(fbits, fname)
    
    # Cross-frame correlation
    cross_frame_analysis(frames)
    
    # Orbit position analysis
    pos_bits = orbit_position_analysis()
    
    # Palindrome analysis
    pal_pairs = palindrome_analysis()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    for fname, fbits in frames.items():
        valid = [b for b in fbits if b >= 0]
        n_valid = len(valid)
        ones = sum(valid) if valid else 0
        bit_str = ''.join(str(b) if b >= 0 else '.' for b in fbits)
        print(f"  {fname:>15s}: {bit_str}  ({ones}/{n_valid})")
    
    print(f"\n  Position frame:   {''.join(str(b) for b in pos_bits)}  "
          f"({sum(pos_bits)}/{len(pos_bits)})")


if __name__ == "__main__":
    main()
