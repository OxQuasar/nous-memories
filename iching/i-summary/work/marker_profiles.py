#!/usr/bin/env python3
"""
marker_profiles.py — Core/shell coupling profiles for all markers

For each marker with ≥8 occurrences, fits logistic regressions:
  Model 0: position only (baseline)
  Model A: position + basin (core)
  Model B: position + shell (surface_relation + rank + palace_element)
  Model C: position + basin + shell (full)

Classifies each marker as Core-only / Shell-only / Dual / None.
Tests: are negative markers more core-coupled than positive markers?
"""

import json
import warnings
import numpy as np
from pathlib import Path
from collections import Counter
from scipy import stats as sp_stats

import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Logit

warnings.filterwarnings("ignore", category=RuntimeWarning)

HERE = Path(__file__).resolve().parent
ICHING = HERE.parent
ATLAS_PATH = ICHING / "atlas" / "atlas.json"
MARKERS_PATH = ICHING / "semantic-map" / "data" / "stock_phrases.json"
OUT_PATH = HERE / "marker_profiles_results.json"

# Marker classification
POSITIVE_MARKERS = {"吉", "利", "亨", "无咎"}
NEGATIVE_MARKERS = {"凶", "咎", "厲", "悔", "吝"}
NEUTRAL_MARKERS  = {"悔亡", "貞"}

MIN_COUNT = 8    # minimum occurrences to include
SPARSE_THRESHOLD = 15  # below this, use reduced shell model

# ─── Data loading ──────────────────────────────────────────────────

def load_records():
    with open(ATLAS_PATH) as f:
        atlas = json.load(f)
    with open(MARKERS_PATH) as f:
        sp = json.load(f)

    marker_index = {}
    for entry in sp["marker_matrix"]:
        marker_index[(entry["hex_val"], entry["line"])] = entry["markers"]

    all_markers = Counter()
    records = []
    for h in range(64):
        a = atlas[str(h)]
        for line in range(6):
            raw_markers = marker_index.get((h, line), [])
            for m in raw_markers:
                all_markers[m] += 1
            records.append({
                "line_position": line,
                "raw_markers": raw_markers,
                "basin": a["basin"],
                "surface_relation": a["surface_relation"],
                "rank": a["rank"],
                "palace_element": a["palace_element"],
            })
    return records, all_markers


def make_dummies(records, col, ref=None):
    levels = sorted(set(r[col] for r in records), key=str)
    if ref is None:
        ref = levels[0]
    levels = [lv for lv in levels if lv != ref]
    out = np.zeros((len(records), len(levels)))
    for i, r in enumerate(records):
        for j, lv in enumerate(levels):
            if r[col] == lv:
                out[i, j] = 1
    return out, [f"{col}={lv}" for lv in levels]


# ─── Model fitting ─────────────────────────────────────────────────

def fit_logit_safe(X, y, label=""):
    """Fit logistic regression; return dict with ll, r2, k, or error."""
    try:
        model = Logit(y, X)
        result = model.fit(disp=0, maxiter=100, method='newton')
        return {
            "ll": result.llf,
            "ll_null": result.llnull,
            "r2": 1.0 - result.llf / result.llnull,
            "aic": result.aic,
            "k": X.shape[1],
            "converged": result.mle_retvals.get('converged', True),
            "params": dict(zip(range(X.shape[1]), result.params.tolist())),
            "pvalues": dict(zip(range(X.shape[1]), result.pvalues.tolist())),
        }
    except Exception as e:
        return {"error": str(e), "ll": None, "r2": None, "k": X.shape[1]}


def lr_test(ll_restricted, ll_full, df_diff):
    if ll_restricted is None or ll_full is None:
        return None, None
    lr_stat = -2 * (ll_restricted - ll_full)
    if lr_stat < 0:
        lr_stat = 0.0
    p = 1 - sp_stats.chi2.cdf(lr_stat, df_diff)
    return lr_stat, p


# ─── Main analysis ─────────────────────────────────────────────────

