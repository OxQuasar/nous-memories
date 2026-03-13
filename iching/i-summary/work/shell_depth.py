#!/usr/bin/env python3
"""
shell_depth.py — How much text variance does the shell projection explain?

Fits logistic regressions predicting 吉 and 凶 (binary) from algebraic
coordinates, comparing core vs shell projection explanatory power.

Models:
  0: position only (baseline)
  1: position + basin (core)
  2: position + surface_relation (single shell)
  3: position + rank (single shell)
  4: position + surface_relation + rank + palace_element (combined shell)
  5: position + basin + surface_relation + rank + palace_element (full)

Reports McFadden pseudo-R² and AIC. Tests rank × surface_relation interaction.
"""

import json
import numpy as np
from pathlib import Path
from scipy import stats as sp_stats

import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Logit

HERE = Path(__file__).resolve().parent
ICHING = HERE.parent
ATLAS_PATH = ICHING / "atlas" / "atlas.json"
MARKERS_PATH = ICHING / "semantic-map" / "data" / "stock_phrases.json"
OUT_PATH = HERE / "shell_depth_results.json"

# ─── Load & build ──────────────────────────────────────────────────

def load_records():
    with open(ATLAS_PATH) as f:
        atlas = json.load(f)
    with open(MARKERS_PATH) as f:
        sp = json.load(f)

    marker_index = {}
    for entry in sp["marker_matrix"]:
        marker_index[(entry["hex_val"], entry["line"])] = entry["markers"]

    records = []
    for h in range(64):
        a = atlas[str(h)]
        for line in range(6):
            markers = marker_index.get((h, line), [])
            records.append({
                "line_position": line,
                "ji": int("吉" in markers),
                "xiong": int("凶" in markers),
                # Core
                "basin": a["basin"],
                # Shell
                "surface_relation": a["surface_relation"],
                "rank": a["rank"],
                "palace_element": a["palace_element"],
                "shi": a["shi"],
            })
    return records


def make_dummies(records, col, ref=None):
    """Create dummy columns for a categorical variable. Drop one level (ref)."""
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


def build_design_matrices(records):
    """Build all feature matrices needed for the 6 models."""
    n = len(records)

    # Position dummies (ref = line 0)
    X_pos, pos_names = make_dummies(records, "line_position", ref=0)

    # Basin dummies (ref = Cycle, the largest group)
    X_basin, basin_names = make_dummies(records, "basin", ref="Cycle")

    # Surface relation dummies (ref = 比和)
    X_sr, sr_names = make_dummies(records, "surface_relation", ref="比和")

    # Rank dummies (ref = 0)
    X_rank, rank_names = make_dummies(records, "rank", ref=0)

    # Palace element dummies (ref = Earth)
    X_pe, pe_names = make_dummies(records, "palace_element", ref="Earth")

    # Shi: is this the shi line? (binary)
    X_shi = np.array([int(r["line_position"] + 1 == r["shi"]) for r in records]).reshape(-1, 1)
    shi_names = ["is_shi"]

    # Targets
    y_ji = np.array([r["ji"] for r in records])
    y_xiong = np.array([r["xiong"] for r in records])

    # Assemble models
    models = {}

    # Model 0: position only
    X0 = sm.add_constant(X_pos)
    models["M0_position"] = (X0, ["const"] + pos_names)

    # Model 1: position + basin
    X1 = sm.add_constant(np.hstack([X_pos, X_basin]))
    models["M1_pos_basin"] = (X1, ["const"] + pos_names + basin_names)

    # Model 2: position + surface_relation
    X2 = sm.add_constant(np.hstack([X_pos, X_sr]))
    models["M2_pos_sr"] = (X2, ["const"] + pos_names + sr_names)

    # Model 3: position + rank
    X3 = sm.add_constant(np.hstack([X_pos, X_rank]))
    models["M3_pos_rank"] = (X3, ["const"] + pos_names + rank_names)

    # Model 4: position + surface_relation + rank + palace_element (combined shell)
    X4 = sm.add_constant(np.hstack([X_pos, X_sr, X_rank, X_pe]))
    models["M4_pos_shell"] = (X4, ["const"] + pos_names + sr_names + rank_names + pe_names)

    # Model 5: position + basin + surface_relation + rank + palace_element (full)
    X5 = sm.add_constant(np.hstack([X_pos, X_basin, X_sr, X_rank, X_pe]))
    models["M5_full"] = (X5, ["const"] + pos_names + basin_names + sr_names + rank_names + pe_names)

    # Model 4i: Model 4 + rank × surface_relation interaction
    # Create interaction: rank_dummy_j × sr_dummy_k for each (j,k)
    interactions = []
    int_names = []
    for j, rn in enumerate(rank_names):
        for k, sn in enumerate(sr_names):
            interactions.append(X_rank[:, j] * X_sr[:, k])
            int_names.append(f"{rn}×{sn}")
    X_int = np.column_stack(interactions) if interactions else np.zeros((n, 0))
    X4i = sm.add_constant(np.hstack([X_pos, X_sr, X_rank, X_pe, X_int]))
    models["M4i_shell_interaction"] = (X4i, ["const"] + pos_names + sr_names + rank_names + pe_names + int_names)

    return models, y_ji, y_xiong


# ─── Fit & report ──────────────────────────────────────────────────

