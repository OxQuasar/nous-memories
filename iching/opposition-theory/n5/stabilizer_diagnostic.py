#!/usr/bin/env python3
"""
n=5 Stabilizer Diagnostic

Expected |Stab| = 128 = S₂ × (Z₂)² × Z₂ × (Z₂)² × Z₂
  = (permute 2 mirror pairs) × (swap within each pair) × (center perm)
  × (flip each mirror pair's values) × (flip center value)

Computed |Stab| = 64. Which generator fails?
"""

from pathlib import Path

N = 5
NUM_STATES = 1 << N
MASK_ALL = (1 << N) - 1

def _reverse(x):
    bits = format(x, f'0{N}b')
    return int(bits[::-1], 2)

REVERSE = [_reverse(x) for x in range(NUM_STATES)]
COMPLEMENT = [x ^ MASK_ALL for x in range(NUM_STATES)]
PALINDROME_SET = {x for x in range(NUM_STATES) if REVERSE[x] == x}

def fmt(x):
    return format(x, f'0{N}b')

def apply_bn(x, perm, flip_mask):
    result = 0
    for out_pos in range(N):
        bit = (x >> perm[out_pos]) & 1
        result |= bit << out_pos
    return result ^ flip_mask

def make_kw_pairs():
    pairs = set()
    seen = set()
    for x in range(NUM_STATES):
        if x in seen:
            continue
        partner = COMPLEMENT[x] if x in PALINDROME_SET else REVERSE[x]
        pairs.add((min(x, partner), max(x, partner)))
        seen.update((x, partner))
    return frozenset(pairs)

KW = make_kw_pairs()

def preserves_kw(perm, flip):
    for a, b in KW:
        sa = apply_bn(a, perm, flip)
        sb = apply_bn(b, perm, flip)
        if (min(sa, sb), max(sa, sb)) not in KW:
            return False
    return True

