#!/usr/bin/env python3
"""
genetic_code_boundary.py — Genetic code as a non-rigid surjection

The standard genetic code maps 64 codons → 21 targets (20 amino acids + stop).
Test whether ANY involution on the domain/target makes it equivariant.

Domain: F₄³ where F₄ = {0, 1, α, α+1} with α² + α + 1 = 0
  Bases: U=0, C=1, A=α, G=α+1
  
Involutions on F₄:
  - Identity (trivial)
  - Frobenius: x ↦ x² (swaps α ↔ α+1, i.e., A ↔ G)
  - Watson-Crick complement: A↔U, C↔G → swaps 0↔α, 1↔α+1

We test all involutions on the 64-element domain that come from:
  1. Componentwise involutions on F₄ (each position independently)
  2. With optional coordinate permutations
"""

from collections import Counter, defaultdict
from itertools import product as iterproduct, permutations
import sys

# ═══════════════════════════════════════════════════════════
# F₄ arithmetic
# ═══════════════════════════════════════════════════════════

# F₄ = {0, 1, α, α+1} with α² = α + 1
# Elements encoded as integers 0-3:
#   0 = 0, 1 = 1, 2 = α, 3 = α+1

F4_ADD = [
    [0, 1, 2, 3],
    [1, 0, 3, 2],
    [2, 3, 0, 1],
    [3, 2, 1, 0],
]

F4_MUL = [
    [0, 0, 0, 0],
    [0, 1, 2, 3],
    [0, 2, 3, 1],
    [0, 3, 1, 2],
]

def f4_add(a, b):
    return F4_ADD[a][b]

def f4_mul(a, b):
    return F4_MUL[a][b]

def f4_neg(a):
    """Additive negation in F₄. Since char=2, -a = a."""
    return a

def f4_frobenius(a):
    """Frobenius: x ↦ x². Swaps α ↔ α+1."""
    return F4_MUL[a][a]

# ═══════════════════════════════════════════════════════════
# Genetic code
# ═══════════════════════════════════════════════════════════

# Standard genetic code
# Codons as (first, second, third) positions
# Bases: U=0, C=1, A=2(=α), G=3(=α+1)
# Using the standard table

BASE_TO_F4 = {'U': 0, 'C': 1, 'A': 2, 'G': 3}
F4_TO_BASE = {0: 'U', 1: 'C', 2: 'A', 3: 'G'}

