"""
Round 3: Is kernel uniformity (chi²) independent of OMI-XOR dominance?

Replicates the Thread E random completion framework:
  - KW's Eulerian orbit path (fixed)
  - KW's matching (mask=sig, fixed)
  - Random pair assignment + orientation per orbit (the free variable)

For each of 50,000 samples, compute:
  1. chi² of kernel frequency from uniform
  2. OMI fraction of consecutive kernel XORs (count OMI / 30)
  3. Mean XOR Hamming weight (average distance between consecutive kernels)

Then: joint distribution, conditional analysis, correlation.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter, defaultdict
from sequence import KING_WEN, all_bits
import random
import time
import math

DIMS = 6
M = all_bits()

KERNEL_NAMES = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI',
}

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])


# ─── Setup: KW orbit walk and pair structure ─────────────────────────────────

kw_hex_seq = [tuple(M[i]) for i in range(64)]
kw_orbit_walk = [xor_sig(kw_hex_seq[2*k]) for k in range(32)]

# KW's orbit pairs (mask=sig matching)
kw_orbit_pairs = defaultdict(list)
for k in range(32):
    a, b = kw_hex_seq[2*k], kw_hex_seq[2*k+1]
    kw_orbit_pairs[xor_sig(a)].append((a, b))


def random_completion(rng):
    """Random pair assignment + orientation on KW's Eulerian path with KW's matching."""
    orbit_queues = {}
    for sig, pairs in kw_orbit_pairs.items():
        shuffled = list(pairs)
        rng.shuffle(shuffled)
        oriented = []
        for a, b in shuffled:
            if rng.random() < 0.5:
                oriented.append((a, b))
            else:
                oriented.append((b, a))
        orbit_queues[sig] = oriented

    seq = []
    visit_count = defaultdict(int)
    for k in range(32):
        sig = kw_orbit_walk[k]
        idx = visit_count[sig]
        visit_count[sig] += 1
        seq.extend(orbit_queues[sig][idx])
    return seq


def kernel_metrics(seq):
    """Extract chi², OMI-XOR fraction, mean XOR weight, full XOR dist from a 64-hex sequence."""
    # Extract kernel chain (31 bridges)
    kernels = []
    for k in range(31):
        a, b = seq[2*k + 1], seq[2*k + 2]
        mask = tuple(a[d] ^ b[d] for d in range(DIMS))
        kernels.append((mask[5], mask[4], mask[3]))

    # Chi² from uniform
    freq = Counter(kernels)
    expected = 31 / 8
    chi2 = sum((freq.get(k, 0) - expected) ** 2 / expected
               for k in KERNEL_NAMES.keys())

    # Consecutive XOR chain (30 elements)
    xors = [tuple(kernels[i][d] ^ kernels[i+1][d] for d in range(3))
            for i in range(30)]

    xor_freq = Counter(xors)
    omi_count = xor_freq.get((1,1,1), 0)
    omi_frac = omi_count / 30

    # Mean XOR Hamming weight
    xor_weights = [sum(x) for x in xors]
    mean_xor_weight = sum(xor_weights) / 30

    # id count (consecutive repeat)
    id_count = xor_freq.get((0,0,0), 0)

    return chi2, omi_frac, mean_xor_weight, omi_count, id_count, xor_freq


# ─── KW reference values ─────────────────────────────────────────────────────

kw_chi2, kw_omi_frac, kw_mean_xw, kw_omi_count, kw_id_count, kw_xor_freq = kernel_metrics(kw_hex_seq)

print("=" * 70)
print("KERNEL INDEPENDENCE ANALYSIS")
print("=" * 70)

print(f"\nKW reference values:")
print(f"  Chi² (kernel uniformity):     {kw_chi2:.3f}")
print(f"  OMI-XOR fraction:             {kw_omi_frac:.4f} ({kw_omi_count}/30)")
print(f"  Mean XOR Hamming weight:      {kw_mean_xw:.4f}")
print(f"  id-XOR count (repeats):       {kw_id_count}")

print(f"\n  Full KW XOR distribution:")
for k in sorted(kw_xor_freq.keys()):
    name = KERNEL_NAMES[k]
    cnt = kw_xor_freq[k]
    w = sum(k)
    print(f"    {name:>3s} (w={w}): {cnt}/30 = {100*cnt/30:.1f}%")


# ─── Main sampling loop ──────────────────────────────────────────────────────

N = 50_000
rng = random.Random(42)

print(f"\nSampling {N} random completions...")
t0 = time.time()

chi2_vals = []
omi_frac_vals = []
mean_xw_vals = []
omi_count_vals = []
id_count_vals = []
# Store full XOR weight distribution per sample
xor_weight_dists = []  # list of Counter({0: n0, 1: n1, 2: n2, 3: n3})

for i in range(N):
    seq = random_completion(rng)
    chi2, omi_frac, mean_xw, omi_count, id_count, xor_freq = kernel_metrics(seq)
    chi2_vals.append(chi2)
    omi_frac_vals.append(omi_frac)
    mean_xw_vals.append(mean_xw)
    omi_count_vals.append(omi_count)
    id_count_vals.append(id_count)

    # XOR weight distribution
    wd = Counter()
    for k, cnt in xor_freq.items():
        wd[sum(k)] += cnt
    xor_weight_dists.append(wd)

    if (i + 1) % 10000 == 0:
        print(f"  {i+1}/{N} ({time.time()-t0:.1f}s)")

t1 = time.time()
print(f"Done in {t1-t0:.1f}s")


# ═══════════════════════════════════════════════════════════════════════════════
# 1. MARGINAL DISTRIBUTIONS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'='*70}")
print("1. MARGINAL DISTRIBUTIONS")
print(f"{'='*70}")

def stats(vals, kw_val, label):
    mean = sum(vals) / len(vals)
    std = (sum((v - mean)**2 for v in vals) / len(vals)) ** 0.5
    p_le = sum(1 for v in vals if v <= kw_val) / len(vals)
    p_ge = sum(1 for v in vals if v >= kw_val) / len(vals)
    print(f"\n  {label}:")
    print(f"    KW = {kw_val:.4f}")
    print(f"    Sample: {mean:.4f} ± {std:.4f}")
    print(f"    P(≤ KW) = {p_le:.4f}  ({100*p_le:.2f}%)")
    print(f"    P(≥ KW) = {p_ge:.4f}  ({100*p_ge:.2f}%)")
    return p_le, p_ge

p_chi2_le, _ = stats(chi2_vals, kw_chi2, "Chi² (lower = more uniform)")
_, p_omi_ge = stats(omi_frac_vals, kw_omi_frac, "OMI-XOR fraction (higher = more contrastive)")
_, p_xw_ge = stats(mean_xw_vals, kw_mean_xw, "Mean XOR weight (higher = more distant)")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. CORRELATION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'='*70}")
print("2. CORRELATION: Chi² vs OMI-XOR fraction")
print(f"{'='*70}")

# Pearson correlation
mean_chi2 = sum(chi2_vals) / N
mean_omi = sum(omi_frac_vals) / N

cov = sum((c - mean_chi2) * (o - mean_omi) for c, o in zip(chi2_vals, omi_frac_vals)) / N
var_chi2 = sum((c - mean_chi2)**2 for c in chi2_vals) / N
var_omi = sum((o - mean_omi)**2 for o in omi_frac_vals) / N
r = cov / (var_chi2 * var_omi) ** 0.5 if var_chi2 > 0 and var_omi > 0 else 0

print(f"\n  Pearson r(chi², OMI_frac) = {r:.4f}")
print(f"  (negative = uniform chains tend to have MORE OMI; positive = they tend to have LESS)")

# Correlation between chi² and mean XOR weight
mean_xw_mean = sum(mean_xw_vals) / N
cov_xw = sum((c - mean_chi2) * (w - mean_xw_mean) for c, w in zip(chi2_vals, mean_xw_vals)) / N
var_xw = sum((w - mean_xw_mean)**2 for w in mean_xw_vals) / N
r_xw = cov_xw / (var_chi2 * var_xw) ** 0.5 if var_chi2 > 0 and var_xw > 0 else 0
print(f"  Pearson r(chi², mean_xor_weight) = {r_xw:.4f}")

# Correlation between OMI frac and mean XOR weight
cov_omi_xw = sum((o - mean_omi) * (w - mean_xw_mean) for o, w in zip(omi_frac_vals, mean_xw_vals)) / N
r_omi_xw = cov_omi_xw / (var_omi * var_xw) ** 0.5 if var_omi > 0 and var_xw > 0 else 0
print(f"  Pearson r(OMI_frac, mean_xor_weight) = {r_omi_xw:.4f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. CONDITIONAL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'='*70}")
print("3. CONDITIONAL ANALYSIS")
print(f"{'='*70}")

# A. Among uniform chains (chi² ≤ KW), what's the OMI distribution?
uniform_mask = [chi2_vals[i] <= kw_chi2 for i in range(N)]
n_uniform = sum(uniform_mask)
uniform_omi = [omi_frac_vals[i] for i in range(N) if uniform_mask[i]]

print(f"\n  A. Conditioning on chi² ≤ {kw_chi2:.3f} (n = {n_uniform}, {100*n_uniform/N:.1f}%)")
if n_uniform > 0:
    mean_omi_cond = sum(uniform_omi) / n_uniform
    std_omi_cond = (sum((o - mean_omi_cond)**2 for o in uniform_omi) / n_uniform) ** 0.5
    p_omi_ge_cond = sum(1 for o in uniform_omi if o >= kw_omi_frac) / n_uniform
    print(f"    OMI-XOR fraction: {mean_omi_cond:.4f} ± {std_omi_cond:.4f}")
    print(f"    (Unconditional:   {mean_omi:.4f} ± {(var_omi**0.5):.4f})")
    print(f"    P(OMI ≥ KW | uniform) = {p_omi_ge_cond:.4f} ({100*p_omi_ge_cond:.2f}%)")
    print(f"    (Unconditional P(OMI ≥ KW) = {sum(1 for o in omi_frac_vals if o >= kw_omi_frac)/N:.4f})")

# B. Among OMI-rich chains (OMI ≥ KW), what's the chi² distribution?
omi_mask = [omi_frac_vals[i] >= kw_omi_frac for i in range(N)]
n_omi_rich = sum(omi_mask)
omi_chi2 = [chi2_vals[i] for i in range(N) if omi_mask[i]]

print(f"\n  B. Conditioning on OMI ≥ {kw_omi_frac:.4f} (n = {n_omi_rich}, {100*n_omi_rich/N:.1f}%)")
if n_omi_rich > 0:
    mean_chi2_cond = sum(omi_chi2) / n_omi_rich
    std_chi2_cond = (sum((c - mean_chi2_cond)**2 for c in omi_chi2) / n_omi_rich) ** 0.5
    p_chi2_le_cond = sum(1 for c in omi_chi2 if c <= kw_chi2) / n_omi_rich
    print(f"    Chi²: {mean_chi2_cond:.3f} ± {std_chi2_cond:.3f}")
    print(f"    (Unconditional: {mean_chi2:.3f} ± {(var_chi2**0.5):.3f})")
    print(f"    P(chi² ≤ KW | OMI-rich) = {p_chi2_le_cond:.4f} ({100*p_chi2_le_cond:.2f}%)")

# C. Among chains with high mean XOR weight (≥ KW), what's the chi² and OMI distribution?
xw_mask = [mean_xw_vals[i] >= kw_mean_xw for i in range(N)]
n_xw_high = sum(xw_mask)
print(f"\n  C. Conditioning on mean XOR weight ≥ {kw_mean_xw:.4f} (n = {n_xw_high}, {100*n_xw_high/N:.1f}%)")
if n_xw_high > 0:
    xw_chi2 = [chi2_vals[i] for i in range(N) if xw_mask[i]]
    xw_omi = [omi_frac_vals[i] for i in range(N) if xw_mask[i]]
    print(f"    Chi²: {sum(xw_chi2)/n_xw_high:.3f} ± {(sum((c-sum(xw_chi2)/n_xw_high)**2 for c in xw_chi2)/n_xw_high)**0.5:.3f}")
    print(f"    OMI frac: {sum(xw_omi)/n_xw_high:.4f} ± {(sum((o-sum(xw_omi)/n_xw_high)**2 for o in xw_omi)/n_xw_high)**0.5:.4f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. JOINT P-VALUE
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'='*70}")
print("4. JOINT P-VALUES")
print(f"{'='*70}")

# Joint: chi² ≤ KW AND OMI ≥ KW
n_both = sum(1 for i in range(N) if chi2_vals[i] <= kw_chi2 and omi_frac_vals[i] >= kw_omi_frac)
p_both = n_both / N
p_if_independent = p_chi2_le * (sum(1 for o in omi_frac_vals if o >= kw_omi_frac) / N)

print(f"\n  P(chi² ≤ KW AND OMI ≥ KW) = {n_both}/{N} = {p_both:.5f} ({100*p_both:.3f}%)")
print(f"  If independent: {p_chi2_le:.4f} × {sum(1 for o in omi_frac_vals if o >= kw_omi_frac)/N:.4f} = {p_if_independent:.5f}")
print(f"  Ratio (observed / independent): {p_both / p_if_independent:.3f}" if p_if_independent > 0 else "  Cannot compute ratio")

# Triple joint: chi² ≤ KW AND OMI ≥ KW AND mean_xw ≥ KW
n_triple = sum(1 for i in range(N) if chi2_vals[i] <= kw_chi2 and omi_frac_vals[i] >= kw_omi_frac and mean_xw_vals[i] >= kw_mean_xw)
p_triple = n_triple / N
print(f"\n  P(chi² ≤ KW AND OMI ≥ KW AND xw ≥ KW) = {n_triple}/{N} = {p_triple:.5f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. XOR WEIGHT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'='*70}")
print("5. XOR WEIGHT DISTRIBUTION")
print(f"{'='*70}")

# KW XOR weight distribution
kw_xor_weights = Counter()
for k, cnt in kw_xor_freq.items():
    kw_xor_weights[sum(k)] += cnt

print(f"\n  XOR Hamming weight distribution:")
print(f"  {'Weight':>6s}  {'KW':>6s}  {'KW%':>6s}  {'Sample mean':>12s}  {'Sample%':>8s}")
print(f"  {'─'*6}  {'─'*6}  {'─'*6}  {'─'*12}  {'─'*8}")

for w in range(4):
    kw_cnt = kw_xor_weights.get(w, 0)
    kw_pct = 100 * kw_cnt / 30
    sample_cnts = [xor_weight_dists[i].get(w, 0) for i in range(N)]
    sample_mean = sum(sample_cnts) / N
    sample_pct = 100 * sample_mean / 30
    print(f"  {w:>6d}  {kw_cnt:>6d}  {kw_pct:>5.1f}%  {sample_mean:>11.2f}  {sample_pct:>6.1f}%")

# Expected weights: 1 element has weight 0 (id), 3 have weight 1 (O,M,I), 
# 3 have weight 2 (OM,OI,MI), 1 has weight 3 (OMI). If XOR is uniform over 
# the 8 elements: P(w=0)=1/8, P(w=1)=3/8, P(w=2)=3/8, P(w=3)=1/8.
print(f"\n  Expected under uniform XOR:")
for w, expected_frac in [(0, 1/8), (1, 3/8), (2, 3/8), (3, 1/8)]:
    print(f"    w={w}: {100*expected_frac:.1f}% ({30*expected_frac:.2f}/30)")

print(f"\n  KW mean XOR weight: {kw_mean_xw:.4f}")
print(f"  Expected under uniform XOR: {(0*1 + 1*3 + 2*3 + 3*1)/8:.4f} = 1.500")
print(f"  Sample mean XOR weight: {sum(mean_xw_vals)/N:.4f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. BINNED CONDITIONAL: CHI² DECILES vs OMI FRACTION
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'='*70}")
print("6. CHI² DECILES vs OMI FRACTION")
print(f"{'='*70}")

sorted_indices = sorted(range(N), key=lambda i: chi2_vals[i])
decile_size = N // 10

print(f"\n  {'Decile':>7s}  {'Chi² range':>18s}  {'Mean OMI':>10s}  {'Mean XOR wt':>12s}  {'P(OMI≥KW)':>10s}")
print(f"  {'─'*7}  {'─'*18}  {'─'*10}  {'─'*12}  {'─'*10}")

for d in range(10):
    start = d * decile_size
    end = (d + 1) * decile_size if d < 9 else N
    indices = sorted_indices[start:end]
    chi2_lo = chi2_vals[indices[0]]
    chi2_hi = chi2_vals[indices[-1]]
    omi_vals = [omi_frac_vals[i] for i in indices]
    xw_vals = [mean_xw_vals[i] for i in indices]
    mean_omi_d = sum(omi_vals) / len(omi_vals)
    mean_xw_d = sum(xw_vals) / len(xw_vals)
    p_omi_ge_d = sum(1 for o in omi_vals if o >= kw_omi_frac) / len(omi_vals)
    label = f"D{d+1} (most unif)" if d == 0 else f"D{d+1} (least unif)" if d == 9 else f"D{d+1}"
    print(f"  {label:>16s}  [{chi2_lo:5.2f}, {chi2_hi:5.2f}]  {mean_omi_d:>9.4f}  {mean_xw_d:>11.4f}  {100*p_omi_ge_d:>8.2f}%")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

print(f"\n{'='*70}")
print("7. SUMMARY")
print(f"{'='*70}")

print(f"""
  Correlation r(chi², OMI_frac) = {r:.4f}
  
  Marginal p-values:
    P(chi² ≤ KW)  = {p_chi2_le:.4f}
    P(OMI ≥ KW)   = {sum(1 for o in omi_frac_vals if o >= kw_omi_frac)/N:.4f}
    P(xw ≥ KW)    = {sum(1 for w in mean_xw_vals if w >= kw_mean_xw)/N:.4f}
  
  Joint p-value:
    P(chi² ≤ KW AND OMI ≥ KW) = {p_both:.5f}
    Expected if independent     = {p_if_independent:.5f}
    Ratio                       = {p_both/p_if_independent:.3f}

  Conditional p-values:
    P(OMI ≥ KW | chi² ≤ KW) = {p_omi_ge_cond:.4f}  (vs marginal {sum(1 for o in omi_frac_vals if o >= kw_omi_frac)/N:.4f})
""")

if abs(r) < 0.05:
    print("  CONCLUSION: Chi² and OMI-XOR are INDEPENDENT.")
    print("  KW has TWO separate design principles:")
    print("    1. Uniform kernel frequency (chi² signal)")
    print("    2. Maximal contrast between consecutive kernels (OMI-XOR signal)")
elif r < -0.05:
    print("  CONCLUSION: Chi² and OMI-XOR are NEGATIVELY CORRELATED.")
    print("  Uniform chains DO tend to have more OMI XORs.")
    if p_omi_ge_cond > 0.05:
        print("  The OMI signal is EXPLAINED BY uniformity — it's a side effect.")
        print("  KW has ONE design principle: kernel uniformity.")
    else:
        print("  But KW's OMI-XOR is extreme EVEN among uniform chains.")
        print("  KW has TWO design principles, partially correlated.")
else:
    print("  CONCLUSION: Chi² and OMI-XOR are POSITIVELY CORRELATED.")
    print("  This means: uniform chains tend to have FEWER OMI XORs.")
    print("  KW's combination of uniformity AND high OMI is even more remarkable.")
    print("  KW has TWO independent (or antagonistic) design principles.")

print(f"\n{'='*70}")
print("ANALYSIS COMPLETE")
print("=" * 70)