def main():
    records, all_markers = load_records()
    n = len(records)
    print(f"Records: {n}")
    print()

    # Build design matrices (shared across markers)
    X_pos, pos_names = make_dummies(records, "line_position", ref=0)
    X_basin, basin_names = make_dummies(records, "basin", ref="Cycle")
    X_sr, sr_names = make_dummies(records, "surface_relation", ref="比和")
    X_rank, rank_names = make_dummies(records, "rank", ref=0)
    X_pe, pe_names = make_dummies(records, "palace_element", ref="Earth")

    X_M0 = sm.add_constant(X_pos)
    X_MA = sm.add_constant(np.hstack([X_pos, X_basin]))
    # Full shell model
    X_MB_full = sm.add_constant(np.hstack([X_pos, X_sr, X_rank, X_pe]))
    X_MC_full = sm.add_constant(np.hstack([X_pos, X_basin, X_sr, X_rank, X_pe]))
    # Reduced shell model (surface_relation only — for sparse markers)
    X_MB_reduced = sm.add_constant(np.hstack([X_pos, X_sr]))
    X_MC_reduced = sm.add_constant(np.hstack([X_pos, X_basin, X_sr]))

    # Select markers to analyze
    active_markers = [(m, c) for m, c in all_markers.most_common() if c >= MIN_COUNT]
    print(f"Markers to analyze (≥{MIN_COUNT} occurrences): {len(active_markers)}")
    for m, c in active_markers:
        valence = "positive" if m in POSITIVE_MARKERS else "negative" if m in NEGATIVE_MARKERS else "neutral"
        sparse = " [sparse — reduced shell]" if c < SPARSE_THRESHOLD else ""
        print(f"  {m:>4}: {c:>3} ({valence}){sparse}")
    print()

    # ── Fit all models for each marker ──
    results = []

    for marker, count in active_markers:
        y = np.array([int(marker in r["raw_markers"]) for r in records])
        prevalence = y.mean()

        # Choose shell model complexity based on marker count
        if count >= SPARSE_THRESHOLD:
            X_MB = X_MB_full
            X_MC = X_MC_full
            shell_model = "full"
        else:
            X_MB = X_MB_reduced
            X_MC = X_MC_reduced
            shell_model = "reduced"

        r0 = fit_logit_safe(X_M0, y, "M0")
        rA = fit_logit_safe(X_MA, y, "MA")
        rB = fit_logit_safe(X_MB, y, "MB")
        rC = fit_logit_safe(X_MC, y, "MC")

        r2_pos = r0["r2"] if r0["r2"] is not None else 0
        r2_A = rA["r2"] if rA["r2"] is not None else 0
        r2_B = rB["r2"] if rB["r2"] is not None else 0
        r2_C = rC["r2"] if rC["r2"] is not None else 0

        # Guard against degenerate fits (negative pseudo-R² or error)
        if r0.get("error") or rA.get("error"):
            dr2_core = 0
        else:
            dr2_core = max(r2_A - r2_pos, 0)  # can't be negative in well-fit model

        if r0.get("error") or rB.get("error"):
            dr2_shell = 0
        else:
            dr2_shell = max(r2_B - r2_pos, 0)

        if r0.get("error") or rC.get("error"):
            dr2_total = 0
        else:
            dr2_total = max(r2_C - r2_pos, 0)

        # Independence: if additive, dr2_core + dr2_shell ≈ dr2_total
        additivity = (dr2_core + dr2_shell) - dr2_total if dr2_total > 0 else 0

        # LR tests — compute df from actual matrices used
        df_core_m = X_MA.shape[1] - X_M0.shape[1]
        df_shell_m = X_MB.shape[1] - X_M0.shape[1]
        df_cgs_m = X_MC.shape[1] - X_MB.shape[1]
        df_sgc_m = X_MC.shape[1] - X_MA.shape[1]

        _, p_core = lr_test(r0["ll"], rA["ll"], df_core_m)
        _, p_shell = lr_test(r0["ll"], rB["ll"], df_shell_m)
        _, p_core_given_shell = lr_test(rB["ll"], rC["ll"], df_cgs_m)
        _, p_shell_given_core = lr_test(rA["ll"], rC["ll"], df_sgc_m)

        # Classification
        sig_core = p_core is not None and p_core < 0.05
        sig_shell = p_shell is not None and p_shell < 0.05
        if sig_core and sig_shell:
            mtype = "Dual"
        elif sig_core:
            mtype = "Core-only"
        elif sig_shell:
            mtype = "Shell-only"
        else:
            mtype = "None"

        valence = "positive" if marker in POSITIVE_MARKERS else \
                  "negative" if marker in NEGATIVE_MARKERS else "neutral"

        entry = {
            "marker": marker,
            "count": count,
            "prevalence": prevalence,
            "valence": valence,
            "shell_model": shell_model,
            "r2_position": r2_pos,
            "r2_core": r2_A,
            "r2_shell": r2_B,
            "r2_full": r2_C,
            "dr2_core": dr2_core,
            "dr2_shell": dr2_shell,
            "dr2_total": dr2_total,
            "additivity_excess": additivity,
            "p_core": p_core,
            "p_shell": p_shell,
            "p_core_given_shell": p_core_given_shell,
            "p_shell_given_core": p_shell_given_core,
            "type": mtype,
            "ll_M0": r0["ll"],
            "ll_MA": rA["ll"],
            "ll_MB": rB["ll"],
            "ll_MC": rC["ll"],
        }
        results.append(entry)

    # ═══════════════════════════════════════════════════════════════
    # Print summary table
    # ═══════════════════════════════════════════════════════════════

    print("=" * 110)
    print("  MARKER COUPLING PROFILES")
    print("=" * 110)
    print()

    hdr = (f"  {'Marker':>6} {'N':>4} {'Val':>8} {'ΔR²core':>8} {'ΔR²shell':>9} "
           f"{'ΔR²total':>9} {'Excess':>7} {'Core p':>10} {'Shell p':>10} "
           f"{'C|S p':>10} {'S|C p':>10} {'Type':>10}")
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))

    for r in results:
        core_flag = "*" if r["p_core"] is not None and r["p_core"] < 0.05 else " "
        shell_flag = "*" if r["p_shell"] is not None and r["p_shell"] < 0.05 else " "

        def fmt_p(p):
            return f"{p:.2e}" if p is not None else "   N/A   "

        print(f"  {r['marker']:>6} {r['count']:>4} {r['valence']:>8} "
              f"{r['dr2_core']:>+8.4f} {r['dr2_shell']:>+9.4f} "
              f"{r['dr2_total']:>+9.4f} {r['additivity_excess']:>+7.4f} "
              f"{fmt_p(r['p_core']):>10}{core_flag}"
              f"{fmt_p(r['p_shell']):>10}{shell_flag}"
              f"{fmt_p(r['p_core_given_shell']):>10} "
              f"{fmt_p(r['p_shell_given_core']):>10} "
              f"{r['type']:>10}")

    print()
    print("  * = significant at p < 0.05")
    print("  Excess = (ΔR²_core + ΔR²_shell) − ΔR²_total  (>0 means overlap)")
    print("  C|S = core given shell; S|C = shell given core")
    print()

    # ═══════════════════════════════════════════════════════════════
    # Type summary
    # ═══════════════════════════════════════════════════════════════

    type_counts = Counter(r["type"] for r in results)
    print("  Type distribution:")
    for t in ["Core-only", "Shell-only", "Dual", "None"]:
        markers_of_type = [r["marker"] for r in results if r["type"] == t]
        print(f"    {t:<12}: {type_counts.get(t, 0)}  {markers_of_type}")
    print()

    # ═══════════════════════════════════════════════════════════════
    # Valence × coupling hypothesis test
    # ═══════════════════════════════════════════════════════════════

    print("=" * 80)
    print("  HYPOTHESIS: Negative markers are more core-coupled than positive markers")
    print("=" * 80)
    print()

    pos_entries = [r for r in results if r["valence"] == "positive"]
    neg_entries = [r for r in results if r["valence"] == "negative"]

    if pos_entries and neg_entries:
        pos_core = [r["dr2_core"] for r in pos_entries]
        neg_core = [r["dr2_core"] for r in neg_entries]
        pos_shell = [r["dr2_shell"] for r in pos_entries]
        neg_shell = [r["dr2_shell"] for r in neg_entries]

        mean_pos_core = np.mean(pos_core)
        mean_neg_core = np.mean(neg_core)
        mean_pos_shell = np.mean(pos_shell)
        mean_neg_shell = np.mean(neg_shell)

        observed_diff = mean_neg_core - mean_pos_core

        print(f"  Positive markers ({len(pos_entries)}): "
              f"{', '.join(r['marker'] for r in pos_entries)}")
        print(f"    Mean ΔR²_core  = {mean_pos_core:.4f}")
        print(f"    Mean ΔR²_shell = {mean_pos_shell:.4f}")
        print()
        print(f"  Negative markers ({len(neg_entries)}): "
              f"{', '.join(r['marker'] for r in neg_entries)}")
        print(f"    Mean ΔR²_core  = {mean_neg_core:.4f}")
        print(f"    Mean ΔR²_shell = {mean_neg_shell:.4f}")
        print()
        print(f"  Observed difference (neg − pos) in ΔR²_core: {observed_diff:+.4f}")
        print()

        # Permutation test
        combined = pos_entries + neg_entries
        all_dr2_core = [r["dr2_core"] for r in combined]
        n_pos = len(pos_entries)
        n_neg = len(neg_entries)
        n_perm = 10000
        rng = np.random.default_rng(42)

        perm_diffs = np.zeros(n_perm)
        for i in range(n_perm):
            idx = rng.permutation(len(all_dr2_core))
            perm_neg = [all_dr2_core[j] for j in idx[:n_neg]]
            perm_pos = [all_dr2_core[j] for j in idx[n_neg:]]
            perm_diffs[i] = np.mean(perm_neg) - np.mean(perm_pos)

        p_perm = np.mean(perm_diffs >= observed_diff)
        print(f"  Permutation test (10000 shuffles, one-sided):")
        print(f"    p = {p_perm:.4f}")
        if p_perm < 0.05:
            print(f"    → SIGNIFICANT: negative markers have higher core coupling")
        else:
            print(f"    → NOT significant at p < 0.05")

        # Also test shell difference
        observed_shell_diff = mean_neg_shell - mean_pos_shell
        all_dr2_shell = [r["dr2_shell"] for r in combined]
        perm_shell_diffs = np.zeros(n_perm)
        for i in range(n_perm):
            idx = rng.permutation(len(all_dr2_shell))
            perm_neg_s = [all_dr2_shell[j] for j in idx[:n_neg]]
            perm_pos_s = [all_dr2_shell[j] for j in idx[n_neg:]]
            perm_shell_diffs[i] = np.mean(perm_neg_s) - np.mean(perm_pos_s)

        p_shell_perm = np.mean(perm_shell_diffs >= observed_shell_diff)
        print()
        print(f"  Shell coupling difference (neg − pos): {observed_shell_diff:+.4f}")
        print(f"    Permutation p = {p_shell_perm:.4f}")
    else:
        print("  Insufficient data for hypothesis test")

    print()

    # ═══════════════════════════════════════════════════════════════
    # 2D scatter data
    # ═══════════════════════════════════════════════════════════════

    print("=" * 60)
    print("  2D COUPLING LANDSCAPE (ΔR²_core, ΔR²_shell)")
    print("=" * 60)
    print()
    print(f"  {'Marker':>6} {'Core':>8} {'Shell':>8} {'Valence':>8} {'Type':>10}")
    print("  " + "-" * 44)
    for r in sorted(results, key=lambda x: -x["dr2_core"]):
        print(f"  {r['marker']:>6} {r['dr2_core']:>+8.4f} {r['dr2_shell']:>+8.4f} "
              f"{r['valence']:>8} {r['type']:>10}")

    print()

    # Visual ascii scatter (crude but informative)
    print("  Coupling landscape (ASCII):")
    print("  ΔR²_shell ↑")
    max_core = max(r["dr2_core"] for r in results) * 1.2 + 0.001
    max_shell = max(r["dr2_shell"] for r in results) * 1.2 + 0.001
    grid_w, grid_h = 50, 20
    grid = [[' '] * grid_w for _ in range(grid_h)]

    for r in results:
        x = int(r["dr2_core"] / max_core * (grid_w - 1))
        y = int(r["dr2_shell"] / max_shell * (grid_h - 1))
        x = max(0, min(grid_w - 1, x))
        y = max(0, min(grid_h - 1, y))
        char = r["marker"][0] if len(r["marker"]) == 1 else r["marker"][:1]
        # Use N/P/U for negative/positive/neutral
        char = "−" if r["valence"] == "negative" else "+" if r["valence"] == "positive" else "○"
        grid[grid_h - 1 - y][x] = char

    for row in grid:
        print("  |" + "".join(row) + "|")
    print("  " + "+" + "-" * grid_w + "+→ ΔR²_core")
    print("  (+ = positive marker, − = negative, ○ = neutral)")
    print()

    # Labeled version
    print("  Labeled positions:")
    for r in results:
        x = r["dr2_core"] / max_core * 100
        y = r["dr2_shell"] / max_shell * 100
        print(f"    {r['marker']:>4} at ({x:>5.1f}%, {y:>5.1f}%) [{r['valence']}]")

    # ═══════════════════════════════════════════════════════════════
    # Cross-projection detail: for Dual markers, does core add to shell?
    # ═══════════════════════════════════════════════════════════════

    print()
    print("=" * 60)
    print("  CROSS-PROJECTION INDEPENDENCE FOR KEY MARKERS")
    print("=" * 60)
    print()

    for r in results:
        if r["type"] in ("Dual", "Core-only"):
            print(f"  {r['marker']} ({r['type']}, N={r['count']}):")
            print(f"    ΔR²_core = {r['dr2_core']:+.4f}, p = {r['p_core']:.2e}")
            print(f"    ΔR²_shell = {r['dr2_shell']:+.4f}, p = {r['p_shell']:.2e}" if r['p_shell'] else "")
            if r['p_core_given_shell'] is not None:
                cs = "✓" if r['p_core_given_shell'] < 0.05 else "✗"
                print(f"    Core given shell: p = {r['p_core_given_shell']:.2e} {cs}")
            if r['p_shell_given_core'] is not None:
                sc = "✓" if r['p_shell_given_core'] < 0.05 else "✗"
                print(f"    Shell given core: p = {r['p_shell_given_core']:.2e} {sc}")
            over = r['additivity_excess']
            if abs(over) > 0.001:
                print(f"    Overlap: {over:+.4f} "
                      f"({'correlated' if over > 0 else 'synergistic'})")
            print()

    # ═══════════════════════════════════════════════════════════════
    # Save
    # ═══════════════════════════════════════════════════════════════

    out = {
        "marker_profiles": [],
        "hypothesis_test": {},
    }

    for r in results:
        entry = dict(r)
        # Ensure JSON-safe
        for k, v in entry.items():
            if isinstance(v, (np.floating, np.integer)):
                entry[k] = float(v)
            elif isinstance(v, np.bool_):
                entry[k] = bool(v)
        out["marker_profiles"].append(entry)

    if pos_entries and neg_entries:
        out["hypothesis_test"] = {
            "positive_markers": [r["marker"] for r in pos_entries],
            "negative_markers": [r["marker"] for r in neg_entries],
            "mean_pos_dr2_core": float(mean_pos_core),
            "mean_neg_dr2_core": float(mean_neg_core),
            "mean_pos_dr2_shell": float(mean_pos_shell),
            "mean_neg_dr2_shell": float(mean_neg_shell),
            "observed_diff_core": float(observed_diff),
            "perm_p_core": float(p_perm),
            "observed_diff_shell": float(observed_shell_diff),
            "perm_p_shell": float(p_shell_perm),
        }

    with open(OUT_PATH, 'w') as f:
        json.dump(out, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nResults saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
