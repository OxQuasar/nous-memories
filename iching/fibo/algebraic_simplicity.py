#!/usr/bin/env python3
"""
Algebraic Simplicity vs Ubiquity Table.

For each algebraic integer: Mahler measure, CF convergence rate,
cyclotomic conductor, minimal recurrence complexity.
Question: is φ's ubiquity exactly predicted by algebraic simplicity?
"""

import json
import math
from pathlib import Path

import mpmath
import sympy
from sympy import Rational, Poly, Symbol, cos, pi, minimal_polynomial, sqrt
from sympy.polys.numberfields import minimal_polynomial as minpoly
from scipy.stats import spearmanr

mpmath.mp.dps = 100  # high precision for CF computation

x = Symbol('x')

# ── Constants: (name, minimal_polynomial_coeffs_descending, approx_value, cyclotomic_conductor) ──

CONSTANTS = [
    {
        "name": "φ (golden ratio)",
        "poly_coeffs": [1, -1, -1],          # x²−x−1
        "approx": 1.6180339887,
        "conductor": 5,
    },
    {
        "name": "√2",
        "poly_coeffs": [1, 0, -2],            # x²−2
        "approx": 1.4142135624,
        "conductor": 8,
    },
    {
        "name": "√3",
        "poly_coeffs": [1, 0, -3],            # x²−3
        "approx": 1.7320508076,
        "conductor": 12,
    },
    {
        "name": "Plastic number ρ",
        "poly_coeffs": [1, 0, -1, -1],        # x³−x−1
        "approx": 1.3247179572,
        "conductor": None,  # not cyclotomic
    },
    {
        "name": "Silver ratio (1+√2)",
        "poly_coeffs": [1, -2, -1],           # x²−2x−1
        "approx": 2.4142135624,
        "conductor": 8,
    },
    {
        "name": "√5",
        "poly_coeffs": [1, 0, -5],            # x²−5
        "approx": 2.2360679775,
        "conductor": 5,
    },
    {
        "name": "2cos(2π/7)",
        "poly_coeffs": [1, 1, -2, -1],        # x³+x²−2x−1
        "approx": 1.2469796037,
        "conductor": 7,
    },
    {
        "name": "Lehmer's number",
        # x¹⁰+x⁹−x⁷−x⁶−x⁵−x⁴−x³+x+1
        "poly_coeffs": [1, 1, 0, -1, -1, -1, -1, -1, 0, 1, 1],
        "approx": 1.17628081826,
        "conductor": None,  # not cyclotomic
    },
]


def poly_from_coeffs(coeffs):
    """Return sympy Poly from descending coefficient list."""
    return Poly(sum(c * x**(len(coeffs)-1-i) for i, c in enumerate(coeffs)), x)


def mahler_measure(coeffs):
    """Product of max(1, |root|) over all roots of the polynomial."""
    # Use mpmath for numerical root finding at high precision
    degree = len(coeffs) - 1
    # Convert to mpmath polynomial and find roots
    mp_coeffs = [mpmath.mpf(c) for c in coeffs]
    roots = mpmath.polyroots(mp_coeffs)
    
    measure = mpmath.mpf(1)
    leading = abs(mpmath.mpf(coeffs[0]))
    measure *= leading  # Mahler measure includes |leading coeff|
    for r in roots:
        modulus = abs(r)
        if modulus > 1:
            measure *= modulus
    return float(measure)


def continued_fraction_expansion(value, n_terms=60):
    """Compute continued fraction partial quotients using mpmath high precision."""
    mpmath.mp.dps = 200
    val = mpmath.mpf(value)
    quotients = []
    for _ in range(n_terms):
        a = int(mpmath.floor(val))
        quotients.append(a)
        frac = val - a
        if frac < mpmath.mpf(10)**(-150):
            break
        val = 1 / frac
    return quotients


