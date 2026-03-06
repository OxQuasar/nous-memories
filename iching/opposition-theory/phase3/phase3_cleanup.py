#!/usr/bin/env python3
"""
Phase 3 Cleanup: Confirm failure sets and produce summary.

1. Characterize the 8 commutativity-breaking hexagrams
2. Confirm failure set = {non-palindromic x : nuclear core L2-L5 is palindromic}
3. Confirm (1,0,0)-signature identity: hugua(x) = hugua(rev(x)) iff sig = (1,0,0)
4. Write phase3_summary.md

Encoding: L1 = bit 0 (bottom), L6 = bit 5 (top).
"""

from pathlib import Path

# ─── Bit operations ──────────────────────────────────────────────────────────

N = 6
NUM_STATES = 1 << N
MASK_ALL = (1 << N) - 1

def bit(x, i):
    return (x >> i) & 1

def popcount(x):
    return bin(x).count('1')

def reverse6(x):
    r = 0
    for i in range(N):
        if x & (1 << i):
            r |= 1 << (N - 1 - i)
    return r

def hugua(x):
    """互卦: L2,L3,L4,L3,L4,L5 from bits 1,2,3,2,3,4."""
    L2, L3, L4, L5 = bit(x, 1), bit(x, 2), bit(x, 3), bit(x, 4)
    return L2 | (L3 << 1) | (L4 << 2) | (L3 << 3) | (L4 << 4) | (L5 << 5)

def kw_partner(x):
    rev = reverse6(x)
    return (x ^ MASK_ALL) if rev == x else rev

def is_palindrome6(x):
    return reverse6(x) == x

def signature(x, y):
    """Mirror-pair signature (O,M,I) of a KW pair's XOR mask."""
    m = x ^ y
    return (bit(m, 0), bit(m, 1), bit(m, 2))

def nuclear_palindromic(x):
    """Is the nuclear core L2-L3-L4-L5 (bits 1,2,3,4) palindromic? i.e., L2=L5 and L3=L4."""
    return bit(x, 1) == bit(x, 4) and bit(x, 2) == bit(x, 3)

def fmt6(x):
    return format(x, '06b')

# ─── Precompute ──────────────────────────────────────────────────────────────

HUGUA = [hugua(x) for x in range(NUM_STATES)]

# ─── 1. The 8 commutativity-breaking hexagrams ──────────────────────────────

print("=" * 70)
print("1. THE 8 COMMUTATIVITY-BREAKING HEXAGRAMS")
print("=" * 70)

failures = []
for x in range(NUM_STATES):
    lhs = HUGUA[kw_partner(x)]
    rhs = kw_partner(HUGUA[x])
    if lhs != rhs:
        failures.append(x)

print(f"\n{len(failures)} hexagrams where hugua(kw(x)) ≠ kw(hugua(x)):\n")
print(f"{'x':>4} {'bin':>8} {'pal?':>5} {'kw(x)':>8} {'sig':>8} "
      f"{'hugua(x)':>10} {'hg pal?':>8} {'hg(kw(x))':>10} {'kw(hg(x))':>10} "
      f"{'nuc pal?':>9}")
for x in failures:
    kw_x = kw_partner(x)
    hx = HUGUA[x]
    sig = signature(x, kw_x)
    print(f"{x:>4} {fmt6(x):>8} {str(is_palindrome6(x)):>5} {fmt6(kw_x):>8} {str(sig):>8} "
          f"{fmt6(hx):>10} {str(is_palindrome6(hx)):>8} {fmt6(HUGUA[kw_x]):>10} {fmt6(kw_partner(hx)):>10} "
          f"{str(nuclear_palindromic(x)):>9}")

# ─── 2. Confirm structural class ────────────────────────────────────────────

print("\n" + "=" * 70)
print("2. CONFIRM: failures = {non-palindromic x : nuclear core is palindromic}")
print("=" * 70)

predicted = {x for x in range(NUM_STATES)
             if not is_palindrome6(x) and nuclear_palindromic(x)}
