#!/usr/bin/env python3
"""Probe M5: Topology detection in empirical data.

Maps financial returns to 先天 trigram positions via quantile discretization,
then tests whether temporal structure produces Q₃-detectable patterns:
- Hamming distance distribution (Q₃ edge preference)
- 五行 type distribution
- GMS grammar (consecutive 克 suppression)
- Valve (克→生 suppression)
- Bit-layer decomposition of Hamming-1 transitions
"""

import numpy as np
from collections import Counter, defaultdict
import warnings
warnings.filterwarnings('ignore')

# ─── Definitions (from m3) ───────────────────────────────────────────────

XIANTIAN = [
    (1, "乾", (1,1,1)), (2, "兌", (0,1,1)), (3, "離", (1,0,1)), (4, "震", (0,0,1)),
    (5, "巽", (1,1,0)), (6, "坎", (0,1,0)), (7, "艮", (1,0,0)), (8, "坤", (0,0,0)),
]

VEC = {pos: v for pos, _, v in XIANTIAN}
NAME_BY_POS = {pos: name for pos, name, _ in XIANTIAN}

WUXING_MAP = {
    (1,1,1): 0, (0,1,1): 0, (0,1,0): 1,
    (0,0,1): 2, (1,1,0): 2, (1,0,1): 3,
    (0,0,0): 4, (1,0,0): 4,
}
Z5_NAMES = {0: "Metal", 1: "Water", 2: "Wood", 3: "Fire", 4: "Earth"}

def wuxing_type(a, b):
    d = abs(a - b); d = min(d, 5 - d)
    return {0: "比和", 1: "生", 2: "克"}[d]

def hamming(a, b):
    return sum(x != y for x, y in zip(a, b))

# Null expectations (from M3: independent uniform ordered pairs on 8 trigrams)
NULL_WX = {"比和": 21.88, "生": 37.50, "克": 40.62}
# Hamming null: uniform pairs from Q₃ → P(d) = {0:1/8, 1:3/8, 2:3/8, 3:1/8}
NULL_HAM = {0: 12.5, 1: 37.5, 2: 37.5, 3: 12.5}

# Q₃ grammar prediction for bit-layer 五行 types (from M1):
#   bit₀: {0 比和, 2 生, 2 克} → 50% 克
#   bit₁: {0, 0, 4 克}        → 100% 克
#   bit₂: {2 比和, 2 生, 0 克} → 0% 克
GRAMMAR_KE = {0: 50.0, 1: 100.0, 2: 0.0}

# ─── Discretization ─────────────────────────────────────────────────────

def discretize(returns, n_bins=8):
    """Map returns to bins 0..7 via empirical quantiles (octiles)."""
    boundaries = np.quantile(returns, np.linspace(0, 1, n_bins + 1)[1:-1])
    return np.digitize(returns, boundaries)  # 0..7

def bin_to_vec(k):
    """bin k → 先天 position (k+1) → F₂³ vector."""
    return VEC[k + 1]

# ─── Core analysis ──────────────────────────────────────────────────────

def analyze(bins):
    """Full transition analysis. Returns dict of all metrics."""
    N = len(bins)
    n_trans = N - 1

    ham_counts = Counter()
    wx_counts = Counter()
    bit_layer_counts = Counter()
    bit_layer_wx = defaultdict(Counter)
    types = []

    for i in range(n_trans):
        v1, v2 = bin_to_vec(bins[i]), bin_to_vec(bins[i + 1])
        hd = hamming(v1, v2)
        ham_counts[hd] += 1

        w1, w2 = WUXING_MAP[v1], WUXING_MAP[v2]
        wt = wuxing_type(w1, w2)
        wx_counts[wt] += 1
        types.append(wt)

        if hd == 1:
            for bit in range(3):
                if v1[2 - bit] != v2[2 - bit]:
                    bit_layer_counts[bit] += 1
                    bit_layer_wx[bit][wt] += 1

    # Consecutive type pairs
    type_pairs = Counter()
    consec_ke = 0
    for i in range(len(types) - 1):
        type_pairs[(types[i], types[i + 1])] += 1
        if types[i] == "克" and types[i + 1] == "克":
            consec_ke += 1

    ke_out = sum(type_pairs.get(("克", t), 0) for t in ["比和", "生", "克"])

    return dict(
        n_trans=n_trans, ham_counts=ham_counts, wx_counts=wx_counts,
        bit_layer_counts=bit_layer_counts, bit_layer_wx=bit_layer_wx,
        types=types, type_pairs=type_pairs, consec_ke=consec_ke,
        ke_sheng=type_pairs.get(("克", "生"), 0), ke_out=ke_out,
    )

