"""
Thread A Step 2+3: For a given Eulerian orbit path, enumerate/count valid 
hexagram-level completions.

Structure:
- Each orbit has 8 hexagrams organized into 4 pairs (perfect matching).
- The Eulerian path visits each orbit exactly 4 times.
- At each visit, we must assign a pair-slot (which of the 4 pairs) and an 
  orientation (which hex comes first in the pair).
- The bridge constraint: hex[2k+1] must connect to hex[2k+2] via the specific
  bridge mask for that position. Since the orbit walk determines which orbit
  each pair occupies, we need the specific hexagram at position 2k+1 (second 
  of pair k) to be related to the hexagram at position 2k+2 (first of pair k+1)
  by the bridge XOR mask.

Actually, the bridge mask is determined by the hexagram pair, not predetermined.
Let me re-read the structure carefully.

The constraint is:
1. Each pair uses a generator mask (O, M, I, OM, OI, MI, OMI, or id)
2. The pair mask is orbit-determined: within orbit O, pair (a,b) means a⊕b = mask
3. The bridge between pair k and pair k+1 goes from hex[2k+1] to hex[2k+2]
4. The bridge orbit transition is determined by the Eulerian path
5. The bridge MASK (6-bit XOR) = orbit_change ⊕ kernel_dressing
6. The kernel dressing is a free choice from the 8 generators

So: given an Eulerian orbit path, we need to:
- At each orbit visit, choose which pair to use (4 choices per visit, must use each pair exactly once per orbit)
- Choose orientation for each pair (2 choices)
- Check that the bridge connecting consecutive pairs is valid (the hex at end of pair k must connect to hex at start of pair k+1)

Let's formalize: hex[2k+1] ⊕ hex[2k+2] = bridge_mask. The bridge_mask decomposes as
orbit_Δ ⊕ kernel. The orbit_Δ is fixed by the Eulerian path. The kernel can be any
of the 8 generators. But the kernel is determined by which specific hexagrams are 
at positions 2k+1 and 2k+2.

So the question is: for a given Eulerian path, how many ways can we assign pairs+orientations
such that all bridges are consistent?

Let me think about what "consistent" means here. Actually, ANY assignment of pairs+orientations
is valid as long as:
1. Each pair-slot in each orbit is used exactly once
2. The resulting hexagram sequence visits all 64 hexagrams exactly once (which is automatic from #1)

Wait — condition 2 IS automatic from condition 1, since each orbit has 4 pairs covering 
all 8 hexagrams, and the Eulerian path visits each orbit exactly 4 times. So using each 
pair-slot exactly once guarantees all 64 hexagrams appear.

But are there additional constraints? Let me re-check: the bridge is just the transition 
between hex[2k+1] and hex[2k+2]. There's no constraint that this transition must be a 
specific mask — ANY mask works for the hexagram-level sequence. The orbit transition is 
already handled by the Eulerian path.

So the ONLY constraint is:
1. At each orbit visit, assign a distinct pair-slot (4! = 24 per orbit)
2. Choose orientation for each pair (2^4 = 16 per orbit)
3. These choices are INDEPENDENT between orbits

Total per Eulerian path = (4! × 2^4)^8 = (24 × 16)^8 = 384^8 ≈ 1.1 × 10^20

Hmm, that seems too large. Let me reconsider whether there are additional constraints.

Actually, I think I'm missing something. The bridge between pair k and pair k+1 
IS constrained: it must be a valid transition in the 6-cube. But EVERY pair of 
hexagrams defines a unique 6-bit XOR — there's no constraint that the XOR must be 
a generator mask. The generator mask constraint only applies to PAIRS (hex[2k] and 
hex[2k+1]), not to bridges.

Actually wait — the original King Wen structure requires that each pair (1-2, 3-4, etc.) 
consists of two hexagrams related by one of the 8 generator masks. This is the "paired" 
constraint. But the bridge between pair k and pair k+1 can be ANY hexagram transition.

So if the ONLY constraints are:
1. Hamiltonian: all 64 hexagrams visited once (automatic from pair assignment)
2. Paired: each pair uses a generator mask (guaranteed since pairs are within orbits)
3. Eulerian: bridges form Eulerian path (given by the orbit path)
4. Endpoints: start Qian orbit, end Tai orbit (given by the orbit path)

Then the number of valid completions per Eulerian path is indeed 
(4! × 2^4)^8 = 384^8 ≈ 1.1 × 10^20.

But wait — within each orbit, the 4 pairs are determined by the orbit's pair structure.
Let me check: does each orbit have a UNIQUE set of 4 pairs, or can the pairing itself vary?
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
from itertools import permutations, product

DIMS = 6
M = all_bits()

ORBIT_NAMES = {
    (0,0,0): 'Qian', (1,1,0): 'Zhun', (1,0,1): 'Xu', (0,1,0): 'Shi',
    (0,0,1): 'XChu', (1,1,1): 'Tai', (1,0,0): 'Bo', (0,1,1): 'WWang',
}

MASK_NAMES = {
    (0,0,0,0,0,0): 'id', (1,0,0,0,0,1): 'O', (0,1,0,0,1,0): 'M',
    (0,0,1,1,0,0): 'I', (1,1,0,0,1,1): 'OM', (1,0,1,1,0,1): 'OI',
    (0,1,1,1,1,0): 'MI', (1,1,1,1,1,1): 'OMI',
}

GEN_FLIPS = {'O': [0, 5], 'M': [1, 4], 'I': [2, 3]}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

def apply_gens(h, gens):
    h = list(h)
    for g in gens:
        for idx in GEN_FLIPS[g]:
            h[idx] = 1 - h[idx]
    return tuple(h)

# Build orbits
def build_orbits():
    GROUP = [frozenset(), frozenset({'O'}), frozenset({'M'}), frozenset({'I'}),
             frozenset({'O','M'}), frozenset({'O','I'}), frozenset({'M','I'}),
             frozenset({'O','M','I'})]
    seen = set()
    orbits = {}  # sig -> {hexagram: kw_index}
    for i in range(64):
        h = tuple(M[i])
        if h in seen:
            continue
        sig = xor_sig(h)
        orbit = {}
        for g in GROUP:
            gh = apply_gens(h, g)
            for j in range(64):
                if tuple(M[j]) == gh:
                    orbit[gh] = j
                    seen.add(gh)
                    break
        orbits[sig] = orbit
    return orbits

orbits = build_orbits()

print("Orbits:")
for sig in sorted(orbits.keys()):
    hexes = orbits[sig]
    kw_nums = sorted(idx + 1 for idx in hexes.values())
    print(f"  {ORBIT_NAMES[sig]} {sig}: KW# {kw_nums}")

# Build KW pair structure
# KW pairs: (hex[0], hex[1]), (hex[2], hex[3]), ..., (hex[62], hex[63])
kw_pairs = []
for k in range(32):
    a = tuple(M[2*k])
    b = tuple(M[2*k+1])
    xor = tuple(a[i] ^ b[i] for i in range(DIMS))
    kw_pairs.append({
        'a': a, 'b': b, 'mask': xor,
        'mask_name': MASK_NAMES.get(xor, '???'),
        'orbit': xor_sig(a),
        'kw_a': 2*k + 1, 'kw_b': 2*k + 2,
    })

# How many pairs per orbit? And which generator masks?
orbit_pairs = defaultdict(list)
for p in kw_pairs:
    orbit_pairs[p['orbit']].append(p)

print(f"\nPair structure per orbit:")
for sig in sorted(orbit_pairs.keys()):
    pairs = orbit_pairs[sig]
    masks = [p['mask_name'] for p in pairs]
    print(f"  {ORBIT_NAMES[sig]}: {len(pairs)} pairs, masks = {masks}")

# Key question: Is the pairing within each orbit UNIQUE or could we re-pair?
# Each orbit has 8 hexagrams. A "valid pairing" = perfect matching using generator masks.
# How many valid perfect matchings exist per orbit?

print(f"\n{'='*70}")
print("COUNTING VALID PERFECT MATCHINGS PER ORBIT")
print(f"{'='*70}")

for sig in sorted(orbits.keys()):
    hexes = list(orbits[sig].keys())
    n = len(hexes)  # 8
    
    # Find ALL valid perfect matchings using generator masks
    # A pair (a, b) is valid iff a⊕b is one of the 8 generator masks
    valid_pairs = []
    for i in range(n):
        for j in range(i+1, n):
            xor = tuple(hexes[i][d] ^ hexes[j][d] for d in range(DIMS))
            if xor in MASK_NAMES:
                valid_pairs.append((i, j, MASK_NAMES[xor]))
    
    print(f"\n  {ORBIT_NAMES[sig]}: {len(valid_pairs)} valid pairs among 8 hexagrams")
    
    # Enumerate perfect matchings (4 pairs covering all 8 vertices)
    # Use recursive backtracking on the valid_pairs
    matchings = []
    
    def find_matchings(remaining_verts, current_matching):
        if not remaining_verts:
            matchings.append(list(current_matching))
            return
        # Pick the smallest remaining vertex, try all valid pairs containing it
        v = min(remaining_verts)
        for i, j, mask in valid_pairs:
            if i == v and j in remaining_verts:
                new_remaining = remaining_verts - {i, j}
                current_matching.append((i, j, mask))
                find_matchings(new_remaining, current_matching)
                current_matching.pop()
    
    find_matchings(set(range(n)), [])
    print(f"  Valid perfect matchings: {len(matchings)}")
    
    for mi, matching in enumerate(matchings):
        masks = [m[2] for m in matching]
        kw_match = all(any(
            (hexes[i] == p['a'] and hexes[j] == p['b']) or 
            (hexes[j] == p['a'] and hexes[i] == p['b'])
            for p in orbit_pairs[sig]) for i, j, _ in matching)
        marker = " ★ KW" if kw_match else ""
        print(f"    M{mi}: {masks}{marker}")

# So within each orbit, there may be multiple valid perfect matchings!
# The "paired" constraint doesn't uniquely determine the pairing.

print(f"\n{'='*70}")
print("COMPLETION COUNT ANALYSIS")
print(f"{'='*70}")

# For each orbit, the number of valid perfect matchings
# For each matching, the number of pair orderings = 4! (which pair goes where)
# For each pair, orientation = 2 (which hex comes first)
# Total per orbit = matchings × 4! × 2^4

total_per_eulerian = 1
for sig in sorted(orbits.keys()):
    hexes = list(orbits[sig].keys())
    n = len(hexes)
    
    valid_pairs = []
    for i in range(n):
        for j in range(i+1, n):
            xor = tuple(hexes[i][d] ^ hexes[j][d] for d in range(DIMS))
            if xor in MASK_NAMES:
                valid_pairs.append((i, j))
    
    matchings_count = [0]
    def count_matchings(remaining):
        if not remaining:
            matchings_count[0] += 1
            return
        v = min(remaining)
        for i, j in valid_pairs:
            if i == v and j in remaining:
                count_matchings(remaining - {i, j})
    
    count_matchings(set(range(n)))
    
    orbit_completions = matchings_count[0] * 24 * 16  # 4! orderings × 2^4 orientations
    total_per_eulerian *= orbit_completions
    print(f"  {ORBIT_NAMES[sig]:>6s}: {matchings_count[0]} matchings × 24 orderings × 16 orientations = {orbit_completions}")

print(f"\nTotal completions per Eulerian path: {total_per_eulerian}")
print(f"  = {total_per_eulerian:.3e}")

# Total valid sequences = Eulerian paths × completions per path
total_eulerian = 150_955_488
total_sequences = total_eulerian * total_per_eulerian
print(f"\nTotal Eulerian paths: {total_eulerian}")
print(f"Total valid KW-type sequences: {total_sequences}")
print(f"  = {total_sequences:.3e}")

# But wait — are the matchings independent across orbits?
# Yes! Each orbit's hexagrams are completely disjoint, so the matching
# choices in one orbit don't constrain the choices in another.

# However, we're over-counting because we haven't checked the bridge constraints.
# The bridge between pair k and pair k+1 just needs hex[2k+1] and hex[2k+2] to exist.
# There's no constraint on what the bridge XOR mask is — ANY hexagram can follow any other.
# So the bridges DON'T add constraints beyond what the orbit path already provides.

# Actually, wait. Let me reconsider. The constraint is that the 31 bridges must 
# form an Eulerian path through the orbit graph. The orbit of each pair is determined
# by which orbit we assign it to (via the Eulerian path). But the specific bridge 
# orbit transition is already determined by the Eulerian path choice. The bridge XOR 
# mask = orbit_Δ ⊕ kernel_dressing, where kernel_dressing is ANY generator. Since
# any kernel dressing is valid (it's determined by the hexagram choice), there's no
# additional constraint.

# So: the orbit-level Eulerian path and the within-orbit choices are INDEPENDENT.
# The total count is simply Eulerian_paths × completions_per_path.

print(f"\n{'='*70}")
print("INDEPENDENCE VERIFICATION")
print(f"{'='*70}")
print("Are bridge constraints satisfied for ANY pair/orientation assignment?")
print("Testing with the KW Eulerian path and random completions...")

import random
rng = random.Random(42)

# The KW Eulerian orbit path
kw_orbit_walk = []
for k in range(32):
    h = tuple(M[2*k])
    kw_orbit_walk.append(xor_sig(h))

# For each orbit, build the set of valid matchings with actual hexagrams
orbit_matchings = {}
for sig in orbits:
    hexes = sorted(orbits[sig].keys())
    valid_pairs = []
    for i in range(len(hexes)):
        for j in range(i+1, len(hexes)):
            xor = tuple(hexes[i][d] ^ hexes[j][d] for d in range(DIMS))
            if xor in MASK_NAMES:
                valid_pairs.append((hexes[i], hexes[j]))
    
    # Build all matchings
    matchings = []
    def find_m(remaining_hexes, current):
        if not remaining_hexes:
            matchings.append(list(current))
            return
        v = min(remaining_hexes)
        for a, b in valid_pairs:
            if a == v and b in remaining_hexes:
                find_m(remaining_hexes - {a, b}, current + [(a, b)])
            elif b == v and a in remaining_hexes:
                find_m(remaining_hexes - {a, b}, current + [(a, b)])
    
    find_m(set(hexes), [])
    orbit_matchings[sig] = matchings

# Check: for a random completion, is the resulting 64-hex sequence valid?
n_valid = 0
n_tests = 1000

for test in range(n_tests):
    # Random completion of the KW Eulerian path
    sequence = []
    
    # For each orbit, pick a random matching
    orbit_match_choice = {}
    orbit_pair_queue = {}
    for sig in orbits:
        matching = rng.choice(orbit_matchings[sig])
        pairs = list(matching)
        rng.shuffle(pairs)
        # Random orientations
        oriented_pairs = []
        for a, b in pairs:
            if rng.random() < 0.5:
                oriented_pairs.append((a, b))
            else:
                oriented_pairs.append((b, a))
        orbit_pair_queue[sig] = list(oriented_pairs)
    
    # Assign pairs to orbit visits according to the Eulerian path
    orbit_visit_count = defaultdict(int)
    for k in range(32):
        sig = kw_orbit_walk[k]
        visit_idx = orbit_visit_count[sig]
        orbit_visit_count[sig] += 1
        pair = orbit_pair_queue[sig][visit_idx]
        sequence.extend(pair)
    
    # Check: all 64 hexagrams present?
    hex_set = set(tuple(h) for h in sequence)
    if len(hex_set) != 64:
        print(f"  Test {test}: DUPLICATE HEXAGRAMS! Only {len(hex_set)} unique")
        continue
    
    # Check: all pairs use generator masks?
    all_gen_masks = True
    for k in range(32):
        a = sequence[2*k]
        b = sequence[2*k + 1]
        xor = tuple(a[d] ^ b[d] for d in range(DIMS))
        if xor not in MASK_NAMES:
            all_gen_masks = False
            break
    
    if not all_gen_masks:
        print(f"  Test {test}: NON-GENERATOR PAIR MASK!")
        continue
    
    # Check: bridges form the correct Eulerian orbit path?
    correct_path = True
    for k in range(31):
        a = sequence[2*k + 1]
        b = sequence[2*k + 2]
        sig_a = xor_sig(a)
        sig_b = xor_sig(b)
        expected_a = kw_orbit_walk[k]
        expected_b = kw_orbit_walk[k+1]
        if sig_a != expected_a or sig_b != expected_b:
            correct_path = False
            break
    
    if not correct_path:
        print(f"  Test {test}: WRONG ORBIT PATH!")
        continue
    
    n_valid += 1

print(f"\n  {n_valid}/{n_tests} random completions are valid")
print(f"  (Expected: 100% if our analysis is correct)")

print(f"\n{'='*70}")
print("FINAL COUNT")
print(f"{'='*70}")
print(f"Eulerian orbit paths: 150,955,488 (exact, BEST theorem)")
print(f"Completions per path: {total_per_eulerian} (exact)")
print(f"Total valid KW-type sequences: {total_sequences:.6e}")

# Let's also factor this more carefully
from math import log10
log_total = log10(total_eulerian) + log10(total_per_eulerian)
print(f"  = 10^{log_total:.1f}")
print(f"\nFor reference:")
print(f"  64! ≈ 10^89")
print(f"  Valid sequences ≈ 10^{log_total:.1f}")
print(f"  Fraction of all permutations: 10^{log_total - 89:.1f}")