actual = set(failures)

print(f"\nNon-palindromic with palindromic nuclear core: {len(predicted)}")
print(f"Commutativity failures: {len(actual)}")
print(f"Sets equal: {predicted == actual}")

if predicted != actual:
    print(f"  Predicted \\ actual: {predicted - actual}")
    print(f"  Actual \\ predicted: {actual - predicted}")

# Also verify: all failures have signature (1,0,0)
sigs = {signature(x, kw_partner(x)) for x in failures}
print(f"\nAll failure signatures: {sigs}")
print(f"All are (1,0,0): {sigs == {(1, 0, 0)}}")

# ─── 3. Confirm: hugua(x) = hugua(rev(x)) iff sig = (1,0,0) ────────────────

print("\n" + "=" * 70)
print("3. CONFIRM: hugua(x) = hugua(rev(x)) iff signature (1,0,0)")
print("=" * 70)

# For all 56 non-palindromic hexagrams (28 pairs × 2):
collapse_set = set()
non_collapse_set = set()
for x in range(NUM_STATES):
    if is_palindrome6(x):
        continue
    rev_x = reverse6(x)
    if HUGUA[x] == HUGUA[rev_x]:
        collapse_set.add(min(x, rev_x))  # canonical pair rep
    else:
        non_collapse_set.add(min(x, rev_x))

# Pairs with signature (1,0,0)
sig100_pairs = set()
for x in range(NUM_STATES):
    if is_palindrome6(x):
        continue
    rev_x = reverse6(x)
    if x > rev_x:
        continue
    sig = signature(x, rev_x)
    if sig == (1, 0, 0):
        sig100_pairs.add(x)

print(f"\nReversal pairs where hugua(x) = hugua(rev(x)): {len(collapse_set)}")
print(f"  Pairs: {sorted(collapse_set)}")
print(f"Reversal pairs with signature (1,0,0): {len(sig100_pairs)}")
print(f"  Pairs: {sorted(sig100_pairs)}")
print(f"Sets equal: {collapse_set == sig100_pairs}")

# Show the 4 collapsing pairs explicitly
print(f"\nThe {len(collapse_set)} pairs where 互卦 erases opposition:")
print(f"{'a':>8} {'b=rev(a)':>10} {'sig':>8} {'hugua(a)':>10} {'hugua(b)':>10} {'equal?':>7}")
for a in sorted(collapse_set):
    b = reverse6(a)
    ha, hb = HUGUA[a], HUGUA[b]
    sig = signature(a, b)
    print(f"{fmt6(a):>8} {fmt6(b):>10} {str(sig):>8} {fmt6(ha):>10} {fmt6(hb):>10} {str(ha == hb):>7}")

# ─── 4. Write phase3_summary.md ─────────────────────────────────────────────

print("\n" + "=" * 70)
print("4. WRITING PHASE 3 SUMMARY")
print("=" * 70)

lines = []
w = lines.append

w("# Phase 3 Summary: Nuclear Trigrams and the L3|L4 Membrane\n")

w("## What Was Tested\n")
w("Three analyses probing whether the nuclear/trigram decomposition carries")
w("independent opposition information beyond the hexagram-level pairing:\n")
w("1. **Trigram decomposition** (`trigram_decomposition.py`): Full trigram and nuclear trigram")
w("   extraction for all 32 KW pairs. Relationship classification, XOR mask analysis,")
w("   weight preservation at each sub-hexagram level.")
w("2. **互卦 self-similarity** (`hugua_test.py`): Does the 互卦 projection (nuclear core → hexagram)")
w("   preserve the KW pairing? Commutativity test, image structure, weight analysis.")
w("3. **Phase 3 cleanup** (`phase3_cleanup.py`): Confirm failure set identity, close loose ends.\n")

w("---\n")

