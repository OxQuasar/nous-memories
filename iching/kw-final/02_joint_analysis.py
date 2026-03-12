#!/usr/bin/env python3
"""
KW Sequence Ordering — Joint Analysis

Loads null distributions from 01_null_distributions.npz.
Computes:
  1. Omnibus statistic: sum of squared z-scores across all metrics.
     Tests whether KW is jointly unusual even if no single metric discriminates.
  2. Triple joint count: fraction of null samples that simultaneously beat KW
     on the three most notable metrics (orbit_oneway_frac, torus_step_mean,
     complement_distance_mean).

Appends results to 01_ordering_results.md.
"""

from pathlib import Path
import numpy as np

SCRIPT_DIR = Path(__file__).parent

# ─── Load data ───────────────────────────────────────────────────────────────

def load_null_data():
    npz_path = SCRIPT_DIR / "01_null_distributions.npz"
    data = np.load(npz_path, allow_pickle=True)
    metric_names = list(data["metric_names"])
    kw_vals = {m: v for m, v in zip(metric_names, data["kw_metrics"])}
    null_arrays = {m: data[f"null_{m}"] for m in metric_names}
    return metric_names, kw_vals, null_arrays

# ─── Omnibus: sum of squared z-scores ───────────────────────────────────────

def compute_omnibus(metric_names, kw_vals, null_arrays):
    """
    For each sample (including KW), compute z-score per metric using null
    mean/std, then sum z². Compare KW's omnibus to the null distribution of
    omnibus values.
    """
    n_samples = len(next(iter(null_arrays.values())))
    null_means = {m: np.mean(null_arrays[m]) for m in metric_names}
    null_stds = {m: np.std(null_arrays[m]) for m in metric_names}

    # KW omnibus
    kw_zscores = {}
    kw_omnibus = 0.0
    for m in metric_names:
        if null_stds[m] > 0:
            z = (kw_vals[m] - null_means[m]) / null_stds[m]
        else:
            z = 0.0
        kw_zscores[m] = z
        kw_omnibus += z * z

    # Null omnibus distribution
    null_omnibus = np.zeros(n_samples)
    for m in metric_names:
        if null_stds[m] > 0:
            z_arr = (null_arrays[m] - null_means[m]) / null_stds[m]
        else:
            z_arr = np.zeros(n_samples)
        null_omnibus += z_arr * z_arr

    # Mid-rank percentile
    below = np.sum(null_omnibus < kw_omnibus)
    equal = np.sum(null_omnibus == kw_omnibus)
    pct = 100.0 * (below + 0.5 * equal) / n_samples

    return kw_omnibus, null_omnibus, pct, kw_zscores

# ─── Triple joint: three most notable metrics simultaneously ────────────────

def compute_triple_joint(kw_vals, null_arrays):
    """
    The three most notable metrics from the single-metric analysis:
      - orbit_oneway_frac: KW is HIGH (98.3rd %ile)
      - torus_step_mean: KW is LOW (9.5th %ile)
      - complement_distance_mean: KW is LOW (10.4th %ile)

    Count fraction of null samples that are simultaneously:
      - orbit_oneway_frac >= KW value AND
      - torus_step_mean <= KW value AND
      - complement_distance_mean <= KW value
    """
    triple_metrics = [
        ("orbit_oneway_frac", ">="),
        ("torus_step_mean", "<="),
        ("complement_distance_mean", "<="),
    ]

    n_samples = len(null_arrays["orbit_oneway_frac"])
    mask = np.ones(n_samples, dtype=bool)

    for m, direction in triple_metrics:
        kw_v = kw_vals[m]
        if direction == ">=":
            mask &= (null_arrays[m] >= kw_v)
        else:
            mask &= (null_arrays[m] <= kw_v)

    joint_count = np.sum(mask)
    joint_frac = joint_count / n_samples

    return triple_metrics, joint_count, joint_frac

# ─── Pairwise correlations among notable metrics ────────────────────────────

def compute_correlations(null_arrays):
    """Pearson correlations among the three notable metrics."""
    metrics = ["orbit_oneway_frac", "torus_step_mean", "complement_distance_mean"]
    corrs = {}
    for i, a in enumerate(metrics):
        for j, b in enumerate(metrics):
            if j > i:
                r = np.corrcoef(null_arrays[a], null_arrays[b])[0, 1]
                corrs[(a, b)] = r
    return metrics, corrs

# ─── Format and append ──────────────────────────────────────────────────────

