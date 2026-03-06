#!/usr/bin/env python3
"""
Phase 2 Closure: Maximal Symmetry Group of the KW Pairing

Is Z₂² = {id, complement, reversal, comp∘rev} the largest subgroup
of the hyperoctahedral group B₆ under which the KW pairing is equivariant?

B₆ = signed permutations of 6 bit positions (order 2⁶ × 6! = 46080).
Each element: permute bit positions, then optionally flip each position.
"""

from itertools import permutations
from pathlib import Path

# ─── Constants ────────────────────────────────────────────────────────────────

N = 6
NUM_STATES = 1 << N
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


# ─── KW pairing ──────────────────────────────────────────────────────────────

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
    return frozenset(pairs)

KW_PAIRS = make_kw_pairing()


# ─── B₆ operations ───────────────────────────────────────────────────────────

def apply_b6(x, perm, flip_mask):
    """
    Apply a B₆ element to state x.
    perm: tuple of 6 indices — perm[i] is which input bit goes to output position i.
    flip_mask: 6-bit mask — bit i set means flip output position i.
    
    Result: permute bits of x according to perm, then XOR with flip_mask.
    """
    result = 0
    for out_pos in range(N):
        in_pos = perm[out_pos]
        bit = (x >> in_pos) & 1
        result |= bit << out_pos
    return result ^ flip_mask


def apply_b6_to_all(perm, flip_mask):
    """Apply B₆ element to all 64 states, return the permutation as a list."""
    return [apply_b6(x, perm, flip_mask) for x in range(NUM_STATES)]


def preserves_kw(perm, flip_mask):
    """Check if a B₆ element preserves the KW pairing."""
    sigma = apply_b6_to_all(perm, flip_mask)
    for a, b in KW_PAIRS:
        sa, sb = sigma[a], sigma[b]
        if (min(sa, sb), max(sa, sb)) not in KW_PAIRS:
            return False
    return True


# ─── Enumerate stabilizer ────────────────────────────────────────────────────

def find_stabilizer():
    """Find all elements of B₆ that preserve the KW pairing."""
    stabilizer = []
    identity = tuple(range(N))

    for perm in permutations(range(N)):
        for flip_int in range(1 << N):
            if preserves_kw(perm, flip_int):
                stabilizer.append((perm, flip_int))

    return stabilizer


# ─── Group analysis ──────────────────────────────────────────────────────────

def describe_element(perm, flip_mask):
    """Human-readable description of a B₆ element."""
    parts = []

    # Describe permutation
    identity = tuple(range(N))
    if perm != identity:
        # Find cycle notation (1-indexed for readability)
        visited = set()
        cycles = []
        for i in range(N):
            if i in visited:
                continue
            cycle = []
            j = i
            while j not in visited:
                visited.add(j)
                cycle.append(j + 1)  # 1-indexed
                j = perm[j]
            if len(cycle) > 1:
                cycles.append(tuple(cycle))
        if cycles:
            parts.append(''.join(f'({" ".join(map(str,c))})' for c in cycles))
    
    # Describe flips
    if flip_mask:
        flipped = [str(i + 1) for i in range(N) if flip_mask & (1 << i)]
        parts.append(f'flip{{{",".join(flipped)}}}')

    return ' ∘ '.join(parts) if parts else 'id'