w("## Main Result: The Nuclear Level Is a Projection, Not Independent\n")
w("The nuclear trigram decomposition carries no opposition information beyond what the")
w("hexagram-level mirror-pair signature already determines. Every nuclear-level property")
w("(XOR masks, weight differences, relationship types) is derivable from the hexagram-level")
w("signature (O,M,I) by erasing the outer component.\n")
w("The 互卦 map is a lossy projection: 64 → 16 hexagrams, 7 signature masks → 3 + identity.")
w("It preserves 28 of 32 KW pairs and nearly commutes with the pairing (56 of 64).\n")

w("---\n")

w("## Finding 1: Depth-Function Separation\n")
w("The 6 line positions separate into three depth layers with distinct roles under the KW pairing:\n")
w("| Layer | Lines | Mirror pair | Role under KW |")
w("|-------|-------|-------------|---------------|")
w("| Outer | L1, L6 | O | **Weight buffer.** Erased by 互卦. Contributes to opposition")
w("  strength but not to nuclear structure. When O is the only differing pair (sig (1,0,0)),")
w("  opposition is invisible at the nuclear level. |")
w("| Middle | L2, L5 | M | **Bridge.** Each line belongs to exactly one nuclear trigram")
w("  (L2 → lower_nuc, L5 → upper_nuc). Preserved by 互卦. |")
w("| Inner | L3, L4 | I | **Opposition core.** Both lines belong to BOTH nuclear trigrams.")
w("  Doubled by 互卦. The structural anchor — the site where mirror-pair geometry")
w("  and trigram geometry maximally non-align. |")
w("")
w("This separation is not imposed — it emerges from the interaction of two independent")
w("geometric structures (mirror-pair partition and trigram partition) at the L3|L4 boundary.\n")

w("---\n")

w("## Finding 2: The Palindrome Phase Boundary\n")
w("**8 hexagrams** (forming 4 KW pairs) cross the palindrome threshold under 互卦:")
w("they are non-palindromic, but their nuclear core (L2-L5) IS palindromic (L2=L5 and L3=L4).\n")
w("These are exactly the hexagrams with mirror-pair signature (1,0,0) —")
w("opposition lives entirely in the outer pair, which 互卦 discards.\n")

w("| x | kw(x) | Signature | hugua(x) | hg palindromic? | hugua(kw(x)) | kw(hugua(x)) |")
w("|---|-------|-----------|----------|-----------------|--------------|--------------|")
for x in sorted(failures):
    kw_x = kw_partner(x)
    hx = HUGUA[x]
    sig = signature(x, kw_x)
    w(f"| {fmt6(x)} | {fmt6(kw_x)} | {sig} | {fmt6(hx)} | {is_palindrome6(hx)} "
      f"| {fmt6(HUGUA[kw_x])} | {fmt6(kw_partner(hx))} |")

w("")
w("**Confirmation:** The failure set equals {non-palindromic x : L2=L5 and L3=L4} exactly.")
w(f"Predicted set size: {len(predicted)}, actual failure set size: {len(actual)}, "
  f"match: **{predicted == actual}**.\n")

w("**Mechanism:** For these hexagrams, the KW rule applies reversal (x is non-palindromic),")
w("but 互卦 maps to a palindromic hexagram where the KW rule would apply complement.")
w("The two paths through the commutativity diagram use different branches of the KW rule:")
w("- hugua(kw(x)) = hugua(rev(x)) = rev(hugua(x)) = hugua(x)  ← palindromic, so rev is identity")
w("- kw(hugua(x)) = comp(hugua(x))  ← because hugua(x) is palindromic")
w("- Result: hugua(x) ≠ comp(hugua(x))  ← commutativity breaks\n")

w("---\n")