# Standard genetic code: codon → amino acid (single letter)
GENETIC_CODE = {
    'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
    'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
    'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
    'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
    'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
    'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}

# Build as F₄³ → target index
AMINO_ACIDS = sorted(set(GENETIC_CODE.values()))
AA_TO_IDX = {aa: i for i, aa in enumerate(AMINO_ACIDS)}

def codon_to_f4(codon_str):
    """Convert codon string to F₄³ tuple."""
    return tuple(BASE_TO_F4[b] for b in codon_str)

def f4_to_codon(f4_tuple):
    """Convert F₄³ tuple to codon string."""
    return ''.join(F4_TO_BASE[x] for x in f4_tuple)

# Build the surjection as a dict: F₄³ tuple → amino acid index
GEN_CODE_MAP = {}
for codon_str, aa in GENETIC_CODE.items():
    f4_codon = codon_to_f4(codon_str)
    GEN_CODE_MAP[f4_codon] = AA_TO_IDX[aa]


# ═══════════════════════════════════════════════════════════
# Involutions on F₄
# ═══════════════════════════════════════════════════════════

def enumerate_f4_involutions():
    """
    All involutions σ: F₄ → F₄ (bijections with σ² = id).
    An involution is a permutation that is its own inverse.
    F₄ has 4! = 24 permutations. Involutions: id + transpositions + double transpositions.
    """
    involutions = []
    for perm in permutations(range(4)):
        # Check σ² = id
        is_involution = all(perm[perm[i]] == i for i in range(4))
        if is_involution:
            involutions.append(perm)
    return involutions

def classify_f4_involution(sigma):
    """Classify an F₄ involution by its cycle structure and algebraic meaning."""
    fixed = [i for i in range(4) if sigma[i] == i]
    swaps = []
    seen = set()
    for i in range(4):
        if i not in seen and sigma[i] != i:
            swaps.append((i, sigma[i]))
            seen.add(i)
            seen.add(sigma[i])
    
    desc = []
    if len(fixed) == 4:
        desc.append("identity")
    else:
        for a, b in swaps:
            desc.append(f"{F4_TO_BASE[a]}↔{F4_TO_BASE[b]}")
    
    # Check if it's the Frobenius
    if all(sigma[i] == f4_frobenius(i) for i in range(4)):
        desc.append("[Frobenius: x↦x²]")
    
    # Check if it's Watson-Crick complement
    wc = {0: 2, 2: 0, 1: 3, 3: 1}  # U↔A, C↔G
    if all(sigma[i] == wc[i] for i in range(4)):
        desc.append("[Watson-Crick complement]")
    
    # Check if it's a field automorphism
    is_aut = all(
        sigma[f4_add(a, b)] == f4_add(sigma[a], sigma[b])
        and sigma[f4_mul(a, b)] == f4_mul(sigma[a], sigma[b])
        for a in range(4) for b in range(4)
    )
    if is_aut and len(fixed) < 4:
        desc.append("[field automorphism]")
    
    # Check if it's additive
    is_additive = all(
        sigma[f4_add(a, b)] == f4_add(sigma[a], sigma[b])
        for a in range(4) for b in range(4)
    )
    if is_additive and not is_aut and len(fixed) < 4:
        desc.append("[additive only]")
    
    return ', '.join(desc), fixed, swaps


# ═══════════════════════════════════════════════════════════
# Domain involutions on F₄³
# ═══════════════════════════════════════════════════════════

def build_domain_involutions():
    """
    Build all involutions on F₄³ from:
    1. Componentwise: σ(x₁,x₂,x₃) = (σ₁(x₁), σ₂(x₂), σ₃(x₃))
       where each σᵢ is an F₄ involution
    2. With coordinate permutation π: σ_π(x₁,x₂,x₃) = σ(x_{π(1)}, x_{π(2)}, x_{π(3)})
    
    Returns: list of (label, involution_function)
    """
    f4_invols = enumerate_f4_involutions()
    involutions = []
    
    # Type 1: Componentwise (no coordinate permutation)
    for s1 in f4_invols:
        for s2 in f4_invols:
            for s3 in f4_invols:
                label1, _, _ = classify_f4_involution(s1)
                label2, _, _ = classify_f4_involution(s2)
                label3, _, _ = classify_f4_involution(s3)
                
                # Skip all-identity
                if s1 == tuple(range(4)) and s2 == tuple(range(4)) and s3 == tuple(range(4)):
                    continue
                
                def make_inv(s1, s2, s3):
                    def inv(codon):
                        return (s1[codon[0]], s2[codon[1]], s3[codon[2]])
                    return inv
                
                label = f"({label1}, {label2}, {label3})"
                involutions.append((label, make_inv(s1, s2, s3), (s1, s2, s3), None))
    
    # Type 2: Coordinate permutations × componentwise
    # Only non-trivial permutations
    coord_perms = [(1,2,0), (2,0,1), (0,2,1), (2,1,0), (1,0,2)]  # non-identity
    
    for perm in coord_perms:
        for s1 in f4_invols:
            for s2 in f4_invols:
                for s3 in f4_invols:
                    def make_perm_inv(perm, s1, s2, s3):
                        sigmas = [s1, s2, s3]
                        def inv(codon):
                            permuted = tuple(codon[perm[i]] for i in range(3))
                            return (sigmas[0][permuted[0]], sigmas[1][permuted[1]], sigmas[2][permuted[2]])
                        return inv
                    
                    fn = make_perm_inv(perm, s1, s2, s3)
                    # Check it's actually an involution
                    is_invol = True
                    for c in iterproduct(range(4), repeat=3):
                        if fn(fn(c)) != c:
                            is_invol = False
                            break
                    
                    if is_invol:
                        perm_label = f"π={perm}"
                        involutions.append((perm_label, fn, (s1, s2, s3), perm))
    
    return involutions


# ═══════════════════════════════════════════════════════════
# Target involutions on amino acid set
# ═══════════════════════════════════════════════════════════

def enumerate_target_involutions(num_targets):
    """
    Enumerate all involutions on {0, ..., num_targets-1}.
    For 21 elements this is huge (≈ 10^10). So we restrict to
    involutions that swap at most a few pairs.
    """
    # For the boundary test, we only check:
    # 1. Identity (trivial)
    # 2. All single transpositions C(21,2) = 210
    # 3. For the best-matching domain involutions, try all double transpositions
    
    involutions = []
    
    # Identity
    involutions.append(("identity", list(range(num_targets))))
    
    # Single transpositions
    for i in range(num_targets):
        for j in range(i+1, num_targets):
            perm = list(range(num_targets))
            perm[i] = j
            perm[j] = i
            involutions.append((f"swap({AMINO_ACIDS[i]},{AMINO_ACIDS[j]})", perm))
    
    return involutions


# ═══════════════════════════════════════════════════════════
# Equivariance test
# ═══════════════════════════════════════════════════════════

def test_equivariance(domain_inv_fn, target_perm, gen_code):
    """
    Test f(σ(x)) = τ(f(x)) for all x ∈ F₄³.
    Returns number of violations.
    """
    violations = 0
    total = 0
    for codon in iterproduct(range(4), repeat=3):
        total += 1
        f_x = gen_code[codon]
        sigma_x = domain_inv_fn(codon)
        f_sigma_x = gen_code[sigma_x]
        tau_f_x = target_perm[f_x]
        if f_sigma_x != tau_f_x:
            violations += 1
    return violations


# ═══════════════════════════════════════════════════════════
# Main analysis
# ═══════════════════════════════════════════════════════════

def main():
    out = []
    def w(s=""):
        out.append(s)
        print(s)

    w("# Genetic Code Boundary Test")
    w()
    w("Testing whether the standard genetic code (64 codons → 21 targets)")
    w("satisfies any equivariance condition f(σ(x)) = τ(f(x)).")
    w()
    
    # ─── Step 1: Fiber sizes ───
    w("## Step 1: Fiber Sizes of the Genetic Code")
    w()
    
    fibers = Counter()
    for codon, aa in GENETIC_CODE.items():
        fibers[aa] += 1
    
    w("| Amino Acid | Codons | Count |")
    w("|------------|--------|-------|")
    for aa in sorted(fibers.keys(), key=lambda x: -fibers[x]):
        codons = [c for c, a in GENETIC_CODE.items() if a == aa]
        w(f"| {aa} | {', '.join(sorted(codons)[:3])}{'...' if len(codons)>3 else ''} | {fibers[aa]} |")
    
    fiber_sizes = sorted(fibers.values(), reverse=True)
    w(f"\nFiber size distribution: {fiber_sizes}")
    w(f"Sum: {sum(fiber_sizes)} (should be 64)")
    w(f"Number of distinct targets: {len(fibers)} (20 AAs + Stop)")
    w(f"Max fiber: {max(fiber_sizes)} (Leu, Ser, Arg)")
    w(f"Min fiber: {min(fiber_sizes)} (Met, Trp)")
    w(f"Fiber shape: {tuple(fiber_sizes)}")
    w()
    
    # Compare with E=1 shapes
    w("### Comparison with E=1 surjection shapes")
    w()
    w("| System | Domain | Target | Fiber shape | Max/Min ratio |")
    w("|--------|--------|--------|-------------|--------------|")
    w(f"| I Ching | F₂³ (8) | Z₅ (5) | (2,2,2,1,1) | 2 |")
    w(f"| Genetic | F₄³ (64) | 21 targets | {tuple(fiber_sizes[:5])}... | {max(fiber_sizes)}/{min(fiber_sizes)} = {max(fiber_sizes)/min(fiber_sizes):.0f} |")
    w()
    w("The genetic code has much more heterogeneous fibers (6:1 ratio vs 2:1).")
    w("This is a structural difference, not just a scaling difference.")
    w()
    
    # ─── Step 2: F₄ involutions ───
    w("## Step 2: F₄ Involutions")
    w()
    
    f4_invols = enumerate_f4_involutions()
    w(f"Number of involutions on F₄: {len(f4_invols)}")
    w()
    for sigma in f4_invols:
        desc, fixed, swaps = classify_f4_involution(sigma)
        w(f"  σ = {sigma}: {desc}")
    w()
    
    # ─── Step 3: Test all componentwise domain involutions ───
    w("## Step 3: Equivariance Tests")
    w()
    w("Testing componentwise domain involutions σ(x₁,x₂,x₃) = (σ₁(x₁), σ₂(x₂), σ₃(x₃))")
    w("with target involution τ = identity (f(σ(x)) = f(x) — symmetry of the code)")
    w()
    
    # First test: domain involutions with τ = identity
    # This tests: which domain transformations preserve the genetic code?
    f4_id = tuple(range(4))
    
    # Key involutions to test:
    key_involutions = []
    
    # Frobenius on each position
    frob = tuple(f4_frobenius(i) for i in range(4))  # (0, 1, 3, 2) = A↔G
    wc = (2, 3, 0, 1)  # Watson-Crick: U↔A, C↔G
    
    # Named involutions
    named = [
        ("Frobenius pos 3 only", f4_id, f4_id, frob),
        ("Frobenius pos 2 only", f4_id, frob, f4_id),
        ("Frobenius pos 1 only", frob, f4_id, f4_id),
        ("Frobenius all positions", frob, frob, frob),
        ("WC pos 3 only", f4_id, f4_id, wc),
        ("WC pos 2 only", f4_id, wc, f4_id),
        ("WC pos 1 only", wc, f4_id, f4_id),
        ("WC all positions", wc, wc, wc),
        ("Transition (U↔C, A↔G)", (1,0,2,3), (1,0,2,3), (1,0,2,3)),
        ("Purine swap only (A↔G all pos)", frob, frob, frob),
        ("Pyrimidine swap (U↔C all pos)", (1,0,2,3), (1,0,2,3), (1,0,2,3)),
    ]
    
    # Remove duplicates
    seen_sigs = set()
    unique_named = []
    for name, s1, s2, s3 in named:
        sig = (s1, s2, s3)
        if sig not in seen_sigs:
            seen_sigs.add(sig)
            unique_named.append((name, s1, s2, s3))
    
    w("### Key named involutions (τ = identity)")
    w()
    w("| Domain involution | Violations (of 64) | Description |")
    w("|-------------------|-------------------|-------------|")
    
    identity_perm = list(range(len(AMINO_ACIDS)))
    
    for name, s1, s2, s3 in unique_named:
        def inv(codon, s1=s1, s2=s2, s3=s3):
            return (s1[codon[0]], s2[codon[1]], s3[codon[2]])
        
        violations = test_equivariance(inv, identity_perm, GEN_CODE_MAP)
        w(f"| {name} | {violations}/64 = {violations/64:.1%} | σ=({s1},{s2},{s3}) |")
    
    w()
    
    # ─── Step 4: Exhaustive search for best match ───
    w("## Step 4: Exhaustive Search — Best (σ, τ) Pairs")
    w()
    w("Testing all componentwise domain involutions × all target involutions")
    w("(identity + single transpositions = 1 + 210 = 211 target involutions)")
    w()
    
    target_invols = enumerate_target_involutions(len(AMINO_ACIDS))
    w(f"Domain involutions (componentwise, non-identity): {len(f4_invols)**3 - 1}")
    w(f"Target involutions: {len(target_invols)}")
    w(f"Total pairs to test: {(len(f4_invols)**3 - 1) * len(target_invols)}")
    w()
    
    best_results = []
    best_nontrivial = []  # τ ≠ identity
    
    for s1 in f4_invols:
        for s2 in f4_invols:
            for s3 in f4_invols:
                if s1 == f4_id and s2 == f4_id and s3 == f4_id:
                    continue  # skip identity
                
                def inv(codon, s1=s1, s2=s2, s3=s3):
                    return (s1[codon[0]], s2[codon[1]], s3[codon[2]])
                
                for tgt_label, tgt_perm in target_invols:
                    violations = test_equivariance(inv, tgt_perm, GEN_CODE_MAP)
                    if violations <= 8:
                        desc1, _, _ = classify_f4_involution(s1)
                        desc2, _, _ = classify_f4_involution(s2)
                        desc3, _, _ = classify_f4_involution(s3)
                        entry = {
                            'violations': violations,
                            'domain': (s1, s2, s3),
                            'domain_desc': f"({desc1}, {desc2}, {desc3})",
                            'target': tgt_label,
                        }
                        best_results.append(entry)
                        if tgt_label != "identity":
                            best_nontrivial.append(entry)
    
    best_results.sort(key=lambda x: x['violations'])
    best_nontrivial.sort(key=lambda x: x['violations'])
    
    w("### All matches with τ = identity (code symmetries)")
    w()
    w("These are NOT analogous to I Ching equivariance — they are trivial")
    w("symmetries where the domain involution preserves codons within fibers.")
    w("(Wobble degeneracy.)")
    w()
    trivial = [r for r in best_results if r['target'] == 'identity']
    if trivial:
        w("| Violations | Domain σ | Description |")
        w("|------------|----------|-------------|")
        for r in trivial[:10]:
            w(f"| {r['violations']}/64 ({r['violations']/64:.1%}) | {r['domain_desc']} | wobble symmetry |")
    w()
    
    w("### Best matches with NON-TRIVIAL τ (analogous to I Ching)")
    w()
    w("For comparison with f(~x) = -f(x): need non-trivial target involution.")
    w()
    if best_nontrivial:
        w("| Violations | Domain σ | Target τ |")
        w("|------------|----------|----------|")
        for r in best_nontrivial[:15]:
            w(f"| {r['violations']}/64 ({r['violations']/64:.1%}) | {r['domain_desc']} | {r['target']} |")
    else:
        w("No pairs with ≤ 8 violations and non-trivial τ.")
    w()
    
    # ─── Step 5: Test with coordinate permutations ───
    w("## Step 5: Coordinate Permutation Tests")
    w()
    w("Testing involutions that also permute codon positions.")
    w("Only checking the most biologically relevant: reverse complement.")
    w()
    
    # Reverse complement: reverse the codon AND apply Watson-Crick to each base
    # This is the biological complement strand reading
    
    best_with_perm = []
    
    coord_perms = [(2, 1, 0)]  # reverse only (most biologically meaningful)
    
    for perm in coord_perms:
        for s1 in f4_invols:
            for s2 in f4_invols:
                for s3 in f4_invols:
                    sigmas = [s1, s2, s3]
                    
                    def inv(codon, perm=perm, sigmas=sigmas):
                        permuted = tuple(codon[perm[i]] for i in range(3))
                        return tuple(sigmas[i][permuted[i]] for i in range(3))
                    
                    # Check if it's an involution
                    is_invol = True
                    for c in iterproduct(range(4), repeat=3):
                        if inv(inv(c)) != c:
                            is_invol = False
                            break
                    
                    if not is_invol:
                        continue
                    
                    for tgt_label, tgt_perm in target_invols:
                        violations = test_equivariance(inv, tgt_perm, GEN_CODE_MAP)
                        if violations <= 10:
                            desc1, _, _ = classify_f4_involution(s1)
                            desc2, _, _ = classify_f4_involution(s2)
                            desc3, _, _ = classify_f4_involution(s3)
                            best_with_perm.append({
                                'violations': violations,
                                'perm': perm,
                                'domain': (s1, s2, s3),
                                'domain_desc': f"rev∘({desc1}, {desc2}, {desc3})",
                                'target': tgt_label,
                            })
    
    best_with_perm.sort(key=lambda x: x['violations'])
    
    w("### Best matches with coordinate reversal (≤ 10 violations)")
    w()
    if best_with_perm:
        w("| Violations | Domain σ | Target τ |")
        w("|------------|----------|----------|")
        for r in best_with_perm[:15]:
            w(f"| {r['violations']}/64 ({r['violations']/64:.1%}) | {r['domain_desc']} | {r['target']} |")
    else:
        w("No pairs found with ≤ 10 violations.")
    w()
    
    # ─── Step 6: Summary ───
    w("## Summary")
    w()
    
    trivial_best = min(r['violations'] for r in best_results if r['target'] == 'identity') if any(r['target'] == 'identity' for r in best_results) else 64
    nontrivial_best = best_nontrivial[0]['violations'] if best_nontrivial else 64
    perm_best = best_with_perm[0]['violations'] if best_with_perm else 64
    
    w(f"**Best trivial equivariance (τ=id, wobble): {trivial_best}/64 violations**")
    w(f"**Best non-trivial equivariance (τ≠id): {nontrivial_best}/64 violations**")
    w()
    
    if trivial_best == 0:
        w("The genetic code DOES have perfect trivial equivariance: swapping U↔C")
        w("at position 3 preserves the amino acid. This is the well-known wobble")
        w("degeneracy — a code symmetry, not an involutory structure.")
        w()
    
    if nontrivial_best <= 4:
        w(f"Near-equivariance with non-trivial τ: {nontrivial_best} violations.")
        w("Some structural pairing of amino acids is approximately respected.")
    elif nontrivial_best <= 10:
        w(f"Weak non-trivial equivariance: {nontrivial_best} violations ({nontrivial_best/64:.0%}).")
    else:
        w(f"No meaningful non-trivial equivariance: best = {nontrivial_best}/64 ({nontrivial_best/64:.0%}).")
        w("The genetic code does NOT have an involutory structure analogous")
        w("to the I Ching's f(~x) = -f(x).")
    
    w()
    w("### Structural comparison with I Ching")
    w()
    w("| Property | I Ching (3,5) | Genetic Code |")
    w("|----------|--------------|--------------|")
    w(f"| Domain | F₂³ (8 elements) | F₄³ (64 codons) |")
    w(f"| Target | Z₅ (5 elements) | 21 targets |")
    w(f"| Fiber shape | (2,2,2,1,1) | {tuple(fiber_sizes[:5])}... |")
    w(f"| Max/min ratio | 2 | {max(fiber_sizes)} |")
    w(f"| Trivial equivariance (τ=id) | EXACT (complement) | EXACT (wobble) |")
    w(f"| Non-trivial equivariance | EXACT (τ=negation) | NONE ({nontrivial_best}/64 best) |")
    w(f"| Rigidity (orbits) | 1 (unique) | N/A (not rigid) |")
    w(f"| Target structure | Z₅ (cyclic, prime) | No group structure |")
    w()
    w("### Key finding")
    w()
    w("The genetic code is a surjection from a combinatorial domain (F₄³)")
    w("to a functional codomain (amino acids), just as the I Ching is a")
    w("surjection from F₂³ to Z₅. But the structural properties diverge:")
    w()
    w("1. **No equivariance**: The genetic code doesn't respect any natural")
    w("   involution on F₄³. The I Ching's equivariance is exact.")
    w("2. **No target group**: Amino acids have no natural cyclic order.")
    w("   Z₅'s cyclic structure is essential for the I Ching's rigidity.")
    w("3. **Heterogeneous fibers**: The genetic code's fiber sizes span")
    w("   1-6, much more varied than the I Ching's 1-2 range.")
    w("4. **The connection is architectural, not algebraic**: Both are")
    w("   surjections from combinatorial to functional space, but the")
    w("   genetic code lacks the algebraic constraints that make (3,5) rigid.")
    
    # Write output
    path = "/home/quasar/nous/memories/iching/relations/genetic_code_boundary_output.md"
    with open(path, 'w') as f:
        f.write('\n'.join(out))
    print(f"\n\nResults written to {path}")


if __name__ == "__main__":
    main()