def print_analysis(r, label, show_bitlayer=True):
    """Print formatted results for one analysis."""
    n = r['n_trans']

    # Hamming distance
    print(f"\n  Hamming distance distribution:")
    print(f"  {'d':>3} {'Count':>7} {'Actual':>7} {'Null':>6} {'Δ':>7}")
    print(f"  " + "─" * 34)
    for d in range(4):
        c = r['ham_counts'].get(d, 0)
        a = c / n * 100
        nl = NULL_HAM[d]
        print(f"  {d:>3} {c:>7} {a:>6.1f}% {nl:>5.1f}% {a - nl:>+6.1f}%")

    # 五行 types
    print(f"\n  五行 type distribution:")
    print(f"  {'Type':>5} {'Count':>7} {'Actual':>7} {'Null':>6} {'Δ':>7}")
    print(f"  " + "─" * 36)
    for t in ["比和", "生", "克"]:
        c = r['wx_counts'].get(t, 0)
        a = c / n * 100
        nl = NULL_WX[t]
        print(f"  {t:>5} {c:>7} {a:>6.1f}% {nl:>5.1f}% {a - nl:>+6.1f}%")

    # GMS
    p_ke = r['wx_counts'].get("克", 0) / n
    exp_kk = (n - 1) * p_ke ** 2
    ratio = r['consec_ke'] / exp_kk if exp_kk > 0 else 0
    print(f"\n  GMS: consecutive 克 = {r['consec_ke']} (expected {exp_kk:.1f}, ratio {ratio:.2f}x)")
    print(f"  Valve: 克→生 = {r['ke_sheng']}/{r['ke_out']}"
          + (f" ({r['ke_sheng']/r['ke_out']*100:.1f}%)" if r['ke_out'] > 0 else ""))

    # Bit-layer
    if show_bitlayer:
        h1 = r['ham_counts'].get(1, 0)
        if h1 > 0:
            print(f"\n  Bit-layer decomposition (Hamming-1 only, N={h1}):")
            print(f"  {'Layer':>6} {'N':>5} {'%':>6} │ {'克':>4} {'克%':>6} {'Grammar':>7} {'Δ':>7}")
            print(f"  " + "─" * 48)
            for bit in range(3):
                c = r['bit_layer_counts'].get(bit, 0)
                pct = c / h1 * 100
                ke = r['bit_layer_wx'][bit].get("克", 0)
                ke_pct = ke / c * 100 if c > 0 else 0
                gpred = GRAMMAR_KE[bit]
                print(f"  bit_{bit:>1} {c:>5} {pct:>5.1f}% │ {ke:>4} {ke_pct:>5.1f}% {gpred:>6.1f}% {ke_pct - gpred:>+6.1f}%")
            print(f"  Grammar: bit₁→100% 克, bit₂→0% 克, bit₀→50% 克")


# ─── Data sources ───────────────────────────────────────────────────────

def load_btc():
    try:
        import yfinance as yf
        df = yf.download("BTC-USD", start="2015-01-01", end="2025-12-31", progress=False)
        close = df[('Close', 'BTC-USD')].dropna().values
        ret = np.log(close[1:] / close[:-1])
        ret = ret[np.isfinite(ret)]
        return ret
    except Exception as e:
        print(f"  WARNING: BTC download failed: {e}")
        return None

def make_synthetics(n=4000, seed=42):
    rng = np.random.default_rng(seed)

    gauss = rng.standard_normal(n)

    ar1 = np.zeros(n)
    ar1[0] = rng.standard_normal()
    noise_scale = np.sqrt(1 - 0.3 ** 2)
    for i in range(1, n):
        ar1[i] = 0.3 * ar1[i - 1] + rng.standard_normal() * noise_scale

    garch = np.zeros(n)
    sigma2 = np.ones(n)
    omega, alpha, beta = 0.01, 0.1, 0.85
    for i in range(1, n):
        sigma2[i] = omega + alpha * garch[i - 1] ** 2 + beta * sigma2[i - 1]
        garch[i] = rng.standard_normal() * np.sqrt(sigma2[i])

    return [
        (gauss, "Gaussian i.i.d."),
        (ar1, "AR(1) ρ=0.3"),
        (garch, "GARCH(1,1)"),
    ]


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 90)
print("M5: TOPOLOGY DETECTION IN EMPIRICAL DATA")
print("=" * 90)