def format_results(kw_omnibus, null_omnibus, omnibus_pct, kw_zscores,
                   triple_metrics, joint_count, joint_frac,
                   corr_metrics, correlations, metric_names):
    lines = []
    w = lines.append

    w("\n---\n")
    w("## Joint Analysis\n")

    # ── Omnibus ──
    w("### Omnibus Statistic (Σz²)\n")
    w(f"KW's sum of squared z-scores across all {len(metric_names)} metrics: **{kw_omnibus:.2f}**\n")
    w(f"| Statistic | Value |")
    w(f"|-----------|-------|")
    w(f"| KW Σz² | {kw_omnibus:.2f} |")
    w(f"| Null mean Σz² | {np.mean(null_omnibus):.2f} |")
    w(f"| Null std Σz² | {np.std(null_omnibus):.2f} |")
    w(f"| KW percentile | {omnibus_pct:.1f}% |")
    w(f"| KW z-score of Σz² | {(kw_omnibus - np.mean(null_omnibus)) / np.std(null_omnibus):+.2f} |")
    w("")

    if omnibus_pct > 95:
        w("**KW is jointly unusual** — the combination of metric deviations is unlikely under the null.\n")
    elif omnibus_pct > 90:
        w("KW is **moderately unusual** jointly — trending toward significance but not strong.\n")
    else:
        w("KW is **not jointly unusual** — metric deviations are within normal joint variation.\n")

    w("Per-metric z-scores feeding the omnibus:\n")
    w("| Metric | z | z² |")
    w("|--------|---|------|")
    for m in metric_names:
        z = kw_zscores[m]
        w(f"| {m} | {z:+.2f} | {z*z:.2f} |")
    w("")

    # ── Triple joint ──
    w("### Triple Joint Test\n")
    w("Simultaneous threshold on the three most notable single metrics:\n")
    for m, direction in triple_metrics:
        w(f"- **{m}** {direction} KW value")
    w("")
    w(f"| Statistic | Value |")
    w(f"|-----------|-------|")
    w(f"| Null samples meeting all three | {joint_count:,} / {len(null_omnibus):,} |")
    w(f"| Joint fraction | {joint_frac:.4f} ({joint_frac*100:.2f}%) |")
    expected_indep = 1.0
    for m, direction in triple_metrics:
        arr = null_omnibus  # placeholder, recompute marginals
        pass
    w("")

    if joint_frac < 0.01:
        w(f"**The triple conjunction is rare** — only {joint_frac*100:.2f}% of null samples match.")
        w("This suggests weak but real joint structure in the KW ordering.\n")
    elif joint_frac < 0.05:
        w(f"The triple conjunction is **uncommon** ({joint_frac*100:.2f}%) but not extreme.\n")
    else:
        w(f"The triple conjunction is **not rare** ({joint_frac*100:.2f}%) — "
          f"the three metrics are not jointly discriminating.\n")

    # ── Correlations ──
    w("### Pairwise Correlations (Notable Metrics)\n")
    w("| Metric A | Metric B | Pearson r |")
    w("|----------|----------|-----------|")
    for (a, b), r in sorted(correlations.items()):
        w(f"| {a} | {b} | {r:+.3f} |")
    w("")

    any_strong = any(abs(r) > 0.3 for r in correlations.values())
    if any_strong:
        w("Some notable metrics are **correlated** in the null — "
          "the joint test partly captures redundant information.\n")
    else:
        w("Notable metrics are **approximately independent** in the null — "
          "the joint test captures genuinely multi-dimensional information.\n")

    return "\n".join(lines)

# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("KW SEQUENCE ORDERING — JOINT ANALYSIS")
    print("=" * 70)

    print("\n1. Loading null distributions...")
    metric_names, kw_vals, null_arrays = load_null_data()
    n_samples = len(next(iter(null_arrays.values())))
    print(f"   {len(metric_names)} metrics, {n_samples:,} samples")

    print("\n2. Computing omnibus statistic...")
    kw_omnibus, null_omnibus, omnibus_pct, kw_zscores = compute_omnibus(
        metric_names, kw_vals, null_arrays)
    print(f"   KW Σz² = {kw_omnibus:.2f}")
    print(f"   Null: mean={np.mean(null_omnibus):.2f}, std={np.std(null_omnibus):.2f}")
    print(f"   KW percentile: {omnibus_pct:.1f}%")

    print("\n3. Computing triple joint test...")
    triple_metrics, joint_count, joint_frac = compute_triple_joint(kw_vals, null_arrays)
    print(f"   Joint count: {joint_count:,} / {n_samples:,} = {joint_frac*100:.2f}%")

    print("\n4. Computing pairwise correlations...")
    corr_metrics, correlations = compute_correlations(null_arrays)
    for (a, b), r in correlations.items():
        a_short = a.split("_", 1)[1][:15]
        b_short = b.split("_", 1)[1][:15]
        print(f"   {a_short} × {b_short}: r={r:+.3f}")

    print("\n5. Appending to results file...")
    md = format_results(kw_omnibus, null_omnibus, omnibus_pct, kw_zscores,
                        triple_metrics, joint_count, joint_frac,
                        corr_metrics, correlations, metric_names)

    results_path = SCRIPT_DIR / "01_ordering_results.md"
    with open(results_path, "a") as f:
        f.write(md)
    print(f"   Appended to {results_path}")

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)


if __name__ == "__main__":
    main()