def cf_period_for_quadratic(coeffs):
    """
    For a quadratic irrational with monic polynomial ax²+bx+c,
    compute the periodic part of the CF expansion.
    Returns the period partial quotients.
    """
    # Expand enough terms, then detect the period
    a_coeff, b_coeff, c_coeff = coeffs
    # The root we want: use the positive root
    disc = b_coeff**2 - 4*a_coeff*c_coeff
    val = (-b_coeff + mpmath.sqrt(disc)) / (2*a_coeff)
    if val < 0:
        val = (-b_coeff - mpmath.sqrt(disc)) / (2*a_coeff)
    
    cfs = continued_fraction_expansion(float(val), 200)
    
    # For quadratic irrationals, CF is eventually periodic
    # Skip the non-periodic prefix, find the repeating block
    # Try to detect period by looking for repetition in tail
    # Standard: for sqrt(D), period starts at index 1
    # For general quadratic, detect by brute force
    for period_len in range(1, len(cfs)//2):
        # Check if cfs[start:start+period_len] repeats
        for start in range(min(5, len(cfs)//3)):
            matches = True
            for rep in range(1, 4):  # check 3 repetitions
                for j in range(period_len):
                    if start + rep*period_len + j >= len(cfs):
                        matches = False
                        break
                    if cfs[start + j] != cfs[start + rep*period_len + j]:
                        matches = False
                        break
                if not matches:
                    break
            if matches and period_len > 0:
                return cfs[start:start+period_len]
    
    # Fallback: return all quotients past the first
    return cfs[1:]


def cf_geometric_mean(coeffs, approx_value, degree):
    """
    Geometric mean of CF partial quotients.
    For quadratic irrationals: use one period.
    For higher degree: use first 50 partial quotients (skip a_0).
    """
    if degree == 2:
        period = cf_period_for_quadratic(coeffs)
        if period:
            # geometric mean of the period
            log_sum = sum(math.log(max(a, 1)) for a in period)
            return math.exp(log_sum / len(period)), period
        
    # Higher degree or fallback
    cfs = continued_fraction_expansion(approx_value, 55)
    quotients = cfs[1:51]  # skip a_0, take 50 partial quotients
    if not quotients:
        return float('inf'), cfs
    log_sum = sum(math.log(max(a, 1)) for a in quotients)
    return math.exp(log_sum / len(quotients)), quotients


def recurrence_complexity(coeffs):
    """
    The minimal polynomial IS the characteristic polynomial of the recurrence.
    Return (order, sum_of_abs_coefficients_excluding_leading).
    
    Polynomial: x^n + c_{n-1}x^{n-1} + ... + c_0
    Recurrence: a(n) = -c_{n-1}*a(n-1) - ... - c_0*a(n-n)
    The recurrence coefficients are the negatives of the non-leading poly coeffs.
    Complexity = sum of absolute values of recurrence coefficients.
    """
    order = len(coeffs) - 1
    # The recurrence coefficients are -coeffs[1:] / coeffs[0]
    # Since these are monic (leading coeff = 1 for most), divide by leading
    leading = coeffs[0]
    rec_coeffs = [-c / leading for c in coeffs[1:]]
    coeff_sum = sum(abs(c) for c in rec_coeffs)
    return order, int(coeff_sum)


def largest_real_root_hp(coeffs):
    """Compute the largest real root of a polynomial at high precision."""
    mpmath.mp.dps = 120
    roots = mpmath.polyroots([mpmath.mpf(c) for c in coeffs])
    real_roots = [mpmath.re(r) for r in roots if abs(mpmath.im(r)) < mpmath.mpf(10)**(-80)]
    return max(real_roots) if real_roots else None


def verify_conductor_pslq(coeffs, k):
    """
    Verify that the largest real root of poly lives in Q(2cos(2π/k)) using PSLQ.
    """
    from sympy import totient
    mpmath.mp.dps = 120
    
    alpha = largest_real_root_hp(coeffs)
    if alpha is None:
        return False
    
    phi_k = int(totient(k))
    d = phi_k // 2
    if d == 0:
        return False
    
    beta = 2 * mpmath.cos(2 * mpmath.pi / k)
    powers = [beta**j for j in range(d)]
    vec = list(powers) + [-alpha]
    
    try:
        relation = mpmath.pslq(vec)
    except Exception:
        return False
    
    if relation is not None and relation[-1] != 0:
        check = sum(r * v for r, v in zip(relation, vec))
        return abs(check) < mpmath.mpf(10)**(-50)
    return False


def main():
    results = []
    
    print("=" * 100)
    print("ALGEBRAIC SIMPLICITY vs UBIQUITY TABLE")
    print("=" * 100)
    print()
    
    for const in CONSTANTS:
        name = const["name"]
        coeffs = const["poly_coeffs"]
        approx = const["approx"]
        known_conductor = const["conductor"]
        degree = len(coeffs) - 1
        
        # 1. Mahler measure
        mm = mahler_measure(coeffs)
        
        # 2. CF convergence rate
        cf_gmean, cf_data = cf_geometric_mean(coeffs, approx, degree)
        
        # 3. Cyclotomic conductor (known values from number theory; verify via PSLQ)
        conductor = known_conductor
        if known_conductor is not None:
            conductor_verified = verify_conductor_pslq(coeffs, known_conductor)
        else:
            conductor_verified = True  # "none" is the known answer
        
        # 4. Recurrence complexity
        rec_order, rec_coeff_sum = recurrence_complexity(coeffs)
        
        entry = {
            "name": name,
            "poly": format_poly(coeffs),
            "approx": approx,
            "mahler_measure": round(mm, 6),
            "cf_geometric_mean": round(cf_gmean, 4),
            "cf_data_sample": cf_data[:20] if isinstance(cf_data, list) else cf_data,
            "conductor": conductor,
            "conductor_verified": conductor_verified,
            "recurrence_order": rec_order,
            "recurrence_coeff_sum": rec_coeff_sum,
            "recurrence_total_complexity": rec_order + rec_coeff_sum,
        }
        results.append(entry)
        
    # ── Print table ──
    print(f"{'Constant':<22} {'Min. Poly':<28} {'≈ Value':>8} {'Mahler':>8} "
          f"{'CF GM':>8} {'Cond.':>7} {'Rec.Ord':>8} {'Rec.|Σc|':>9} {'Rec.Tot':>8}")
    print("─" * 120)
    
    for r in results:
        cond_str = str(r["conductor"]) if r["conductor"] is not None else "∞"
        ver_str = "" if r.get("conductor_verified", True) else " ✗"
        print(f"{r['name']:<22} {r['poly']:<28} {r['approx']:>8.4f} {r['mahler_measure']:>8.4f} "
              f"{r['cf_geometric_mean']:>8.4f} {cond_str:>6}{ver_str} {r['recurrence_order']:>8} "
              f"{r['recurrence_coeff_sum']:>9} {r['recurrence_total_complexity']:>8}")
    
    print()
    
    # ── Rankings ──
    print("=" * 100)
    print("RANKINGS BY MAHLER MEASURE (ascending = simpler)")
    print("=" * 100)
    
    ranked = sorted(results, key=lambda r: r["mahler_measure"])
    for i, r in enumerate(ranked):
        print(f"  {i+1}. {r['name']:<22} Mahler={r['mahler_measure']:.6f}")
    
    print()
    
    # ── Correlation analysis ──
    print("=" * 100)
    print("CORRELATION ANALYSIS")
    print("=" * 100)
    print()
    
    # Rank by each measure
    n = len(results)
    
    # Mahler measure rank
    mm_sorted = sorted(range(n), key=lambda i: results[i]["mahler_measure"])
    mm_rank = [0] * n
    for rank, idx in enumerate(mm_sorted):
        mm_rank[idx] = rank + 1
    
    # CF geometric mean rank (ascending = most irrational = smallest GM)
    cf_sorted = sorted(range(n), key=lambda i: results[i]["cf_geometric_mean"])
    cf_rank = [0] * n
    for rank, idx in enumerate(cf_sorted):
        cf_rank[idx] = rank + 1
    
    # Recurrence total complexity rank
    rec_sorted = sorted(range(n), key=lambda i: results[i]["recurrence_total_complexity"])
    rec_rank = [0] * n
    for rank, idx in enumerate(rec_sorted):
        rec_rank[idx] = rank + 1
    
    # Print rank comparison table
    print(f"{'Constant':<22} {'MM Rank':>8} {'CF Rank':>8} {'Rec Rank':>9} {'Cond.':>7}")
    print("─" * 60)
    for i, r in enumerate(results):
        cond_str = str(r["conductor"]) if r["conductor"] is not None else "∞"
        print(f"{r['name']:<22} {mm_rank[i]:>8} {cf_rank[i]:>8} {rec_rank[i]:>9} {cond_str:>7}")
    
    print()
    
    # Spearman correlations
    # 1. Mahler vs CF
    rho_cf, p_cf = spearmanr(mm_rank, cf_rank)
    print(f"Spearman(Mahler rank, CF convergence rank):     ρ = {rho_cf:+.4f}, p = {p_cf:.4f}")
    
    # 2. Mahler vs Recurrence
    rho_rec, p_rec = spearmanr(mm_rank, rec_rank)
    print(f"Spearman(Mahler rank, Recurrence complexity):   ρ = {rho_rec:+.4f}, p = {p_rec:.4f}")
    
    # 3. Mahler vs Conductor (cyclotomic entries only)
    cyc_indices = [i for i in range(n) if results[i]["conductor"] is not None]
    if len(cyc_indices) >= 3:
        cyc_mm = [mm_rank[i] for i in cyc_indices]
        cyc_cond = [results[i]["conductor"] for i in cyc_indices]
        # Rank conductors
        cond_sorted = sorted(range(len(cyc_indices)), key=lambda j: cyc_cond[j])
        cond_rank = [0] * len(cyc_indices)
        for rank, idx in enumerate(cond_sorted):
            cond_rank[idx] = rank + 1
        rho_cond, p_cond = spearmanr(cyc_mm, cond_rank)
        print(f"Spearman(Mahler rank, Conductor rank) [cycl.]:  ρ = {rho_cond:+.4f}, p = {p_cond:.4f}")
        print(f"  (cyclotomic entries: {[results[i]['name'] for i in cyc_indices]})")
    
    print()
    
    # ── φ outlier analysis ──
    print("=" * 100)
    print("φ OUTLIER ANALYSIS")
    print("=" * 100)
    print()
    
    phi_idx = 0  # φ is first in our list
    phi_name = results[phi_idx]["name"]
    print(f"{phi_name}:")
    print(f"  Mahler measure rank:      {mm_rank[phi_idx]} / {n}")
    print(f"  CF convergence rank:      {cf_rank[phi_idx]} / {n}")
    print(f"  Recurrence complexity:    {rec_rank[phi_idx]} / {n}")
    print(f"  Cyclotomic conductor:     {results[phi_idx]['conductor']}")
    print()
    
    # Is φ at the endpoint of all rankings?
    phi_is_simplest_mahler = mm_rank[phi_idx] == 1
    phi_is_most_irrational_cf = cf_rank[phi_idx] == 1
    phi_is_simplest_recurrence = rec_rank[phi_idx] == 1
    phi_has_smallest_conductor = results[phi_idx]["conductor"] == min(
        r["conductor"] for r in results if r["conductor"] is not None
    )
    
    print(f"  Simplest by Mahler?       {'YES' if phi_is_simplest_mahler else 'NO'}")
    print(f"  Most irrational by CF?    {'YES' if phi_is_most_irrational_cf else 'NO'}")
    print(f"  Simplest recurrence?      {'YES' if phi_is_simplest_recurrence else 'NO'}")
    print(f"  Smallest conductor?       {'YES' if phi_has_smallest_conductor else 'NO'}")
    print()
    
    if all([phi_is_simplest_mahler, phi_is_most_irrational_cf, 
            phi_is_simplest_recurrence, phi_has_smallest_conductor]):
        print("  ▶ CONCLUSION: φ is at the ENDPOINT of ALL simplicity rankings.")
        print("    Its ubiquity is monotonically predicted by algebraic simplicity.")
        conclusion = "monotone_endpoint"
    else:
        outlier_on = []
        if not phi_is_simplest_mahler: outlier_on.append("Mahler measure")
        if not phi_is_most_irrational_cf: outlier_on.append("CF convergence")
        if not phi_is_simplest_recurrence: outlier_on.append("Recurrence complexity")
        if not phi_has_smallest_conductor: outlier_on.append("Cyclotomic conductor")
        print(f"  ▶ SURPRISE: φ is NOT at the endpoint on: {', '.join(outlier_on)}")
        print("    Something specific to x²−x−1 may matter beyond algebraic minimality.")
        conclusion = f"outlier_on:{','.join(outlier_on)}"
    
    print()
    
    # ── CF detail ──
    print("=" * 100)
    print("CONTINUED FRACTION DETAIL")
    print("=" * 100)
    for r in results:
        cf_sample = r["cf_data_sample"]
        print(f"  {r['name']:<22} CF = [{', '.join(str(x) for x in cf_sample[:15])}{'...' if len(cf_sample) > 15 else ''}]  GM = {r['cf_geometric_mean']:.4f}")
    
    print()
    
    # ── Save JSON ──
    output = {
        "constants": [{k: v for k, v in r.items()} for r in results],
        "correlations": {
            "mahler_vs_cf": {"rho": round(rho_cf, 4), "p": round(p_cf, 4)},
            "mahler_vs_recurrence": {"rho": round(rho_rec, 4), "p": round(p_rec, 4)},
        },
        "phi_analysis": {
            "simplest_mahler": phi_is_simplest_mahler,
            "most_irrational_cf": phi_is_most_irrational_cf,
            "simplest_recurrence": phi_is_simplest_recurrence,
            "smallest_conductor": phi_has_smallest_conductor,
            "conclusion": conclusion,
        }
    }
    
    if len(cyc_indices) >= 3:
        output["correlations"]["mahler_vs_conductor_cyclotomic"] = {
            "rho": round(rho_cond, 4), "p": round(p_cond, 4)
        }
    
    out_path = Path(__file__).parent / "algebraic_simplicity_results.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Results saved to {out_path}")


def format_poly(coeffs):
    """Format polynomial from descending coefficients."""
    degree = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        d = degree - i
        if c == 0:
            continue
        if d == 0:
            terms.append(f"{c:+d}")
        elif d == 1:
            if c == 1:
                terms.append("+x")
            elif c == -1:
                terms.append("-x")
            else:
                terms.append(f"{c:+d}x")
        else:
            if c == 1:
                terms.append(f"+x^{d}")
            elif c == -1:
                terms.append(f"-x^{d}")
            else:
                terms.append(f"{c:+d}x^{d}")
    result = "".join(terms)
    if result.startswith("+"):
        result = result[1:]
    return result


if __name__ == "__main__":
    main()