def compose_b6(perm1, flip1, perm2, flip2):
    """Compose two B₆ elements: first apply (perm2, flip2), then (perm1, flip1)."""
    # Combined permutation: perm1 ∘ perm2
    new_perm = tuple(perm2[perm1[i]] for i in range(N))
    # Wait — need to think about this carefully.
    # Applying (perm2, flip2) to x: permute bits by perm2, then XOR flip2.
    # Then applying (perm1, flip1): permute bits by perm1, then XOR flip1.
    # 
    # Step 1: y = perm2(x) ^ flip2
    # Step 2: z = perm1(y) ^ flip1 = perm1(perm2(x) ^ flip2) ^ flip1
    #        = perm1(perm2(x)) ^ perm1(flip2) ^ flip1
    # where perm1(flip2) means permuting the bits of flip2 by perm1.
    #
    # So composition is (perm1 ∘ perm2, perm1(flip2) ^ flip1).
    composed_perm = tuple(perm2[perm1[i]] for i in range(N))
    # Permute flip2 by perm1
    permuted_flip2 = 0
    for i in range(N):
        if flip2 & (1 << perm1[i]):
            permuted_flip2 |= 1 << i
    composed_flip = permuted_flip2 ^ flip1
    return composed_perm, composed_flip


def inverse_b6(perm, flip_mask):
    """Inverse of a B₆ element."""
    # (perm, flip)^{-1}: need (perm', flip') such that
    # perm'(perm(x) ^ flip) ^ flip' = x for all x
    # perm'(perm(x)) ^ perm'(flip) ^ flip' = x
    # So perm' = perm^{-1}, flip' = perm^{-1}(flip)
    inv_perm = [0] * N
    for i in range(N):
        inv_perm[perm[i]] = i
    inv_perm = tuple(inv_perm)
    # perm^{-1}(flip)
    inv_flip = 0
    for i in range(N):
        if flip_mask & (1 << perm[i]):
            inv_flip |= 1 << i
    return inv_perm, inv_flip