datasets = []

btc = load_btc()
if btc is not None:
    datasets.append((btc, "BTC-USD (2015–2025)"))
    print(f"  BTC: {len(btc)} daily returns")

for ret, lab in make_synthetics():
    datasets.append((ret, lab))

# Mapping table
print(f"\n  先天 MAPPING: bin → position → trigram → element")
print(f"  {'Bin':>4} {'Pos':>4} {'Name':>4} {'F₂³':>7} {'Element':>7}")
print(f"  " + "─" * 30)
for k in range(8):
    v = VEC[k + 1]
    print(f"  {k:>4} {k+1:>4} {NAME_BY_POS[k+1]:>4} {v[0]}{v[1]}{v[2]:>5} {Z5_NAMES[WUXING_MAP[v]]:>7}")

# Run analysis
results = []  # (label, analysis, shuffled_analysis)

for returns, label in datasets:
    print(f"\n{'=' * 90}")
    print(f"DATA: {label} (N={len(returns)})")
    print(f"{'=' * 90}")

    bins = discretize(returns)

    # Verify bin balance
    bc = Counter(bins)
    min_b, max_b = min(bc.values()), max(bc.values())
    print(f"  Bin balance: min={min_b}, max={max_b}, ideal={len(returns)//8}")

    r = analyze(bins)
    print(f"\n  --- ORIGINAL ---")
    print_analysis(r, label)

    # Shuffled control
    rng = np.random.default_rng(123)
    shuf = bins.copy()
    rng.shuffle(shuf)
    rs = analyze(shuf)
    print(f"\n  --- SHUFFLED CONTROL ---")
    print_analysis(rs, f"{label} [shuf]", show_bitlayer=False)

    results.append((label, r, rs))

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY TABLE
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 90}")
print("SUMMARY TABLE")
print(f"{'=' * 90}")

hdr = (f"  {'Source':>22} │ {'H=0%':>5} {'H=1%':>5} {'H=2%':>5} {'H=3%':>5}"
       f" │ {'比和%':>5} {'克%':>5} │ {'GMS':>4} {'E':>5} {'r':>5}"
       f" │ {'克生':>4}")
print(hdr)
print(f"  " + "─" * (len(hdr) - 2))
print(f"  {'NULL':>22} │ {12.5:>5.1f} {37.5:>5.1f} {37.5:>5.1f} {12.5:>5.1f}"
      f" │ {21.9:>5.1f} {40.6:>5.1f} │ {'':>4} {'':>5} {'':>5}"
      f" │ {'':>4}")

for label, r, rs in results:
    n = r['n_trans']
    h = {d: r['ham_counts'].get(d, 0) / n * 100 for d in range(4)}
    bh = r['wx_counts'].get("比和", 0) / n * 100
    ke = r['wx_counts'].get("克", 0) / n * 100
    p_ke = r['wx_counts'].get("克", 0) / n
    exp = (n - 1) * p_ke ** 2
    rat = r['consec_ke'] / exp if exp > 0 else 0

    short = label[:22]
    print(f"  {short:>22} │ {h[0]:>5.1f} {h[1]:>5.1f} {h[2]:>5.1f} {h[3]:>5.1f}"
          f" │ {bh:>5.1f} {ke:>5.1f} │ {r['consec_ke']:>4} {exp:>5.0f} {rat:>5.2f}"
          f" │ {r['ke_sheng']:>4}")

    # shuffled
    ns = rs['n_trans']
    hs = {d: rs['ham_counts'].get(d, 0) / ns * 100 for d in range(4)}
    bhs = rs['wx_counts'].get("比和", 0) / ns * 100
    kes = rs['wx_counts'].get("克", 0) / ns * 100
    p_kes = rs['wx_counts'].get("克", 0) / ns
    exps = (ns - 1) * p_kes ** 2
    rats = rs['consec_ke'] / exps if exps > 0 else 0

    print(f"  {'  ↳ shuffled':>22} │ {hs[0]:>5.1f} {hs[1]:>5.1f} {hs[2]:>5.1f} {hs[3]:>5.1f}"
          f" │ {bhs:>5.1f} {kes:>5.1f} │ {rs['consec_ke']:>4} {exps:>5.0f} {rats:>5.2f}"
          f" │ {rs['ke_sheng']:>4}")

