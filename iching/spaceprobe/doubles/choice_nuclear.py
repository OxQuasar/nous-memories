#!/usr/bin/env python3
"""
Choice point 3: Alternative nuclear (互卦) operations.

Traditional 互: lower_nuc = (L2,L3,L4), upper_nuc = (L3,L4,L5).
This is a 4-line consecutive window at position 2, with two overlapping trigrams.

What alternatives exist? We enumerate:
1. All 3 consecutive-window positions (start=1,2,3)
2. All non-overlapping trigram selections  
3. Classify by kernel, H-like subgroup, idempotence
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from cycle_algebra import hugua, bit, fmt6, NUM_HEX, MASK_ALL
from collections import Counter

# ═══════════════════════════════════════════════════════════════════════════
# Framework
# ═══════════════════════════════════════════════════════════════════════════

# Hexagram: 6 bits, L1=bit0 (bottom) through L6=bit5 (top).
# A nuclear operation selects 3 bit positions for lower trigram
# and 3 for upper trigram, producing a new hexagram.

def make_nuclear(lower_bits, upper_bits):
    """Create a nuclear operation from bit selections.
    lower_bits = (b0, b1, b2): which input bits form output bits 0,1,2
    upper_bits = (b3, b4, b5): which input bits form output bits 3,4,5
    """
    def nuc(h):
        out = 0
        for i, src in enumerate(lower_bits):
            out |= bit(h, src) << i
        for i, src in enumerate(upper_bits):
            out |= bit(h, src) << (i + 3)
        return out
    return nuc

def kernel_mask(o, m, i):
    """Palindromic mask from (O,M,I) flip pattern."""
    return o | (m << 1) | (i << 2) | (i << 3) | (m << 4) | (o << 5)

NAMES = {(0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
         (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'}


def analyze_nuclear(nuc_fn, label):
    """Analyze a nuclear operation."""
    # Image size
    images = set(nuc_fn(h) for h in range(NUM_HEX))
    image_size = len(images)

    # Kernel: palindromic masks that leave output unchanged
    kernel = []
    for o in range(2):
        for m in range(2):
            for i in range(2):
                mask = kernel_mask(o, m, i)
                if all(nuc_fn(h) == nuc_fn(h ^ mask) for h in range(NUM_HEX)):
                    kernel.append((o, m, i))

    # H-like: palindromic masks that act as identity OR complement on output
    h_like = []
    for o in range(2):
        for m in range(2):
            for i in range(2):
                mask = kernel_mask(o, m, i)
                is_id = all(nuc_fn(h ^ mask) == nuc_fn(h) for h in range(NUM_HEX))
                is_comp = all(nuc_fn(h ^ mask) == nuc_fn(h) ^ MASK_ALL for h in range(NUM_HEX))
                if is_id or is_comp:
                    action = "id" if is_id else "comp"
                    h_like.append(((o, m, i), action))

    # Idempotence
    idempotent = all(nuc_fn(nuc_fn(h)) == nuc_fn(h) for h in range(NUM_HEX))

    # Fiber compatibility: for each Z₂³ element, does it preserve fibers?
    fiber_compat = []
    for o in range(2):
        for m in range(2):
            for i in range(2):
                mask = kernel_mask(o, m, i)
                compatible = True
                for h1 in range(NUM_HEX):
                    for h2 in range(h1 + 1, NUM_HEX):
                        if nuc_fn(h1) == nuc_fn(h2):
                            if nuc_fn(h1 ^ mask) != nuc_fn(h2 ^ mask):
                                compatible = False
                                break
                    if not compatible:
                        break
                if compatible:
                    fiber_compat.append((o, m, i))

    return {
        'label': label,
        'image_size': image_size,
        'kernel': frozenset(kernel),
        'h_like': frozenset(k for k, _ in h_like),
        'h_like_detail': h_like,
        'idempotent': idempotent,
        'fiber_compat': frozenset(fiber_compat),
    }


def main():
    print("=" * 70)
    print("CHOICE POINT 3: ALTERNATIVE NUCLEAR OPERATIONS")
    print("=" * 70)

    # ───────────────────────────────────────────────────────────────────
    # Part 1: Consecutive-window nuclear operations
    # ───────────────────────────────────────────────────────────────────
    print("\n--- Consecutive-window nuclear operations ---")
    print("  Lower=(L_s, L_{s+1}, L_{s+2}), Upper=(L_{s+1}, L_{s+2}, L_{s+3})")
    print()

    consec_results = []
    for start in [1, 2, 3]:
        # Bit positions: L_k = bit(k-1)
        lower_bits = (start - 1, start, start + 1)
        upper_bits = (start, start + 1, start + 2)
        label = f"start={start}: L{start}-L{start+3}"
        nuc_fn = make_nuclear(lower_bits, upper_bits)

        # Verify traditional
        if start == 2:
            for h in range(NUM_HEX):
                assert nuc_fn(h) == hugua(h), f"Mismatch at h={h}"

        result = analyze_nuclear(nuc_fn, label)
        consec_results.append(result)

        kernel_str = ','.join(NAMES[k] for k in sorted(result['kernel']))
        h_like_str = ','.join(NAMES[k] for k in sorted(result['h_like']))
        fiber_str = ','.join(NAMES[k] for k in sorted(result['fiber_compat']))
        trad = " ← TRADITIONAL 互" if start == 2 else ""

        print(f"  {label}{trad}")
        print(f"    Image: {result['image_size']}/64, "
              f"Kernel: {{{kernel_str}}}, "
              f"H-like: {{{h_like_str}}}")
        print(f"    Fiber-compatible: {{{fiber_str}}}")
        print(f"    Idempotent: {result['idempotent']}")
        print()

    # ───────────────────────────────────────────────────────────────────
    # Part 2: All 4-line window operations (not necessarily consecutive)
    # ───────────────────────────────────────────────────────────────────
    print("--- All 4-line window operations ---")
    print("  Choose 4 of 6 lines. Lower = first 3, Upper = last 3 (overlapping middle 2).")
    print()

    from itertools import combinations

    window_results = []
    for lines in combinations(range(6), 4):
        # Lower trigram = first 3 lines, upper = last 3
        lower_bits = lines[:3]
        upper_bits = lines[1:]
        label = f"lines ({','.join(f'L{l+1}' for l in lines)})"
        nuc_fn = make_nuclear(lower_bits, upper_bits)
        result = analyze_nuclear(nuc_fn, label)
        window_results.append((lines, result))

    print(f"  {'Lines':>25s}  {'Image':>5s}  {'Kernel':>15s}  "
          f"{'H-like':>20s}  {'Idem':>4s}")
    print("-" * 80)

    for lines, result in window_results:
        kernel_str = ','.join(NAMES[k] for k in sorted(result['kernel']))
        h_like_str = ','.join(NAMES[k] for k in sorted(result['h_like']))
        line_str = ','.join(f'L{l+1}' for l in lines)
        idem = 'yes' if result['idempotent'] else 'no'
        note = ""
        if lines == (1, 2, 3, 4):
            note = " ← TRADITIONAL"
        if result['h_like'] == frozenset([(0,0,0),(1,0,0),(0,1,1),(1,1,1)]):
            note += " [H=trad]"
        print(f"  {line_str:>25s}  {result['image_size']:>5d}  "
              f"{'{'+kernel_str+'}':>15s}  "
              f"{'{'+h_like_str+'}':>20s}  "
              f"{idem:>4s}{note}")

    # ───────────────────────────────────────────────────────────────────
    # Part 3: Non-overlapping trigram pairs
    # ───────────────────────────────────────────────────────────────────
    print("\n--- Non-overlapping trigram pairs ---")
    print("  Choose 3 bits for lower, 3 different bits for upper.")
    print()

    # All ways to partition 6 bits into 2 groups of 3
    non_overlap_results = []
    seen = set()
    for lower in combinations(range(6), 3):
        upper = tuple(b for b in range(6) if b not in lower)
        key = (lower, upper)
        if key in seen:
            continue
        seen.add(key)

        label = f"lower=({','.join(f'L{l+1}' for l in lower)}), upper=({','.join(f'L{u+1}' for u in upper)})"
        nuc_fn = make_nuclear(lower, upper)
        result = analyze_nuclear(nuc_fn, label)
        non_overlap_results.append((lower, upper, result))

    print(f"  {'Lower':>15s}  {'Upper':>15s}  {'Image':>5s}  {'Kernel':>10s}  "
          f"{'H-like':>20s}  {'Idem':>4s}")
    print("-" * 80)
    for lower, upper, result in non_overlap_results:
        l_str = ','.join(f'L{l+1}' for l in lower)
        u_str = ','.join(f'L{u+1}' for u in upper)
        k_str = ','.join(NAMES[k] for k in sorted(result['kernel']))
        h_str = ','.join(NAMES[k] for k in sorted(result['h_like']))
        idem = 'yes' if result['idempotent'] else 'no'
        note = ""
        # Natural one: lower=(L1,L2,L3), upper=(L4,L5,L6) = identity
        if lower == (0, 1, 2) and upper == (3, 4, 5):
            note = " ← identity"
        if result['h_like'] == frozenset([(0,0,0),(1,0,0),(0,1,1),(1,1,1)]):
            note += " [H=trad]"
        print(f"  {l_str:>15s}  {u_str:>15s}  {result['image_size']:>5d}  "
              f"{'{'+k_str+'}':>10s}  "
              f"{'{'+h_str+'}':>20s}  "
              f"{idem:>4s}{note}")

    # ───────────────────────────────────────────────────────────────────
    # Part 4: What uniquely characterizes traditional 互?
    # ───────────────────────────────────────────────────────────────────
    trad_h = frozenset([(0,0,0), (1,0,0), (0,1,1), (1,1,1)])
    trad_h_name = '{id,O,MI,OMI}'

    print(f"\n--- Which operations produce H = {trad_h_name}? ---")

    all_results = []
    all_results.extend([(r, 'consec-window') for r in consec_results])
    all_results.extend([(r, '4-line-window') for _, r in window_results])
    all_results.extend([(r, 'non-overlap') for _, _, r in non_overlap_results])

    # Deduplicate: the consecutive start=2 is the same as L2,L3,L4,L5 window
    trad_h_labels = set()
    trad_h_ops = []
    for r, src in all_results:
        if r['h_like'] == trad_h and r['label'] not in trad_h_labels:
            trad_h_labels.add(r['label'])
            trad_h_ops.append((r, src))
    print(f"  Distinct operations with H = {trad_h_name}: {len(trad_h_ops)}")
    for r, src in trad_h_ops:
        trad = " ← TRADITIONAL" if 'start=2' in r['label'] else ""
        print(f"    {r['label']} ({src}), idem={r['idempotent']}{trad}")

    # ───────────────────────────────────────────────────────────────────
    # Summary
    # ───────────────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")

    # Classify all distinct H-like subgroups
    all_h_likes = set()
    for r, _ in all_results:
        all_h_likes.add(r['h_like'])

    trad_result = consec_results[1]  # start=2

    print(f"""