def element_order(perm, flip_mask):
    """Order of a B₆ element."""
    cur_perm, cur_flip = perm, flip_mask
    identity = tuple(range(N))
    for k in range(1, 100):
        if cur_perm == identity and cur_flip == 0:
            return k
        cur_perm, cur_flip = compose_b6(perm, flip_mask, cur_perm, cur_flip)
    return -1  # shouldn't happen


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    out_dir = Path(__file__).parent
    lines = []

    def pr(s=""):
        print(s)
        lines.append(s)

    pr("=" * 70)
    pr("MAXIMAL SYMMETRY GROUP OF THE KW PAIRING IN B₆")
    pr("=" * 70)

    pr(f"\n  B₆ = hyperoctahedral group on 6 bits")
    pr(f"  |B₆| = 2⁶ × 6! = {(1 << N) * 720}")
    pr(f"  Each element: permute bit positions + selectively flip bits")

    # ── Verify Z₂² elements ──
    pr(f"\n## Known Z₂² Symmetries")

    identity_perm = tuple(range(N))
    rev_perm = tuple(reversed(range(N)))  # (5,4,3,2,1,0)

    known = [
        (identity_perm, 0, "identity"),
        (identity_perm, MASK_ALL, "complement"),
        (rev_perm, 0, "reversal"),
        (rev_perm, MASK_ALL, "comp∘rev"),
    ]

    for perm, flip, name in known:
        ok = preserves_kw(perm, flip)
        pr(f"  {name}: perm={perm}, flip={fmt(flip)}, preserves KW: {ok}")

    # ── Find full stabilizer ──
    pr(f"\n## Enumerating Stabilizer")
    pr(f"  Checking all {(1 << N) * 720:,} elements of B₆...")

    import time
    t0 = time.time()
    stabilizer = find_stabilizer()
    elapsed = time.time() - t0
    pr(f"  Found {len(stabilizer)} elements preserving KW ({elapsed:.1f}s)")

    # ── Analyze structure ──
    pr(f"\n## Stabilizer Elements")

    # Separate by type
    pure_perms = [(p, f) for p, f in stabilizer if f == 0]
    pure_flips = [(p, f) for p, f in stabilizer if p == identity_perm]
    mixed = [(p, f) for p, f in stabilizer if f != 0 and p != identity_perm]

    pr(f"\n  Pure permutations (no flips): {len(pure_perms)}")
    for p, f in pure_perms:
        desc = describe_element(p, f)
        order = element_order(p, f)
        pr(f"    {desc}  order={order}  perm={p}")

    pr(f"\n  Pure flips (no permutation): {len(pure_flips)}")
    for p, f in pure_flips:
        desc = describe_element(p, f)
        order = element_order(p, f)
        pr(f"    {desc}  order={order}  flip={fmt(f)}")

    pr(f"\n  Mixed (permutation + flip): {len(mixed)}")
    for p, f in mixed:
        desc = describe_element(p, f)
        order = element_order(p, f)
        pr(f"    {desc}  order={order}")

    # ── Group structure ──
    pr(f"\n## Group Structure")
    pr(f"\n  |Stab_B₆(KW)| = {len(stabilizer)}")

    # Check if it equals Z₂²
    pr(f"  |Z₂²| = 4")
    if len(stabilizer) == 4:
        pr(f"  Z₂² IS the full stabilizer in B₆!")
        pr(f"  No additional bitwise symmetry preserves the KW pairing.")
    else:
        pr(f"  Z₂² is a PROPER subgroup of Stab_B₆(KW).")
        pr(f"  Index [Stab : Z₂²] = {len(stabilizer) // 4}")

        # Element orders
        from collections import Counter
        orders = Counter(element_order(p, f) for p, f in stabilizer)
        pr(f"\n  Element orders: {dict(sorted(orders.items()))}")

        # Check if abelian
        is_abelian = True
        for i, (p1, f1) in enumerate(stabilizer):
            if not is_abelian:
                break
            for p2, f2 in stabilizer[i+1:]:
                ab_p, ab_f = compose_b6(p1, f1, p2, f2)
                ba_p, ba_f = compose_b6(p2, f2, p1, f1)
                if ab_p != ba_p or ab_f != ba_f:
                    is_abelian = False
                    break
        pr(f"  Abelian: {is_abelian}")

        # Find generators
        pr(f"\n  Looking for generators...")
        generated = {(identity_perm, 0)}
        generators = []
        
        for p, f in stabilizer:
            if (p, f) in generated:
                continue
            generators.append((p, f))
            # Close under composition with existing generated set
            new = {(p, f)}
            while new:
                to_add = set()
                for g in new:
                    for h in generated:
                        prod1 = compose_b6(g[0], g[1], h[0], h[1])
                        prod2 = compose_b6(h[0], h[1], g[0], g[1])
                        inv = inverse_b6(g[0], g[1])
                        for x in [prod1, prod2, inv]:
                            if x not in generated:
                                to_add.add(x)
                new = to_add
                generated |= new

            if len(generated) == len(stabilizer):
                break

        pr(f"  Generators ({len(generators)}):")
        for p, f in generators:
            desc = describe_element(p, f)
            order = element_order(p, f)
            pr(f"    {desc}  order={order}")

        pr(f"  Generated group size: {len(generated)} (expected {len(stabilizer)})")

        # What are the non-Z₂² elements doing?
        pr(f"\n## Analysis of Extra Symmetries")
        
        z2_sq = {
            (identity_perm, 0),
            (identity_perm, MASK_ALL),
            (rev_perm, 0),
            (rev_perm, MASK_ALL),
        }
        extras = [(p, f) for p, f in stabilizer if (p, f) not in z2_sq]
        
        pr(f"\n  Elements beyond Z₂² ({len(extras)}):")
        for p, f in extras[:20]:
            desc = describe_element(p, f)
            # Show what it does to a few states
            sigma = apply_b6_to_all(p, f)
            examples = [(x, sigma[x]) for x in [0, 1, 2, 3]]
            ex_str = ', '.join(f'{fmt(x)}→{fmt(y)}' for x, y in examples)
            pr(f"    {desc}: {ex_str}")
        if len(extras) > 20:
            pr(f"    ... and {len(extras) - 20} more")

        # Check which line permutations alone preserve KW
        pr(f"\n  Line permutations preserving KW:")
        for p, f in stabilizer:
            if f == 0 and p != identity_perm:
                # Which mirror-pair structure does this permutation have?
                desc = describe_element(p, f)
                # Check: does it map palindromes to palindromes?
                pals = [x for x in range(NUM_STATES) if REVERSE[x] == x]
                sigma = apply_b6_to_all(p, f)
                pal_preserved = all(REVERSE[sigma[x]] == sigma[x] for x in pals)
                pr(f"    {desc}: preserves palindromes={pal_preserved}")

    # ── Relationship to KW structure ──
    pr(f"\n## Structural Interpretation")

    # How does the stabilizer relate to the mirror-pair structure?
    # The KW pairing is defined by: rev for non-palindromes, comp for palindromes.
    # A permutation σ preserves this iff:
    #   For each pair (a, rev(a)): (σ(a), σ(rev(a))) is also a KW pair
    #   i.e., σ(rev(a)) = rev(σ(a)) [if σ(a) is not a palindrome]
    #   or σ(rev(a)) = comp(σ(a)) [if σ(a) is a palindrome]

    # For a line permutation π (no flips):
    # π preserves reversal iff π commutes with bit-reversal:
    #   π(rev(x)) = rev(π(x)) for all x
    # This means π(i) + π(N-1-i) = N-1 for all i
    # i.e., π preserves the mirror-pair structure {(0,5),(1,4),(2,3)}

    pr(f"\n  A line permutation π preserves KW iff π commutes with reversal:")
    pr(f"  π(rev(x)) = rev(π(x)) for all x")
    pr(f"  Equivalently: π preserves the mirror-pair partition {{L1↔L6, L2↔L5, L3↔L4}}")
    pr(f"  Such π can permute the 3 pairs among themselves and/or swap within pairs.")
    pr(f"  This gives S₃ ⋊ (Z₂)³ — but swapping within a pair IS reversal of that pair,")
    pr(f"  and we need the PRODUCT of all swaps to preserve the palindrome structure.")
    
    # Actually: permutations of {(0,5),(1,4),(2,3)} as blocks = S₃ acting on 3 pairs
    # Within each pair, swap or not = (Z₂)³
    # Total: S₃ × (Z₂)³ = 6 × 8 = 48... but not all preserve KW.
    # We need to also check that complement pairs (palindromes) are preserved.
    
    # Count: how many pure permutations (no flips)?
    n_pure = len(pure_perms)
    pr(f"\n  Pure permutations preserving KW: {n_pure}")
    
    # For each, check if it preserves mirror-pair partition
    for p, f in pure_perms:
        # Check: does p map mirror-pairs to mirror-pairs?
        mirror_pairs = [(0, 5), (1, 4), (2, 3)]
        maps = []
        for a, b in mirror_pairs:
            pa, pb = p[a], p[b]
            mapped_pair = (min(pa, pb), max(pa, pb))
            maps.append(mapped_pair)
        pr(f"    perm={p}: mirror pairs map to {maps}")

    # ── Summary ──
    pr(f"\n{'='*70}")
    pr("SUMMARY")
    pr(f"{'='*70}")

    pr(f"\n  |Stab_B₆(KW)| = {len(stabilizer)}")
    if len(stabilizer) == 4:
        pr(f"  Z₂² is the MAXIMAL bitwise symmetry group of the KW pairing.")
        pr(f"  No line permutation or partial complement beyond Z₂² preserves KW.")
    else:
        pr(f"  Stab_B₆(KW) strictly contains Z₂² (index {len(stabilizer)//4}).")
    
    pr(f"  Generators: {len(generators) if len(stabilizer) > 4 else 2}")

    # ── Save ──
    md_path = out_dir / 'maximal_symmetry_results.md'
    with open(md_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    pr(f"\nSaved to {md_path}")


if __name__ == '__main__':
    main()