def fit_logit(X, y, names, label=""):
    """Fit logistic regression, return summary dict."""
    try:
        model = Logit(y, X)
        result = model.fit(disp=0, maxiter=100, method='newton')
        ll = result.llf
        ll_null = result.llnull
        mcfadden_r2 = 1.0 - ll / ll_null
        aic = result.aic
        bic = result.bic
        nobs = result.nobs
        k = X.shape[1]
        converged = result.mle_retvals.get('converged', True)

        return {
            "label": label,
            "nobs": int(nobs),
            "k": k,
            "ll": ll,
            "ll_null": ll_null,
            "mcfadden_r2": mcfadden_r2,
            "aic": aic,
            "bic": bic,
            "converged": converged,
            "params": {n: float(p) for n, p in zip(names, result.params)},
            "pvalues": {n: float(p) for n, p in zip(names, result.pvalues)},
        }
    except Exception as e:
        return {"label": label, "error": str(e)}


def lr_test(ll_restricted, ll_full, df_diff):
    """Likelihood ratio test."""
    lr_stat = -2 * (ll_restricted - ll_full)
    p = 1 - sp_stats.chi2.cdf(lr_stat, df_diff)
    return lr_stat, p


def main():
    records = load_records()
    models, y_ji, y_xiong = build_design_matrices(records)
    print(f"Records: {len(records)}")
    print()

    all_results = {}

    for target_name, y in [("吉", y_ji), ("凶", y_xiong)]:
        print("=" * 72)
        print(f"  TARGET: {target_name} (prevalence: {y.sum()}/{len(y)} = {y.mean()*100:.1f}%)")
        print("=" * 72)
        print()

        results = {}
        for model_name in ["M0_position", "M1_pos_basin", "M2_pos_sr",
                           "M3_pos_rank", "M4_pos_shell", "M5_full",
                           "M4i_shell_interaction"]:
            X, names = models[model_name]
            r = fit_logit(X, y, names, label=model_name)
            results[model_name] = r

        # Summary table
        print(f"  {'Model':<25} {'k':>3} {'LL':>10} {'McF R²':>8} {'AIC':>10} {'BIC':>10}")
        print("  " + "-" * 72)
        for mn in ["M0_position", "M1_pos_basin", "M2_pos_sr",
                    "M3_pos_rank", "M4_pos_shell", "M5_full",
                    "M4i_shell_interaction"]:
            r = results[mn]
            if "error" in r:
                print(f"  {mn:<25} ERROR: {r['error']}")
                continue
            print(f"  {mn:<25} {r['k']:>3} {r['ll']:>10.2f} "
                  f"{r['mcfadden_r2']:>8.4f} {r['aic']:>10.2f} {r['bic']:>10.2f}")

        print()

        # Key comparisons via LR tests
        print(f"  Likelihood ratio tests (nested models):")
        comparisons = [
            ("M0→M1 (add basin)", "M0_position", "M1_pos_basin"),
            ("M0→M2 (add surface_rel)", "M0_position", "M2_pos_sr"),
            ("M0→M3 (add rank)", "M0_position", "M3_pos_rank"),
            ("M0→M4 (add all shell)", "M0_position", "M4_pos_shell"),
            ("M0→M5 (add all)", "M0_position", "M5_full"),
            ("M1→M5 (shell|basin)", "M1_pos_basin", "M5_full"),
            ("M4→M5 (basin|shell)", "M4_pos_shell", "M5_full"),
            ("M4→M4i (interaction)", "M4_pos_shell", "M4i_shell_interaction"),
        ]
        for label, m_r, m_f in comparisons:
            r_r = results[m_r]
            r_f = results[m_f]
            if "error" in r_r or "error" in r_f:
                print(f"    {label:<30} SKIPPED (model error)")
                continue
            df = r_f["k"] - r_r["k"]
            lr_stat, p = lr_test(r_r["ll"], r_f["ll"], df)
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            print(f"    {label:<30} LR={lr_stat:>8.3f}, df={df:>2}, p={p:.2e} {sig}")

        print()

        # Incremental R² contributions
        print(f"  Incremental McFadden R² (relative to position-only baseline):")
        r0 = results["M0_position"]
        if "error" not in r0:
            for mn, desc in [
                ("M1_pos_basin", "basin alone"),
                ("M2_pos_sr", "surface_rel alone"),
                ("M3_pos_rank", "rank alone"),
                ("M4_pos_shell", "combined shell"),
                ("M5_full", "full (basin + shell)"),
            ]:
                r = results[mn]
                if "error" not in r:
                    delta = r["mcfadden_r2"] - r0["mcfadden_r2"]
                    print(f"    {desc:<25} ΔR² = {delta:>+.4f}  (total R² = {r['mcfadden_r2']:.4f})")

        print()

        # Show significant coefficients from Model 5 (full)
        r5 = results["M5_full"]
        if "error" not in r5:
            print(f"  Significant coefficients in full model (p < 0.05):")
            sig_params = [(n, r5["params"][n], r5["pvalues"][n])
                          for n in r5["params"]
                          if r5["pvalues"][n] < 0.05 and n != "const"]
            sig_params.sort(key=lambda x: x[2])
            for name, coef, pv in sig_params:
                or_val = np.exp(coef)
                print(f"    {name:<30} β={coef:>+7.3f}  OR={or_val:>6.3f}  p={pv:.4f}")
            if not sig_params:
                print(f"    (none)")

        print()
        all_results[target_name] = results

    # Save
    # Clean for JSON
    clean = {}
    for tgt, models_r in all_results.items():
        clean[tgt] = {}
        for mn, r in models_r.items():
            cr = {}
            for k, v in r.items():
                if isinstance(v, (np.floating, np.integer)):
                    cr[k] = float(v)
                elif isinstance(v, dict):
                    cr[k] = {kk: float(vv) if isinstance(vv, (np.floating, np.integer)) else vv
                             for kk, vv in v.items()}
                else:
                    cr[k] = v
            clean[tgt][mn] = cr

    with open(OUT_PATH, 'w') as f:
        json.dump(clean, f, indent=2, ensure_ascii=False, default=str)
    print(f"Results saved to {OUT_PATH}")


if __name__ == "__main__":
    main()
