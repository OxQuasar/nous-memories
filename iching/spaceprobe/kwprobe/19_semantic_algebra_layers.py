"""
Which algebraic layer do the semantics track?

Decompose pairwise algebraic distance into:
  1. Outer trigram pair: (lower, upper) — lives in S₄ on 8 trigrams
  2. 互 trigram pair: (hu_lower, hu_upper) — lives in H ≅ V₄ ⊂ Z₂³
  3. Kernel: (O, M, I) — the XOR symmetry class in Z₂³
  4. Basin: interface homogeneity
  5. Inner bits: bits 1-4
  6. Outer bits: bits 0,5

For each: compute distance/same matrix, correlate with semantic similarity.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kingwen')
sys.path.insert(0, '/home/quasar/nous/memories/iching/opposition-theory/phase4')

import json
import requests
import numpy as np
from collections import Counter, defaultdict
from scipy import stats
import random

from sequence import KING_WEN
from cycle_algebra import (
    hugua, reverse6, hamming6,
    lower_trigram, upper_trigram, TRIGRAM_NAMES,
    five_phase_relation,
)

random.seed(42)

# ══════════════════════════════════════════════════════════════════════════════
# 0. LOAD DATA
# ══════════════════════════════════════════════════════════════════════════════

TEXTS_DIR = '/home/quasar/nous/memories/iching/texts'
EMBED_URL = 'http://localhost:8103/embed'

kw_hex = []
kw_names = []
kw_number = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    kw_hex.append(sum(b[j] << j for j in range(6)))
    kw_names.append(KING_WEN[i][1])
    kw_number.append(KING_WEN[i][0])

def get_basin(h):
    b2 = (h >> 2) & 1
    b3 = (h >> 3) & 1
    if b2 == 0 and b3 == 0: return -1
    elif b2 == 1 and b3 == 1: return 1
    else: return 0

def get_inner(h): return (h >> 1) & 0xF
def get_outer(h): return (h & 1) | (((h >> 5) & 1) << 1)

def mirror_kernel(xor):
    bits = [(xor >> i) & 1 for i in range(6)]
    return (bits[0] ^ bits[5], bits[1] ^ bits[4], bits[2] ^ bits[3])

kernel_names = {
    (0,0,0): 'id', (1,0,0): 'O', (0,1,0): 'M', (0,0,1): 'I',
    (1,1,0): 'OM', (1,0,1): 'OI', (0,1,1): 'MI', (1,1,1): 'OMI'
}
H_KERNELS = {(0,0,0), (1,0,0), (0,1,1), (1,1,1)}

# Precompute per-hexagram properties
lo_trig = [lower_trigram(kw_hex[i]) for i in range(64)]
up_trig = [upper_trigram(kw_hex[i]) for i in range(64)]
hu_val = [hugua(kw_hex[i]) for i in range(64)]
hu_lo = [lower_trigram(hu_val[i]) for i in range(64)]
hu_up = [upper_trigram(hu_val[i]) for i in range(64)]
basins = [get_basin(kw_hex[i]) for i in range(64)]
inners = [get_inner(kw_hex[i]) for i in range(64)]
outers = [get_outer(kw_hex[i]) for i in range(64)]

# Load texts
with open(f'{TEXTS_DIR}/tuan.json') as f:
    tuan_data = json.load(f)
with open(f'{TEXTS_DIR}/xugua.json') as f:
    xugua_data = json.load(f)
with open(f'{TEXTS_DIR}/guaci.json') as f:
    guaci_data = json.load(f)

tuan_by_num = {e['number']: e['text'] for e in tuan_data['entries']}
xugua_by_num = {e['number']: e['text'] for e in xugua_data['entries']}
guaci_by_num = {e['number']: e['text'] for e in guaci_data['entries']}

tuan_texts = [tuan_by_num[kw_number[i]] for i in range(64)]
xugua_texts = [xugua_by_num[kw_number[i]] for i in range(64)]
guaci_texts = [guaci_by_num[kw_number[i]] for i in range(64)]

# Embed
def embed(texts):
    resp = requests.post(EMBED_URL, json={"texts": texts})
    resp.raise_for_status()
    return np.array(resp.json()['embeddings'])

print("Embedding texts...")
tuan_emb = embed(tuan_texts)
xugua_emb = embed(xugua_texts)
guaci_emb = embed(guaci_texts)

tuan_sim = tuan_emb @ tuan_emb.T
xugua_sim = xugua_emb @ xugua_emb.T
guaci_sim = guaci_emb @ guaci_emb.T

upper_idx = np.triu_indices(64, k=1)
N_PAIRS = len(upper_idx[0])

# ══════════════════════════════════════════════════════════════════════════════
# 1. COMPUTE ALGEBRAIC LAYER MATRICES
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("1. ALGEBRAIC LAYER MATRICES")
print("=" * 70)

# A. Outer trigram distance matrices
# Lower trigram same
lo_same = np.zeros((64, 64))
up_same = np.zeros((64, 64))
both_same = np.zeros((64, 64))  # same hexagram trigram pair
lo_dist = np.zeros((64, 64))    # hamming between lower trigrams
up_dist = np.zeros((64, 64))    # hamming between upper trigrams

for i in range(64):
    for j in range(64):
        lo_same[i,j] = 1 if lo_trig[i] == lo_trig[j] else 0
        up_same[i,j] = 1 if up_trig[i] == up_trig[j] else 0
        both_same[i,j] = 1 if (lo_trig[i] == lo_trig[j] and up_trig[i] == up_trig[j]) else 0
        lo_dist[i,j] = bin(lo_trig[i] ^ lo_trig[j]).count('1')
        up_dist[i,j] = bin(up_trig[i] ^ up_trig[j]).count('1')

# B. 互 trigram distance matrices
hu_lo_same = np.zeros((64, 64))
hu_up_same = np.zeros((64, 64))
hu_both_same = np.zeros((64, 64))
hu_lo_dist = np.zeros((64, 64))
hu_up_dist = np.zeros((64, 64))
hu_full_dist = np.zeros((64, 64))

for i in range(64):
    for j in range(64):
        hu_lo_same[i,j] = 1 if hu_lo[i] == hu_lo[j] else 0
        hu_up_same[i,j] = 1 if hu_up[i] == hu_up[j] else 0
        hu_both_same[i,j] = 1 if (hu_lo[i] == hu_lo[j] and hu_up[i] == hu_up[j]) else 0
        hu_lo_dist[i,j] = bin(hu_lo[i] ^ hu_lo[j]).count('1')
        hu_up_dist[i,j] = bin(hu_up[i] ^ hu_up[j]).count('1')
        hu_full_dist[i,j] = hamming6(hu_val[i], hu_val[j])

# C. Kernel matrices
kernel_same = np.zeros((64, 64))
kernel_in_H = np.zeros((64, 64))
kernel_O = np.zeros((64, 64))
kernel_M = np.zeros((64, 64))
kernel_I = np.zeros((64, 64))

for i in range(64):
    for j in range(64):
        xor = kw_hex[i] ^ kw_hex[j]
        k = mirror_kernel(xor)
        kernel_same[i,j] = 1 if k == (0,0,0) else 0
        kernel_in_H[i,j] = 1 if k in H_KERNELS else 0
        kernel_O[i,j] = k[0]
        kernel_M[i,j] = k[1]
        kernel_I[i,j] = k[2]

# D. Basin matrix
basin_same = np.zeros((64, 64))
for i in range(64):
    for j in range(64):
        basin_same[i,j] = 1 if basins[i] == basins[j] else 0

# E. Inner/Outer bit distances
inner_dist = np.zeros((64, 64))
outer_dist = np.zeros((64, 64))
hamming_mat = np.zeros((64, 64))

for i in range(64):
    for j in range(64):
        hamming_mat[i,j] = hamming6(kw_hex[i], kw_hex[j])
        inner_dist[i,j] = bin(inners[i] ^ inners[j]).count('1')
        outer_dist[i,j] = bin(outers[i] ^ outers[j]).count('1')

# F. S₄ orbit: same involution class (reverse pair, complement pair, etc.)
# Two hexagrams are in the same S₄ orbit if one can be reached from the other
# by applying reverse, complement, or both
s4_orbit_same = np.zeros((64, 64))
for i in range(64):
    hi = kw_hex[i]
    orbit_i = {hi, reverse6(hi), hi ^ 0x3F, reverse6(hi) ^ 0x3F}
    for j in range(64):
        s4_orbit_same[i,j] = 1 if kw_hex[j] in orbit_i else 0

print("  All matrices computed.")

# ══════════════════════════════════════════════════════════════════════════════
# 2. CORRELATIONS: EACH SEMANTIC TEXT × EACH ALGEBRAIC LAYER
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("2. FULL CORRELATION TABLE: SEMANTIC × ALGEBRAIC")
print("=" * 70)

algebraic_layers = [
    # (name, matrix, direction)  direction: 'dist' means higher=further, 'same' means 1=same
    ("Hamming (full)", hamming_mat, 'dist'),
    ("Outer bit dist", outer_dist, 'dist'),
    ("Inner bit dist", inner_dist, 'dist'),
    ("Lower trig dist", lo_dist, 'dist'),
    ("Upper trig dist", up_dist, 'dist'),
    ("Lower trig same", lo_same, 'same'),
    ("Upper trig same", up_same, 'same'),
    ("Both trig same", both_same, 'same'),
    ("互 full dist", hu_full_dist, 'dist'),
    ("互 lower dist", hu_lo_dist, 'dist'),
    ("互 upper dist", hu_up_dist, 'dist'),
    ("互 lower same", hu_lo_same, 'same'),
    ("互 upper same", hu_up_same, 'same'),
    ("互 both same", hu_both_same, 'same'),
    ("Basin same", basin_same, 'same'),
    ("Kernel = id", kernel_same, 'same'),
    ("Kernel in H", kernel_in_H, 'same'),
    ("Kernel O comp", kernel_O, 'binary'),
    ("Kernel M comp", kernel_M, 'binary'),
    ("Kernel I comp", kernel_I, 'binary'),
    ("S₄ orbit same", s4_orbit_same, 'same'),
]

semantic_layers = [
    ("Tuan", tuan_sim),
    ("Xugua", xugua_sim),
    ("Guaci", guaci_sim),
]

print(f"\n  {'Algebraic layer':>20s}", end="")
for sem_name, _ in semantic_layers:
    print(f"  {'r':>7s} {'p':>9s}", end="")
print()
print("  " + "-" * 80)

for alg_name, alg_mat, direction in algebraic_layers:
    alg_upper = alg_mat[upper_idx]
    print(f"  {alg_name:>20s}", end="")
    
    for sem_name, sem_sim in semantic_layers:
        sem_upper = sem_sim[upper_idx]
        r, p = stats.pearsonr(sem_upper, alg_upper)
        sig = "***" if p < 0.001 else "** " if p < 0.01 else "*  " if p < 0.05 else "   "
        print(f"  {r:+.4f} {p:>8.1e}{sig}", end="")
    print()

# ══════════════════════════════════════════════════════════════════════════════
# 3. PARTIAL CORRELATIONS: WHICH LAYER IS PRIMARY?
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("3. PARTIAL CORRELATIONS — TUAN")
print("=" * 70)

# For Tuan (the text that tracks algebra):
# Partial correlation of semantic sim with layer X, controlling for layer Y

tuan_upper = tuan_sim[upper_idx]

def partial_corr(x, y, z):
    """Partial correlation of x and y, controlling for z."""
    # Residualize x and y against z
    slope_xz = np.polyfit(z, x, 1)
    slope_yz = np.polyfit(z, y, 1)
    x_resid = x - np.polyval(slope_xz, z)
    y_resid = y - np.polyval(slope_yz, z)
    return stats.pearsonr(x_resid, y_resid)

print(f"\n  Tuan sim vs algebraic layer, controlling for confounds:")

# Key question: outer trigram dist vs 互 dist — which is primary?
key_layers = [
    ("Lower trig dist", lo_dist),
    ("Upper trig dist", up_dist),
    ("互 lower dist", hu_lo_dist),
    ("互 upper dist", hu_up_dist),
    ("Inner bit dist", inner_dist),
    ("Outer bit dist", outer_dist),
    ("Basin same", basin_same),
]

print(f"\n  {'Target':>20s} {'raw r':>8s} {'ctrl outer':>10s} {'ctrl inner':>10s} {'ctrl 互':>10s}")

for name, mat in key_layers:
    alg_upper = mat[upper_idx]
    raw_r, raw_p = stats.pearsonr(tuan_upper, alg_upper)
    
    # Control for outer bits
    ctrl_outer_r, ctrl_outer_p = partial_corr(tuan_upper, alg_upper, outer_dist[upper_idx])
    # Control for inner bits
    ctrl_inner_r, ctrl_inner_p = partial_corr(tuan_upper, alg_upper, inner_dist[upper_idx])
    # Control for 互 full
    ctrl_hu_r, ctrl_hu_p = partial_corr(tuan_upper, alg_upper, hu_full_dist[upper_idx])
    
    print(f"  {name:>20s} {raw_r:+.4f}   {ctrl_outer_r:+.4f}     {ctrl_inner_r:+.4f}     {ctrl_hu_r:+.4f}")

# ══════════════════════════════════════════════════════════════════════════════
# 4. TRIGRAM-LEVEL SEMANTIC SIMILARITY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("4. TRIGRAM-LEVEL: DO HEXAGRAMS WITH SAME TRIGRAMS CLUSTER?")
print("=" * 70)

# For each of the 8 trigrams, compute mean Tuan similarity
# among hexagrams that share it as lower/upper/互-lower/互-upper

for trig_type, trig_list, label in [
    ("Lower", lo_trig, "outer lower"),
    ("Upper", up_trig, "outer upper"),
    ("互 lower", hu_lo, "mutual lower"),
    ("互 upper", hu_up, "mutual upper"),
]:
    print(f"\n  {label} trigram — mean Tuan similarity within groups:")
    groups = defaultdict(list)
    for i in range(64):
        groups[trig_list[i]].append(i)
    
    within_sims = []
    between_sims = []
    
    for trig_val, members in sorted(groups.items()):
        tname = TRIGRAM_NAMES[trig_val]
        n = len(members)
        if n < 2:
            continue
        
        group_sims = []
        for a in range(len(members)):
            for b in range(a+1, len(members)):
                s = tuan_sim[members[a], members[b]]
                group_sims.append(s)
                within_sims.append(s)
        
        print(f"    {tname:4s} (n={n:2d}): mean={np.mean(group_sims):.4f}")
    
    # Between-group
    for trig_val_a, members_a in groups.items():
        for trig_val_b, members_b in groups.items():
            if trig_val_a >= trig_val_b:
                continue
            for a in members_a:
                for b in members_b:
                    between_sims.append(tuan_sim[a, b])
    
    t, p = stats.ttest_ind(within_sims, between_sims)
    print(f"    Within vs between: {np.mean(within_sims):.4f} vs {np.mean(between_sims):.4f}  "
          f"t={t:.2f}  p={p:.2e}")

# ══════════════════════════════════════════════════════════════════════════════
# 5. S₄ ORBIT SEMANTIC SIMILARITY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("5. S₄ ORBIT — DO ALGEBRAIC TWINS SHARE MEANING?")
print("=" * 70)

# Each hexagram has up to 3 orbit partners: reverse, complement, rev+comp
# Are these semantically similar?

orbit_sims = {'reverse': [], 'complement': [], 'rev_comp': [], 'unrelated': []}

for i in range(64):
    hi = kw_hex[i]
    for j in range(i+1, 64):
        hj = kw_hex[j]
        s = tuan_sim[i, j]
        
        if hj == reverse6(hi):
            orbit_sims['reverse'].append(s)
        elif hj == hi ^ 0x3F:
            orbit_sims['complement'].append(s)
        elif hj == reverse6(hi) ^ 0x3F:
            orbit_sims['rev_comp'].append(s)
        else:
            orbit_sims['unrelated'].append(s)

print(f"\n  Tuan similarity by S₄ orbit relationship:")
for rel in ['reverse', 'complement', 'rev_comp', 'unrelated']:
    sims = orbit_sims[rel]
    if sims:
        print(f"    {rel:12s}: mean={np.mean(sims):.4f}  n={len(sims)}")

# ══════════════════════════════════════════════════════════════════════════════
# 6. FIVE-PHASE RELATIONS AND SEMANTIC SIMILARITY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("6. FIVE-PHASE RELATIONS — DOES 生/克 TRACK MEANING?")
print("=" * 70)

# For consecutive pairs, what's the five-phase relation between their trigrams?
from cycle_algebra import TRIGRAM_ELEMENT

for sem_name, sem_sim in [("Tuan", tuan_sim), ("Xugua", xugua_sim)]:
    phase_sims = defaultdict(list)
    
    for i in range(63):
        lo_elem_i = TRIGRAM_ELEMENT[lo_trig[i]]
        lo_elem_j = TRIGRAM_ELEMENT[lo_trig[i+1]]
        up_elem_i = TRIGRAM_ELEMENT[up_trig[i]]
        up_elem_j = TRIGRAM_ELEMENT[up_trig[i+1]]
        lo_rel = five_phase_relation(lo_elem_i, lo_elem_j)
        up_rel = five_phase_relation(up_elem_i, up_elem_j)
        
        phase_sims[f"lo_{lo_rel}"].append(sem_sim[i, i+1])
        phase_sims[f"up_{up_rel}"].append(sem_sim[i, i+1])
    
    print(f"\n  {sem_name} — mean semantic similarity by five-phase relation:")
    RELS = ['比和', '生体', '克体', '体生用', '体克用']
    for prefix in ['lo', 'up']:
        print(f"    {prefix} trigram:")
        for rel in RELS:
            key = f"{prefix}_{rel}"
            if key in phase_sims:
                sims = phase_sims[key]
                print(f"      {rel}: mean={np.mean(sims):.4f}  n={len(sims)}")

# ══════════════════════════════════════════════════════════════════════════════
# 7. PERMUTATION TESTS FOR KEY FINDINGS
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("7. PERMUTATION TESTS FOR KEY LAYER CORRELATIONS (Tuan)")
print("=" * 70)

N_PERM = 10000

for name, mat in [
    ("Lower trig dist", lo_dist),
    ("Upper trig dist", up_dist),
    ("互 full dist", hu_full_dist),
    ("互 lower dist", hu_lo_dist),
    ("互 upper dist", hu_up_dist),
    ("Inner bit dist", inner_dist),
    ("Outer bit dist", outer_dist),
]:
    alg_upper = mat[upper_idx]
    real_r, _ = stats.pearsonr(tuan_upper, alg_upper)
    
    perm_rs = []
    idx = list(range(64))
    for _ in range(N_PERM):
        random.shuffle(idx)
        perm_sim = tuan_sim[np.ix_(idx, idx)]
        perm_upper = perm_sim[upper_idx]
        r, _ = stats.pearsonr(perm_upper, alg_upper)
        perm_rs.append(r)
    
    if real_r < 0:
        perm_p = np.mean([r <= real_r for r in perm_rs])
    else:
        perm_p = np.mean([r >= real_r for r in perm_rs])
    
    sig = "***" if perm_p < 0.001 else "** " if perm_p < 0.01 else "*  " if perm_p < 0.05 else "   "
    print(f"  {name:>20s}: r={real_r:+.4f}  perm_p={perm_p:.4f}  {sig}")

# ══════════════════════════════════════════════════════════════════════════════
# 8. SUMMARY
# ══════════════════════════════════════════════════════════════════════════════

print(f"\n{'=' * 70}")
print("8. SUMMARY")
print("=" * 70)

print("""
  The Tuan semantic similarity tracks multiple algebraic layers:
  
  OUTER TRIGRAMS (the visible hexagram structure):
    - Lower trigram distance: measures how different the bottom halves are
    - Upper trigram distance: measures how different the top halves are
    
  MUTUAL TRIGRAMS (互 — the hidden structure):
    - 互 lower distance: nuclear lower trigram difference
    - 互 upper distance: nuclear upper trigram difference
    
  KERNEL (Z₂³ — XOR symmetry class):
    - Whether the transformation is in H or not
    - Individual O, M, I components
    
  S₄ ORBIT:
    - Reverse, complement, reverse+complement relationships
    
  FIVE-PHASE:
    - 生/克 relations between consecutive trigrams
    
  The question: which layer is PRIMARY for the Tuan?
  Which does it track independently of the others?
""")