Traditional 互 = consecutive window at L2-L5:
  Lower=(L2,L3,L4), Upper=(L3,L4,L5)
  Image: {trad_result['image_size']}/64
  Kernel: {{{','.join(NAMES[k] for k in sorted(trad_result['kernel']))}}}
  H-like: {{{','.join(NAMES[k] for k in sorted(trad_result['h_like']))}}}
  Idempotent: {trad_result['idempotent']}

Three consecutive-window options (start 1, 2, 3):""")
    for i, r in enumerate(consec_results):
        h_str = ','.join(NAMES[k] for k in sorted(r['h_like']))
        print(f"  start={i+1}: H={{{h_str}}}, "
              f"kernel={{{','.join(NAMES[k] for k in sorted(r['kernel']))}}}")

    print(f"""
Key findings:
  1. Only start=2 (traditional 互) has kernel {{id,O}}.
     Start=1 and start=3 have trivial kernel — no position is invisible.
     This is because start=2 uniquely erases L1,L6 (the outer pair),
     which form the O palindromic position.

  2. Only start=2 has H = {trad_h_name}.
     Start=1 and start=3 have H = {{id,OMI}} (only complement).
     The larger H comes from the kernel: O is invisible, and MI maps
     to complement. Together: {{id, O, MI, OMI}} = ker × {{id, MI}}.

  3. The traditional 互 is NOT idempotent: 互(互(h)) ≠ 互(h) in general.
     The second application further erases structure.

  4. Among all 4-line window operations, ONLY the consecutive window
     L2-L5 produces the traditional H. It is the unique operation with
     kernel = {{id,O}} (erasing exactly the outer palindromic position).

  → The nuclear operation is determined by: "erase the outermost pair."
    This is the simplest positional choice and the only one that makes
    a full palindromic position (O) invisible. The resulting H = {trad_h_name}
    is a consequence, not a design target.
""")


if __name__ == '__main__':
    main()