w("## Finding 3: Weight Preservation Degrades at Nuclear Level\n")
w("| Level | Mean |Δw| (all 32 pairs) | Mean |Δw| (28 reversal) | Correlation r |")
w("|-------|-------------------------|------------------------|---------------|")
w("| Full hexagram | 0.375 | 0.000 | +0.516 |")
w("| Nuclear trigram | 0.750 | 0.571 | +0.277 |")
w("| Standard trigram | 1.125 | 1.071 | +0.024 |")
w("")
w("Reversal preserves hexagram-level weight perfectly (Δw = 0 for all 28 pairs).")
w("At sub-hexagram levels, the swap+reverse operation redistributes weight between")
w("upper and lower components. Nuclear trigrams are more weight-stable than standard")
w("trigrams (0.57 vs 1.07) because they share the inner pair {L3, L4},")
w("which dampens the redistribution.\n")
w("The outer pair acts as a weight buffer: removing it (via 互卦) increases mean |Δw|")
w("from 0.375 to 0.500 for palindromic pairs, because L1 and L6 partially absorb")
w("the weight disruption that complement imposes.\n")

w("---\n")

w("## Finding 4: 互卦 Map Structure\n")
w("| Property | Value |")
w("|----------|-------|")
w("| Image size | 16 of 64 (constrained: bit1=bit3, bit2=bit4) |")
w("| Preimage size | Uniform: 4 hexagrams per image element |")
w("| Fixed points | 2 (000000, 111111 — all bits equal) |")
w("| Idempotent | No — hugua² converges to 4 hexagrams (L3,L4 alternation) |")
w("| KW pairs preserved | 28 of 32 (87.5%) |")
w("| Commutativity | 56 of 64 (87.5%) — fails at palindrome boundary |")
w("| 互卦 XOR masks | 3 nonzero + identity (down from 7 hex-level) |")
w("")
w("The 互卦 is a 4:1 compression that erases the outer pair and doubles the inner pair.")
w("It is NOT idempotent: iterated application converges in 2 steps to the 4-element set")
w("{000000, 010101, 101010, 111111} — pure L3,L4 alternation.\n")

w("---\n")

w("## Mask Vocabulary Reduction Under 互卦\n")
w("| Hex signature | Hex mask | 互卦 XOR |")
w("|--------------|----------|---------|")
w("| (0,0,1) | 001100 | 011110 |")
w("| (1,0,1) | 101101 | 011110 |")
w("| (0,1,0) | 010010 | 100001 |")
w("| (1,1,0) | 110011 | 100001 |")
w("| (0,1,1) | 011110 | 111111 |")
w("| (1,1,1) | 111111 | 111111 |")
w("| **(1,0,0)** | **100001** | **000000** |")
w("")
w("Pairs differing only in O-bit collapse to the same 互卦 XOR.")
w("Signature (1,0,0) collapses to identity — all opposition erased.\n")

w("---\n")

w("## Status\n")
w("**Phase 3: Complete.**\n")
w("No new opposition measures emerge from the nuclear/trigram decomposition.")
w("The nuclear level is a strict projection of the hexagram level, with the outer pair erased.\n")
w("One structural insight carries forward: the **depth-function separation** (outer = buffer,")
w("inner = core) may connect to the 体/用 (tǐ/yòng) distinction in Phase 4,")
w("where the nuclear trigram traditionally determines the 体 (substance) of a hexagram.\n")

w("### Open questions resolved")
w("- **Q5 from plan (nuclear trigram boundary):** The L3|L4 membrane does not carry")
w("  independent opposition information. It is the site of maximal geometric non-alignment,")
w("  but the opposition structure there is fully determined by the hexagram-level signature.\n")

w("### Files")
w("| File | Description |")
w("|------|-------------|")
w("| `trigram_decomposition.py` | Trigram/nuclear extraction and analysis |")
w("| `trigram_decomposition_results.md` | Full 32-pair tables + summary statistics |")
w("| `hugua_test.py` | 互卦 self-similarity and commutativity test |")
w("| `hugua_results.md` | 互卦 pair table + structural analysis |")
w("| `phase3_cleanup.py` | Failure set confirmation (this script) |")
w("| `phase3_summary.md` | This summary document |")

md = '\n'.join(lines)
out_path = Path(__file__).parent / "phase3_summary.md"
out_path.write_text(md)
print(f"\nWritten to {out_path}")


if __name__ == '__main__':
    pass  # Script runs at module level