def main():
    out_dir = Path(__file__).parent
    lines = []
    def pr(s=""):
        print(s)
        lines.append(s)

    pr("=" * 60)
    pr("n=5 STABILIZER DIAGNOSTIC")
    pr("=" * 60)

    # Bit positions: 0=L1, 1=L2, 2=L3(center), 3=L4, 4=L5
    # Mirror pairs: {L1↔L5} = {pos 0 ↔ pos 4}, {L2↔L4} = {pos 1 ↔ pos 3}
    # Center: L3 = pos 2

    id_perm = (0, 1, 2, 3, 4)

    generators = [
        # Permutation generators
        ("swap within pair 1: L1↔L5",
         (4, 1, 2, 3, 0), 0b00000),
        ("swap within pair 2: L2↔L4",
         (0, 3, 2, 1, 4), 0b00000),
        ("permute pairs: {L1,L5}↔{L2,L4}",
         (1, 0, 2, 4, 3), 0b00000),
        # Wait — permuting mirror pairs means:
        # pair1 = {pos0, pos4}, pair2 = {pos1, pos3}
        # swapping the pairs: pos0↔pos1, pos4↔pos3, center stays
        # So L1→L2, L2→L1, L4→L5, L5→L4, L3→L3
        # perm[0]=1, perm[1]=0, perm[2]=2, perm[3]=4, perm[4]=3
        # Let me redo this carefully.

        # Actually the above is wrong. Let me think again.
        # "Permute the two mirror pairs" means the pair {L1,L5} swaps with {L2,L4}.
        # L1→L2, L5→L4, L2→L1, L4→L5
        # In bit positions: pos0→pos1, pos4→pos3, pos1→pos0, pos3→pos4
        # perm[new_pos] = old_pos, so:
        # new pos0 gets old pos1: perm[0]=1
        # new pos1 gets old pos0: perm[1]=0
        # new pos2 stays: perm[2]=2
        # new pos3 gets old pos4: perm[3]=4
        # new pos4 gets old pos3: perm[4]=3

        # Flip generators
        ("flip pair 1 values: complement at {L1,L5}",
         id_perm, 0b10001),  # bits 0 and 4
        ("flip pair 2 values: complement at {L2,L4}",
         id_perm, 0b01010),  # bits 1 and 3
        ("flip center value: complement at L3",
         id_perm, 0b00100),  # bit 2
    ]

    # Fix the permute-pairs generator
    generators[2] = ("permute pairs: {L1,L5}↔{L2,L4}",
                     (1, 0, 2, 4, 3), 0b00000)

    pr(f"\nMirror pairs: {{L1↔L5}} = {{pos0↔pos4}}, {{L2↔L4}} = {{pos1↔pos3}}")
    pr(f"Center: L3 = pos2")
    pr(f"\nTesting {len(generators)} expected generators:\n")

    for name, perm, flip in generators:
        ok = preserves_kw(perm, flip)
        pr(f"  {'✓' if ok else '✗'} {name}")
        pr(f"    perm={perm}, flip={fmt(flip)}, preserves KW: {ok}")

        if not ok:
            # Show which pair breaks
            for a, b in sorted(KW):
                sa = apply_bn(a, perm, flip)
                sb = apply_bn(b, perm, flip)
                mapped = (min(sa, sb), max(sa, sb))
                if mapped not in KW:
                    is_pal_a = a in PALINDROME_SET
                    is_pal_sa = sa in PALINDROME_SET
                    pr(f"    BREAK: ({fmt(a)},{fmt(b)}) → ({fmt(sa)},{fmt(sb)})")
                    pr(f"      {fmt(a)}: palindrome={is_pal_a}")
                    pr(f"      {fmt(sa)}: palindrome={is_pal_sa}")
                    # Show what KW expects for sa
                    for ka, kb in KW:
                        if ka == min(sa, sb) or kb == min(sa, sb):
                            pr(f"      KW expects: ({fmt(ka)},{fmt(kb)})")
                    break

    # Count: how many of the 7 generators preserve KW?
    n_preserve = sum(1 for _, p, f in generators if preserves_kw(p, f))
    pr(f"\n  {n_preserve}/7 generators preserve KW")

    # Expected group if all worked: 2^(perm part) * 2^(flip part)
    # Perm part: S₂ × (Z₂)² = 2 × 4 = 8
    # Flip part: (Z₂)³ = 8
    # Total: 64... wait that's already 64
    # Actually: S₂ acts on 2 pairs = 2 permutations
    # (Z₂)² = swap within each pair = 4
    # Center has no permutation freedom (it maps to itself)
    # Total perm: 2 × 4 = 8... no.
    # swap within pair 1: Z₂, swap within pair 2: Z₂, permute the 2 pairs: S₂
    # These generate: wreath product Z₂ ≀ S₂ = order 2² × 2 = 8
    # But wait, at n=5 center is fixed, so perm part = Z₂ ≀ S₂ = 8
    # Flip part: flip pair 1, flip pair 2, flip center = (Z₂)³ = 8
    # Total = 8 × 8 = 64... this IS 64!

    pr(f"\n## Group Structure Explanation")
    pr(f"  Permutation part: Z₂ ≀ S₂ = (Z₂)² ⋊ S₂ = order 8")
    pr(f"    (swap within pair 1) × (swap within pair 2) × (permute pairs)")
    pr(f"  Flip part: (Z₂)³ = order 8")
    pr(f"    (flip pair 1) × (flip pair 2) × (flip center)")
    pr(f"  Total: 8 × 8 = 64")
    pr(f"\n  The initial expectation of 128 double-counted: there is no")
    pr(f"  independent 'center permutation' generator — the center position")
    pr(f"  is always fixed by any mirror-pair-preserving permutation.")
    pr(f"  |Stab| = 64 is the correct expected order, matching computation.")

    # Verify: is the full group generated by all 7?
    from itertools import product

    def compose(perm1, flip1, perm2, flip2):
        """Apply (perm2,flip2) then (perm1,flip1)."""
        new_perm = tuple(perm2[perm1[i]] for i in range(N))
        permuted_flip2 = 0
        for i in range(N):
            if flip2 & (1 << perm1[i]):
                permuted_flip2 |= 1 << i
        return new_perm, permuted_flip2 ^ flip1

    def inverse(perm, flip):
        inv_perm = [0]*N
        for i in range(N):
            inv_perm[perm[i]] = i
        inv_perm = tuple(inv_perm)
        inv_flip = 0
        for i in range(N):
            if flip & (1 << perm[i]):
                inv_flip |= 1 << i
        return inv_perm, inv_flip

    # Generate the group from all generators
    generated = {(id_perm, 0)}
    queue = [(p, f) for _, p, f in generators]
    for g in queue:
        generated.add(g)

    changed = True
    while changed:
        changed = False
        new = set()
        for g in list(generated):
            for h in list(generated):
                prod = compose(g[0], g[1], h[0], h[1])
                if prod not in generated:
                    new.add(prod)
                inv = inverse(g[0], g[1])
                if inv not in generated:
                    new.add(inv)
        if new:
            generated |= new
            changed = True

    pr(f"\n  Group generated by all 7 generators: {len(generated)} elements")

    # How many of these preserve KW?
    n_kw = sum(1 for p, f in generated if preserves_kw(p, f))
    pr(f"  Of these, {n_kw} preserve KW")

    # Append to cross_scale_results.md
    results_path = out_dir / 'cross_scale_results.md'
    with open(results_path, 'a') as f:
        f.write('\n\n')
        f.write('\n'.join(lines) + '\n')
    pr(f"\nAppended to {results_path}")


if __name__ == '__main__':
    main()