# ═══════════════════════════════════════════════════════════════════════════
# BIT-LAYER SUMMARY (original data only)
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 90}")
print("BIT-LAYER 克% SUMMARY (Hamming-1 transitions only)")
print(f"{'=' * 90}")
print(f"  Grammar prediction: bit₀=50%, bit₁=100%, bit₂=0%")
print(f"\n  {'Source':>22} │ {'bit₀ 克%':>8} {'bit₁ 克%':>8} {'bit₂ 克%':>8} │ {'bit₁-bit₂':>10}")
print(f"  " + "─" * 62)
print(f"  {'GRAMMAR':>22} │ {'50.0%':>8} {'100.0%':>8} {'0.0%':>8} │ {'100.0pp':>10}")

for label, r, _ in results:
    short = label[:22]
    vals = []
    for bit in range(3):
        c = r['bit_layer_counts'].get(bit, 0)
        ke = r['bit_layer_wx'][bit].get("克", 0)
        vals.append(ke / c * 100 if c > 0 else 0)
    spread = vals[1] - vals[2]
    print(f"  {short:>22} │ {vals[0]:>7.1f}% {vals[1]:>7.1f}% {vals[2]:>7.1f}% │ {spread:>8.1f}pp")

# ═══════════════════════════════════════════════════════════════════════════
# DETECTION VERDICTS
# ═══════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 90}")
print("DETECTION VERDICTS")
print(f"{'=' * 90}")

for label, r, rs in results:
    n = r['n_trans']
    ns = rs['n_trans']

    h1 = r['ham_counts'].get(1, 0) / n * 100
    h1s = rs['ham_counts'].get(1, 0) / ns * 100
    h1_diff = h1 - h1s

    h0 = r['ham_counts'].get(0, 0) / n * 100
    h0s = rs['ham_counts'].get(0, 0) / ns * 100
    h0_diff = h0 - h0s

    p_ke = r['wx_counts'].get("克", 0) / n
    exp = (n - 1) * p_ke ** 2
    gms_ratio = r['consec_ke'] / exp if exp > 0 else 0

    # Bit-layer spread
    b1_c = r['bit_layer_counts'].get(1, 0)
    b1_ke = r['bit_layer_wx'][1].get("克", 0)
    b2_c = r['bit_layer_counts'].get(2, 0)
    b2_ke = r['bit_layer_wx'][2].get("克", 0)
    b1_pct = b1_ke / b1_c * 100 if b1_c > 0 else 0
    b2_pct = b2_ke / b2_c * 100 if b2_c > 0 else 0

    print(f"\n  {label}:")
    print(f"    Hamming-0 (persistence): {h0:.1f}% vs shuffled {h0s:.1f}% (Δ={h0_diff:+.1f}%)")
    print(f"    Hamming-1 (Q₃ edges):    {h1:.1f}% vs shuffled {h1s:.1f}% (Δ={h1_diff:+.1f}%)")
    print(f"    克-clustering (GMS/E):    {gms_ratio:.2f}x {'(clustered)' if gms_ratio > 1.15 else '(not clustered)'}")
    print(f"    Bit-layer spread:         bit₁ 克%={b1_pct:.1f}%, bit₂ 克%={b2_pct:.1f}%"
          f" (grammar predicts 100% vs 0%)")

    edge_pref = abs(h1_diff) > 2.0
    clustering = gms_ratio > 1.15
    bit_signal = (b1_pct - b2_pct) > 15.0

    signals = sum([edge_pref, clustering, bit_signal])
    print(f"    → Q₃ edge preference: {'YES' if edge_pref else 'no'}"
          f" | 克-clustering: {'YES' if clustering else 'no'}"
          f" | bit-layer signal: {'YES' if bit_signal else 'no'}"
          f" | overall: {signals}/3 signals")

print(f"\n{'=' * 90}")
print("DONE")
print(f"{'=' * 90}")
