"""
Thread F: Fu Xi (binary ordering) comparison.

The Fu Xi ordering lists hexagrams by binary value 0-63.
This is the "natural" / "computer science" ordering — maximally regular,
non-designed. Apply the full analysis pipeline and compare to King Wen.
"""

import sys
from collections import Counter, defaultdict

sys.path.insert(0, '../../kingwen')
from analysis_utils import (analyze_sequence, summarize, xor_sig, xor_tuple,
                             VALID_MASKS, DIMS, build_orbits_by_sig)
from sequence import KING_WEN, all_bits


def fuxi_sequence():
    """Generate the Fu Xi binary ordering: hexagrams 0-63 in binary."""
    seq = []
    for i in range(64):
        # 6-bit tuple, bit 0 = LSB (matching kingwen convention: bottom line first)
        h = tuple((i >> b) & 1 for b in range(6))
        seq.append(h)
    return seq


def detailed_bridge_analysis(seq, label):
    """Print detailed bridge-by-bridge analysis."""
    print(f"\n{'=' * 70}")
    print(f"BRIDGE ANALYSIS: {label}")
    print(f"{'=' * 70}")
    
    print(f"\n  {'B':>3s}  {'Hex_a':>8s} → {'Hex_b':>8s}  {'Mask':>8s}  "
          f"{'OrbitA':>7s} → {'OrbitB':>7s}  H  minH  S")
    
    for k in range(31):
        a = seq[2 * k + 1]
        b = seq[2 * k + 2]
        mask = xor_tuple(a, b)
        sig_a = xor_sig(a)
        sig_b = xor_sig(b)
        h = sum(mask)
        
        mask_name = VALID_MASKS.get(mask, ''.join(map(str, mask)))
        
        # Minimum Hamming to target orbit
        orbits = build_orbits_by_sig()
        target = orbits[sig_b]
        min_h = min(sum(x ^ y for x, y in zip(a, tuple(t))) for t in target)
        S = (h - min_h) // 2 if (h - min_h) % 2 == 0 else -1
        
        cross = "→" if sig_a != sig_b else "⟳"
        
        print(f"  {k+1:3d}  {''.join(map(str,a))} {cross} {''.join(map(str,b))}  "
              f"{mask_name:>8s}  "
              f"{''.join(map(str,sig_a))} → {''.join(map(str,sig_b))}  "
              f"{h}  {min_h:4d}  {S}")


def detailed_pair_analysis(seq, label):
    """Print detailed pair-by-pair analysis."""
    print(f"\n{'=' * 70}")
    print(f"PAIR ANALYSIS: {label}")
    print(f"{'=' * 70}")
    
    print(f"\n  {'P':>3s}  {'Hex_a':>8s}  {'Hex_b':>8s}  {'Mask':>8s}  "
          f"{'Orbit':>7s}  {'Valid':>5s}  H")
    
    for k in range(32):
        a = seq[2 * k]
        b = seq[2 * k + 1]
        mask = xor_tuple(a, b)
        sig = xor_sig(a)
        is_valid = mask in VALID_MASKS
        mask_name = VALID_MASKS.get(mask, ''.join(map(str, mask)))
        h = sum(mask)
        
        print(f"  {k+1:3d}  {''.join(map(str,a))}  {''.join(map(str,b))}  "
              f"{mask_name:>8s}  {''.join(map(str,sig))}  "
              f"{'✓' if is_valid else '✗':>5s}  {h}")


