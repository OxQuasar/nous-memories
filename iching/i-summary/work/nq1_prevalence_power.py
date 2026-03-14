#!/usr/bin/env python3
"""
NQ1 — Prevalence power simulation

Is 凶's 13.5% prevalence a statistical sweet spot for detecting both
core (basin, ΔR²≈0.063) and shell (surface_relation+rank+palace_element, ΔR²≈0.117)?

Simulate detection power across prevalences.
"""

import numpy as np
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

N = 384  # hexagram-line pairs
N_REPS = 1000

# Basin structure: Kun=96, Cycle=192, Qian=96
basin_labels = np.array([0]*96 + [1]*192 + [2]*96)  # 0=Kun, 1=Cycle, 2=Qian

# Surface relation distribution: 5 levels
# Approximate split: 72/78/72/84/78
sr_labels = np.concatenate([
    np.full(72, 0), np.full(78, 1), np.full(72, 2),
    np.full(84, 3), np.full(78, 4)
])
# Shuffle to avoid correlation with basin
np.random.shuffle(sr_labels)

# Effect sizes (log-odds scale, calibrated to approximate ΔR² values)
# ΔR²≈0.063 for basin → moderate effect
# ΔR²≈0.117 for shell → larger effect

# Basin log-odds (relative to Cycle=reference):
# Kun and Qian differ from Cycle
BASIN_EFFECTS = {0: 0.6, 1: 0.0, 2: -0.3}  # Kun high, Qian low

# Shell effects (5-level surface_relation)
SHELL_EFFECTS = {0: 0.4, 1: -0.2, 2: 0.3, 3: -0.1, 4: -0.4}

def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))

def generate_marker(prevalence, basin_effect_scale, shell_effect_scale):
    """Generate binary marker with given prevalence and effect sizes."""
    # Compute intercept for desired prevalence
    # p = logistic(intercept + basin_effect + shell_effect)
    # Start with rough intercept, then calibrate
    
    basin_contrib = np.array([BASIN_EFFECTS[b] for b in basin_labels]) * basin_effect_scale
    shell_contrib = np.array([SHELL_EFFECTS[s] for s in sr_labels]) * shell_effect_scale
    
    # Find intercept that gives desired marginal prevalence
    # Binary search
    lo, hi = -10, 10
    for _ in range(50):
        mid = (lo + hi) / 2
        probs = logistic(mid + basin_contrib + shell_contrib)
        if probs.mean() < prevalence:
            lo = mid
        else:
            hi = mid
    intercept = (lo + hi) / 2
    
    probs = logistic(intercept + basin_contrib + shell_contrib)
    marker = (np.random.random(N) < probs).astype(int)
    return marker

def lr_test(y, X_full, X_reduced):
    """Likelihood ratio test comparing full vs reduced logistic regression.
    Returns p-value. Uses manual Newton-Raphson for speed."""
    def log_likelihood(X, beta, y):
        z = X @ beta
        z = np.clip(z, -20, 20)
        p = logistic(z)
        p = np.clip(p, 1e-10, 1-1e-10)
        return np.sum(y * np.log(p) + (1-y) * np.log(1-p))
    
    def fit_logistic(X, y, max_iter=25):
        beta = np.zeros(X.shape[1])
        for _ in range(max_iter):
            z = X @ beta
            z = np.clip(z, -20, 20)
            p = logistic(z)
            p = np.clip(p, 1e-10, 1-1e-10)
            W = p * (1 - p)
            # Hessian
            H = X.T @ (W[:, None] * X)
            # Gradient
            g = X.T @ (y - p)
            try:
                delta = np.linalg.solve(H + 1e-8 * np.eye(H.shape[0]), g)
            except np.linalg.LinAlgError:
                break
            beta += delta
            if np.max(np.abs(delta)) < 1e-6:
                break
        return beta
    
    beta_full = fit_logistic(X_full, y)
    beta_red = fit_logistic(X_reduced, y)
    
    ll_full = log_likelihood(X_full, beta_full, y)
    ll_red = log_likelihood(X_reduced, beta_red, y)
    
    lr_stat = 2 * (ll_full - ll_red)
    df = X_full.shape[1] - X_reduced.shape[1]
    
    if lr_stat < 0:
        lr_stat = 0
    
    from scipy.stats import chi2
    p_val = chi2.sf(lr_stat, df)
    return p_val

# Build design matrices
# Position: 6 dummy variables (for line positions 1-6, using 1 as reference)
position = np.tile(np.arange(6), 64)  # 384 positions
X_pos = np.zeros((N, 5))
for i in range(5):
    X_pos[:, i] = (position == (i+1)).astype(float)

# Basin: 2 dummy variables (Cycle as reference)
X_basin = np.zeros((N, 2))
X_basin[:, 0] = (basin_labels == 0).astype(float)  # Kun
X_basin[:, 1] = (basin_labels == 2).astype(float)  # Qian

# Shell: 4 dummy variables for surface_relation (level 0 as reference)
X_shell = np.zeros((N, 4))
for i in range(4):
    X_shell[:, i] = (sr_labels == (i+1)).astype(float)

