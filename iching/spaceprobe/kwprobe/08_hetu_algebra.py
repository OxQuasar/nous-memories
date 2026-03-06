"""
Quick probe: He Tu pairing as algebraic operation on trigrams.

He Tu: Kan(010)↔Qian(111), Kun(000)↔Dui(110), Zhen(100)↔Gen(001), Xun(011)↔Li(101)

What operation relates these?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

from cycle_algebra import TRIGRAM_NAMES

# He Tu pairs
hetu = {
    0b010: 0b111,  # Kan↔Qian
    0b000: 0b110,  # Kun↔Dui
    0b100: 0b001,  # Zhen↔Gen
    0b011: 0b101,  # Xun↔Li
}
# Make symmetric
hetu.update({v: k for k, v in hetu.items()})

# Fu Xi (complement) pairs
fuxi = {t: t ^ 0b111 for t in range(8)}

print("=" * 60)
print("HE TU AS PERMUTATION")
print("=" * 60)

# He Tu as a permutation of 8 trigrams
print(f"\n  He Tu permutation:")
for t in range(8):
    print(f"    {TRIGRAM_NAMES[t]:4s} ({t:03b}) → {TRIGRAM_NAMES[hetu[t]]:4s} ({hetu[t]:03b})")

# What is He Tu ∘ Fu Xi?
print(f"\n  He Tu ∘ Fu Xi (apply Fu Xi first, then He Tu):")
for t in range(8):
    fx = fuxi[t]
    ht_fx = hetu[fx]
    print(f"    {TRIGRAM_NAMES[t]:4s} → FuXi → {TRIGRAM_NAMES[fx]:4s} → HeTu → {TRIGRAM_NAMES[ht_fx]:4s}")

# Compute: what single-bit operations relate each He Tu pair?
print(f"\n  He Tu XOR patterns:")
for t in range(8):
    xor = t ^ hetu[t]
    bits = [(xor >> i) & 1 for i in range(3)]
    print(f"    {TRIGRAM_NAMES[t]:4s}↔{TRIGRAM_NAMES[hetu[t]]:4s}: XOR = {xor:03b} ({bits})")

# He Tu as composition of operations
# Check: is He Tu = some combination of bit operations?
# Let's check: He Tu(t) = reverse(t) XOR something?
print(f"\n  He Tu vs reverse:")
for t in range(8):
    rev = ((t >> 2) & 1) | (((t >> 1) & 1) << 1) | ((t & 1) << 2)
    print(f"    {TRIGRAM_NAMES[t]:4s}: reverse={TRIGRAM_NAMES[rev]:4s}, "
          f"hetu={TRIGRAM_NAMES[hetu[t]]:4s}, "
          f"reverse_xor_hetu={rev ^ hetu[t]:03b}")

# Check: He Tu(t) = complement(reverse(t))?
print(f"\n  He Tu vs complement(reverse):")
for t in range(8):
    rev = ((t >> 2) & 1) | (((t >> 1) & 1) << 1) | ((t & 1) << 2)
    comp_rev = rev ^ 0b111
    match = (comp_rev == hetu[t])
    print(f"    {TRIGRAM_NAMES[t]:4s}: comp(rev)={TRIGRAM_NAMES[comp_rev]:4s}, "
          f"hetu={TRIGRAM_NAMES[hetu[t]]:4s} {'✓' if match else '✗'}")

# Check if He Tu relates to swapping specific bits
# He Tu seems to: swap bit0 and bit2, then flip bit1?
# Test: swap outer bits, flip middle
print(f"\n  Test: swap bits 0,2 then flip bit 1:")
for t in range(8):
    b0, b1, b2 = t & 1, (t >> 1) & 1, (t >> 2) & 1
    result = (b2 << 0) | ((1 - b1) << 1) | (b0 << 2)
    match = (result == hetu[t])
    print(f"    {TRIGRAM_NAMES[t]:4s} ({t:03b}) → ({result:03b}) {TRIGRAM_NAMES[result]:4s} {'✓' if match else '✗'}")

# Test: flip all bits then reverse (= reverse complement)
print(f"\n  Test: reverse then complement:")
for t in range(8):
    rev = ((t >> 2) & 1) | (((t >> 1) & 1) << 1) | ((t & 1) << 2)
    result = rev ^ 0b111
    match = (result == hetu[t])
    print(f"    {TRIGRAM_NAMES[t]:4s}: rev_comp={TRIGRAM_NAMES[result]:4s} {'✓' if match else '✗'}")

# What IS the He Tu permutation in cycle notation?
print(f"\n  He Tu in cycle notation:")
visited = set()
cycles = []
for t in range(8):
    if t in visited:
        continue
    cycle = [t]
    visited.add(t)
    current = hetu[t]
    while current != t:
        cycle.append(current)
        visited.add(current)
        current = hetu[current]
    if len(cycle) > 1:
        cycles.append(tuple(cycle))

for cycle in cycles:
    names = [f"{TRIGRAM_NAMES[t]}({t:03b})" for t in cycle]
    print(f"    ({' '.join(names)})")

# He Tu composed with itself
print(f"\n  He Tu²:")
for t in range(8):
    ht2 = hetu[hetu[t]]
    print(f"    {TRIGRAM_NAMES[t]:4s} → {TRIGRAM_NAMES[ht2]:4s} {'(identity)' if ht2 == t else ''}")

print(f"\n  He Tu is an involution (He Tu² = identity).")

# ══════════════════════════════════════════════════════════════════════════════
# FACING-LINE VIEW OF HE TU
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 60}")
print("FACING-LINE VIEW OF HE TU")
print("=" * 60)

# For each He Tu pair, what happens to each line?
print(f"\n  Line-by-line transformation:")
for t in range(8):
    if t > hetu[t]:
        continue
    ht = hetu[t]
    b = [(t >> i) & 1 for i in range(3)]
    h = [(ht >> i) & 1 for i in range(3)]
    flips = [b[i] != h[i] for i in range(3)]
    print(f"    {TRIGRAM_NAMES[t]:4s}({b[2]}{b[1]}{b[0]}) ↔ "
          f"{TRIGRAM_NAMES[ht]:4s}({h[2]}{h[1]}{h[0]}): "
          f"flips={['top' if flips[2] else '', 'mid' if flips[1] else '', 'bot' if flips[0] else '']}")

# Key: top bit (facing line as lower) ALWAYS flips → He Tu always changes facing
# What about middle and bottom?

print(f"\n  Summary of He Tu flips:")
always_flips = [True, True, True]
for t in range(8):
    ht = hetu[t]
    for i in range(3):
        if ((t >> i) & 1) == ((ht >> i) & 1):
            always_flips[i] = False

print(f"    Bottom line (bit 0): always flips? {always_flips[0]}")
print(f"    Middle line (bit 1): always flips? {always_flips[1]}")
print(f"    Top line (bit 2):    always flips? {always_flips[2]}")

# What determines which other bits flip?
print(f"\n  Detailed flip pattern:")
for t in range(8):
    ht = hetu[t]
    for i in range(3):
        flipped = ((t >> i) & 1) != ((ht >> i) & 1)
        line_name = ['bot', 'mid', 'top'][i]
        if not flipped:
            print(f"    {TRIGRAM_NAMES[t]:4s}→{TRIGRAM_NAMES[ht]:4s}: {line_name} NOT flipped "
                  f"(value={(t>>i)&1})")