def comparison_table(kw_result, fx_result):
    """Print side-by-side comparison table."""
    print(f"\n{'=' * 70}")
    print("COMPARISON TABLE: KING WEN vs FU XI")
    print(f"{'=' * 70}")
    
    rows = [
        ("Orbit-consistent pairs", 
         f"{kw_result['orbit_consistent']}/32",
         f"{fx_result['orbit_consistent']}/32"),
        ("Eulerian bridge walk",
         f"{'YES' if kw_result['is_eulerian'] else 'NO'} ({kw_result['eulerian_type']})",
         f"{'YES' if fx_result['is_eulerian'] else 'NO'}"),
        ("Start orbit",
         f"{kw_result['start_orbit']}",
         f"{fx_result['start_orbit']}"),
        ("End orbit",
         f"{kw_result['end_orbit']}",
         f"{fx_result['end_orbit']}"),
        ("Qian(000)→Tai(111)",
         f"{'YES' if kw_result['qian_to_tai'] else 'NO'}",
         f"{'YES' if fx_result['qian_to_tai'] else 'NO'}"),
        ("S distribution",
         str(dict(sorted(kw_result['S_dist'].items()))),
         str(dict(sorted(fx_result['S_dist'].items())))),
        ("Mean S",
         f"{sum(kw_result['S_values'])/31:.3f}",
         f"{sum(fx_result['S_values'])/31:.3f}"),
        ("Self-loop count",
         str(kw_result['self_loop_count']),
         str(fx_result['self_loop_count'])),
        ("Self-loop positions",
         str(kw_result['self_loop_positions']),
         str(fx_result['self_loop_positions'])),
        ("Weight-5 gap (no wt-5)",
         f"{'YES' if not kw_result['has_weight_5'] else 'NO'}",
         f"{'YES' if not fx_result['has_weight_5'] else 'NO'}"),
        ("Bridge weight dist",
         str(dict(sorted(kw_result['weight_dist'].items()))),
         str(dict(sorted(fx_result['weight_dist'].items())))),
        ("Hamiltonian prefix",
         str(kw_result['prefix_length']),
         str(fx_result['prefix_length'])),
        ("Orbits in bridge graph",
         str(kw_result['n_orbits_used']),
         str(fx_result['n_orbits_used'])),
        ("Orbit visits",
         str(dict(sorted(kw_result['orbit_visits'].items()))),
         str(dict(sorted(fx_result['orbit_visits'].items())))),
    ]
    
    # Also compute pair mask distribution
    kw_pair_masks = Counter(VALID_MASKS.get(m, 'non-std') for m in kw_result['pair_masks'])
    fx_pair_masks = Counter(VALID_MASKS.get(m, 'non-std') for m in fx_result['pair_masks'])
    rows.append(("Pair mask distribution",
                 str(dict(sorted(kw_pair_masks.items()))),
                 str(dict(sorted(fx_pair_masks.items())))))
    
    # Degree balance
    rows.append(("Sources (out>in)",
                 str([f"{s}" for s in kw_result['sources']]),
                 str([f"{s}" for s in fx_result['sources']])))
    rows.append(("Sinks (in>out)",
                 str([f"{s}" for s in kw_result['sinks']]),
                 str([f"{s}" for s in fx_result['sinks']])))
    
    print(f"\n  {'Metric':<30s}  {'King Wen':<35s}  {'Fu Xi':<35s}")
    print(f"  {'─'*30}  {'─'*35}  {'─'*35}")
    for metric, kw_val, fx_val in rows:
        print(f"  {metric:<30s}  {kw_val:<35s}  {fx_val:<35s}")


def main():
    print("=" * 70)
    print("THREAD F: FU XI (BINARY ORDERING) COMPARISON")
    print("=" * 70)
    
    # Build sequences
    M = all_bits()
    kw_seq = [tuple(M[i]) for i in range(64)]
    fx_seq = fuxi_sequence()
    
    # Print first few to verify
    print("\nFu Xi sequence (first 8):")
    for i in range(8):
        print(f"  {i}: {''.join(map(str, fx_seq[i]))}")
    
    print("\nKing Wen sequence (first 8):")
    for i in range(8):
        print(f"  {i}: {''.join(map(str, kw_seq[i]))} = #{KING_WEN[i][0]} {KING_WEN[i][1]}")
    
    # Detailed pair analysis
    detailed_pair_analysis(fx_seq, "FU XI")
    
    # Detailed bridge analysis
    detailed_bridge_analysis(fx_seq, "FU XI")
    
    # Full analysis
    print(f"\n{'=' * 70}")
    print("RUNNING FULL ANALYSIS...")
    print(f"{'=' * 70}")
    
    kw_result = analyze_sequence(kw_seq)
    fx_result = analyze_sequence(fx_seq)
    
    print(f"\n{summarize(kw_result, 'King Wen')}")
    print(f"{summarize(fx_result, 'Fu Xi')}")
    
    # Comparison table
    comparison_table(kw_result, fx_result)
    
    # Additional Fu Xi-specific analysis
    print(f"\n{'=' * 70}")
    print("FU XI SPECIFIC ANALYSIS")
    print(f"{'=' * 70}")
    
    # Fu Xi pairs: (0,1), (2,3), (4,5)... in binary, consecutive pairs differ by bit 0
    print("\nFu Xi pair structure:")
    print("  All pairs (2k, 2k+1) differ in bit 0 only.")
    print("  Every pair mask should be (1,0,0,0,0,0).")
    
    fx_masks = []
    for k in range(32):
        mask = xor_tuple(fx_seq[2*k], fx_seq[2*k+1])
        fx_masks.append(mask)
    mask_counter = Counter(fx_masks)
    print(f"  Pair mask distribution: {dict((str(k), v) for k, v in mask_counter.items())}")
    
    # Check: (1,0,0,0,0,0) is NOT a valid Z₂³ mask (it's a single-bit flip, not an O/M/I pair)
    for mask in mask_counter:
        valid = mask in VALID_MASKS
        print(f"    {mask}: {'VALID' if valid else 'NOT VALID'} Z₂³ mask")
    
    # Fu Xi bridges: hex 2k+1 -> hex 2k+2
    # (2k+1) in binary -> (2k+2) in binary
    # Example: 1 (000001) -> 2 (000010), XOR = 000011
    print("\nFu Xi bridge structure:")
    print("  Bridge from hex 2k+1 to hex 2k+2:")
    print("  In binary: (2k+1) XOR (2k+2)")
    
    for k in range(min(8, 31)):
        a_val = 2*k + 1
        b_val = 2*k + 2
        xor_val = a_val ^ b_val
        print(f"    B{k+1}: {a_val:2d}({a_val:06b}) → {b_val:2d}({b_val:06b}) "
              f"XOR={xor_val:06b} H={bin(xor_val).count('1')}")
    
    print(f"\n{'=' * 70}")
    print("THREAD F COMPLETE")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