# Intercept
ones = np.ones((N, 1))

# Model matrices:
# Reduced: intercept + position
X_base = np.hstack([ones, X_pos])

# Core model: base + basin
X_core = np.hstack([X_base, X_basin])

# Shell model: base + shell
X_shell_full = np.hstack([X_base, X_shell])

# Full model: base + basin + shell
X_full = np.hstack([X_base, X_basin, X_shell])

# ═══════════════════════════════════════════════════════════════
# Run simulations
# ═══════════════════════════════════════════════════════════════

prevalences = [0.05, 0.10, 0.135, 0.20, 0.30, 0.50]

# Calibrate effect scales to match target ΔR²
# Use moderate effects that produce the right order of magnitude
CORE_SCALE = 1.0  # tuned to give ΔR²≈0.06
SHELL_SCALE = 1.2  # tuned to give ΔR²≈0.12

print("=" * 72)
print("NQ1: PREVALENCE POWER SIMULATION")
print("=" * 72)
print(f"\nN = {N}, N_REPS = {N_REPS}")
print(f"Basin: Kun={96}, Cycle={192}, Qian={96}")
print(f"Effect scales: core={CORE_SCALE}, shell={SHELL_SCALE}")
print(f"Prevalences: {prevalences}")

results = {}

for pi in prevalences:
    print(f"\n--- Prevalence π = {pi} ---")
    
    core_sig = 0
    shell_sig = 0
    dual_sig = 0
    core_pvals = []
    shell_pvals = []
    
    for rep in range(N_REPS):
        y = generate_marker(pi, CORE_SCALE, SHELL_SCALE)
        
        # Skip if degenerate (all 0 or all 1)
        if y.sum() == 0 or y.sum() == N:
            continue
        
        # LR test for core: full=(base+basin+shell) vs reduced=(base+shell)
        p_core = lr_test(y, X_full, X_shell_full)
        
        # LR test for shell: full=(base+basin+shell) vs reduced=(base+basin)  
        p_shell = lr_test(y, X_full, X_core)
        
        core_pvals.append(p_core)
        shell_pvals.append(p_shell)
        
        is_core_sig = p_core < 0.05
        is_shell_sig = p_shell < 0.05
        
        if is_core_sig:
            core_sig += 1
        if is_shell_sig:
            shell_sig += 1
        if is_core_sig and is_shell_sig:
            dual_sig += 1
    
    valid = len(core_pvals)
    core_power = core_sig / valid if valid > 0 else 0
    shell_power = shell_sig / valid if valid > 0 else 0
    dual_power = dual_sig / valid if valid > 0 else 0
    
    print(f"  Valid replicates: {valid}")
    print(f"  Core power:  {core_power:.3f} ({core_sig}/{valid})")
    print(f"  Shell power: {shell_power:.3f} ({shell_sig}/{valid})")
    print(f"  Dual power:  {dual_power:.3f} ({dual_sig}/{valid})")
    
    results[pi] = {
        'core_power': core_power,
        'shell_power': shell_power,
        'dual_power': dual_power,
        'core_sig': core_sig,
        'shell_sig': shell_sig,
        'dual_sig': dual_sig,
        'valid': valid,
    }

# ═══════════════════════════════════════════════════════════════
# Summary table
# ═══════════════════════════════════════════════════════════════

print(f"\n{'='*72}")
print(f"SUMMARY: POWER CURVES")
print(f"{'='*72}")
print(f"\n{'π':>8s} {'Core':>8s} {'Shell':>8s} {'Dual':>8s} {'Dual−max':>10s}")
print(f"{'---':>8s} {'---':>8s} {'---':>8s} {'---':>8s} {'---':>10s}")

max_dual = max(r['dual_power'] for r in results.values())
for pi in prevalences:
    r = results[pi]
    gap = r['dual_power'] - max_dual
    marker = " ←" if abs(gap) < 0.001 else ""
    print(f"{pi:8.3f} {r['core_power']:8.3f} {r['shell_power']:8.3f} {r['dual_power']:8.3f} {gap:+10.3f}{marker}")

# Find optimal
best_pi = max(results.keys(), key=lambda pi: results[pi]['dual_power'])
print(f"\nMaximum dual power at π = {best_pi}")
print(f"  Core={results[best_pi]['core_power']:.3f}, Shell={results[best_pi]['shell_power']:.3f}, Dual={results[best_pi]['dual_power']:.3f}")

# Is 13.5% unique or is the curve flat?
powers = [results[pi]['dual_power'] for pi in prevalences]
range_power = max(powers) - min(powers)
print(f"\nDual power range: {range_power:.3f}")
if range_power < 0.05:
    print("  → Curve is FLAT: prevalence doesn't matter much")
elif best_pi == 0.135:
    print("  → 13.5% IS near the optimum for dual detection")
else:
    print(f"  → Optimum is at {best_pi}, not at 13.5%")
    print(f"  → 'Why 凶?' is NOT explained by prevalence alone")

print(f"\nDone.")
