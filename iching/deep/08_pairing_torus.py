#!/usr/bin/env python3
"""
V₄-Compatible Pairings + Palace Torus Trajectories

Task 1: Enumerate V₄-compatible pairings of 64 hexagrams.
Task 2: Palace walks on the Z₅×Z₅ torus.
Task 3: What additional constraint selects the KW pairing?
"""

import sys
from pathlib import Path
from collections import Counter, defaultdict
from itertools import product as iproduct
import importlib.util

import numpy as np

# ─── Infrastructure ──────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent
ICHING = ROOT / "iching"
OUT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(ICHING / "kingwen"))
sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))

from sequence import KING_WEN
from cycle_algebra import (
    hugua, reverse6, hamming6,
    lower_trigram, upper_trigram, TRIGRAM_NAMES,
    TRIGRAM_ELEMENT, five_phase_relation,
)

_spec = importlib.util.spec_from_file_location(
    "palace_kernel", str(ICHING / "huozhulin" / "02_palace_kernel.py"))
_pk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_pk)

generate_palaces = _pk.generate_palaces
PALACE_MASKS = _pk.PALACE_MASKS
RANK_NAMES = _pk.RANK_NAMES
PALACE_ROOTS = _pk.PALACE_ROOTS

# ─── Constants ───────────────────────────────────────────────────────────────

TRIG_NAME = {
    0: "坤", 1: "震", 2: "坎", 3: "兌",
    4: "艮", 5: "離", 6: "巽", 7: "乾",
}
ELEM = TRIGRAM_ELEMENT
SHENG_ORDER = ["Wood", "Fire", "Earth", "Metal", "Water"]
ELEM_Z5 = {e: i for i, e in enumerate(SHENG_ORDER)}

# KW data
KW = []
KW_NAME = []
for i in range(64):
    b = [int(c) for c in KING_WEN[i][2]]
    KW.append(sum(b[j] << j for j in range(6)))
    KW_NAME.append(KING_WEN[i][1])
KW_INDEX = {h: i for i, h in enumerate(KW)}

def comp(h): return h ^ 63
def rev(h): return reverse6(h)
def comp_rev(h): return comp(rev(h))

def basin_int(h):
    b2, b3 = (h >> 2) & 1, (h >> 3) & 1
    if b2 == 0 and b3 == 0: return -1
    if b2 == 1 and b3 == 1: return 1
    return 0

BASIN_NAME = {-1: "Kun", 0: "KanLi", 1: "Qian"}

def directed_rel(h):
    return five_phase_relation(ELEM[lower_trigram(h)], ELEM[upper_trigram(h)])

def elem_pair(h):
    return (ELEM[lower_trigram(h)], ELEM[upper_trigram(h)])

def hex_label(h):
    return f"#{KW_INDEX[h]+1} {KW_NAME[KW_INDEX[h]]}"

REL_SHORT = {"比和": "比和", "生体": "生体", "体生用": "体生", "克体": "克体", "体克用": "体克"}
INV_REL = {"比和": "比和", "生体": "体生用", "体生用": "生体", "克体": "体克用", "体克用": "克体"}

# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    out_lines = []
    def out(s=""):
        out_lines.append(s)
        print(s)

    out("# V₄-Compatible Pairings + Palace Torus Trajectories")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Build V₄ orbits
    # ════════════════════════════════════════════════════════════════════════

    visited = set()
    orbits = []
    for h in range(64):
        if h in visited:
            continue
        orb = sorted({h, comp(h), rev(h), comp_rev(h)})
        for x in orb:
            visited.add(x)
        orbits.append(orb)

    size2_orbits = [o for o in orbits if len(o) == 2]
    size4_orbits = [o for o in orbits if len(o) == 4]

    # ════════════════════════════════════════════════════════════════════════
    # Task 1: V₄-compatible pairings
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 1: V₄-Compatible Pairings")
    out()

    out(f"V₄ orbits: {len(size2_orbits)} of size 2, {len(size4_orbits)} of size 4")
    out(f"Size-2 orbits: pairing forced (1 way each)")
    out(f"Size-4 orbits: 3 splittings each (one per involution)")
    out()

    # For each size-4 orbit, list the 3 involution-based splittings
    out("### Size-4 orbit splittings")
    out()

    INVOLUTION_NAMES = ["comp", "rev", "c∘r"]
    INVOLUTION_FNS = [comp, rev, comp_rev]

    orbit_splittings = []  # list of list of 3 splittings per orbit
    for oi, orb in enumerate(size4_orbits):
        a, b, c, d = orb
        splittings = []
        for inv_name, inv_fn in zip(INVOLUTION_NAMES, INVOLUTION_FNS):
            # Pair each element with its image under this involution
            pairs = set()
            for x in orb:
                pair = tuple(sorted([x, inv_fn(x)]))
                pairs.add(pair)
            splittings.append((inv_name, sorted(pairs)))
        orbit_splittings.append(splittings)

        out(f"  Orbit {oi+1}: {[hex_label(x) for x in orb]}")
        for inv_name, pairs in splittings:
            p1, p2 = pairs
            out(f"    {inv_name}: {{{hex_label(p1[0])},{hex_label(p1[1])}}} + "
                f"{{{hex_label(p2[0])},{hex_label(p2[1])}}}")

        # Verify all 3 are distinct
        pair_sets = [frozenset(frozenset(p) for p in s[1]) for s in splittings]
        assert len(set(pair_sets)) == 3, f"Orbit {oi+1}: splittings not all distinct!"
    out()

    # Verify: are choices independent across orbits?
    # V₄ acts on orbits independently. A pairing is V₄-compatible iff
    # within each orbit, the splitting is one of the 3 involution-based ones.
    # Cross-orbit: V₄ maps orbit→orbit, but since each orbit is V₄-invariant,
    # there's no coupling between choices.
    out("### Independence verification")
    out()
    out("V₄ acts on each orbit independently (orbits are V₄-invariant sets).")
    out("A pairing is V₄-compatible iff within each orbit, the splitting")
    out("comes from one of the 3 involutions. No cross-orbit constraints.")
    out()

    # Proof: each involution σ maps orbit O to O. If we pair x with σ(x) within O,
    # then τ (another involution) maps this pair {x, σ(x)} to {τ(x), τσ(x)}.
    # Since τσ is the third involution ρ, this maps to {τ(x), ρ(x)}.
    # If we chose σ-splitting: pairs are {x,σ(x)} and {τ(x),ρ(x)} (where ρ=τσ).
    # Under τ: {x,σ(x)} → {τ(x), τσ(x)} = {τ(x), ρ(x)} ✓ (maps pair to pair)
    # Under σ: {x,σ(x)} → {σ(x), x} = {x,σ(x)} ✓ (fixed)
    # Under ρ: {x,σ(x)} → {ρ(x), ρσ(x)} = {ρ(x), τ(x)} ✓ (maps pair to pair)

    # Verify computationally with random mixed choices
    import random
    random.seed(42)
    n_tests = 1000
    n_pass = 0
    for _ in range(n_tests):
        # Random choice per orbit
        choices = [random.randint(0, 2) for _ in range(12)]
        # Build the full pairing
        pairing = {}
        for oi, choice in enumerate(choices):
            _, pairs = orbit_splittings[oi][choice]
            for p in pairs:
                pairing[p[0]] = p[1]
                pairing[p[1]] = p[0]
        # Add size-2 orbit pairs
        for orb in size2_orbits:
            pairing[orb[0]] = orb[1]
            pairing[orb[1]] = orb[0]

        # Check V₄ compatibility: for each pair {x,y}, check that
        # {σ(x),σ(y)} is also a pair, for all σ in V₄
        ok = True
        for x, y in list(pairing.items()):
            if x > y:
                continue  # only check each pair once
            for inv_fn in INVOLUTION_FNS:
                sx, sy = inv_fn(x), inv_fn(y)
                if pairing.get(sx) != sy:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            n_pass += 1

    out(f"  Random mixed-involution pairings tested: {n_tests}")
    out(f"  V₄-compatible: {n_pass}/{n_tests}")
    out()

    total_pairings = 3 ** 12
    out(f"### Total V₄-compatible pairings: 3^12 = {total_pairings:,}")
    out()

    # Identify the KW pairing's involution choices
    out("### KW pairing involution choices")
    out()
    kw_pairs = {}
    for k in range(32):
        a, b = KW[2*k], KW[2*k+1]
        kw_pairs[a] = b
        kw_pairs[b] = a

    kw_choices = []
    for oi, orb in enumerate(size4_orbits):
        # Which involution matches KW?
        matched = None
        for ci, (inv_name, pairs) in enumerate(orbit_splittings[oi]):
            pair_set = frozenset(frozenset(p) for p in pairs)
            kw_set = frozenset(
                frozenset([x, kw_pairs[x]]) for x in orb if x < kw_pairs[x]
            )
            if pair_set == kw_set:
                matched = (ci, inv_name)
                break
        assert matched is not None, f"KW pairing doesn't match any involution in orbit {oi+1}"
        kw_choices.append(matched)
        out(f"  Orbit {oi+1}: KW uses {matched[1]}")

    kw_inv_counts = Counter(name for _, name in kw_choices)
    out()
    out(f"  KW involution distribution: {dict(kw_inv_counts)}")
    out(f"  KW uses reversal for ALL 12 size-4 orbits: "
        f"{all(name == 'rev' for _, name in kw_choices)}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 2: Palace walks on Z₅×Z₅ torus
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 2: Palace Walks on Z₅×Z₅ Torus")
    out()

    entries, hex_info = generate_palaces()

    out("### Element-pair trajectories")
    out()

    palace_traj = {}
    for root in PALACE_ROOTS:
        trig = lower_trigram(root)
        p_name = TRIG_NAME[trig]
        p_elem = ELEM[trig]
        members = sorted([e for e in entries if e['root'] == root], key=lambda e: e['rank'])
        traj = [elem_pair(e['hex']) for e in members]
        palace_traj[trig] = traj

        out(f"  {p_name}宮 ({p_elem}):")
        cells_visited = set(traj)
        revisits = len(traj) - len(cells_visited)
        rels = [directed_rel(e['hex']) for e in members]
        unique_rels = len(set(rels))

        out(f"    Trajectory: {['→'.join([e[:2] for e in pair]) for pair in traj]}")
        out(f"    Z₅×Z₅ cells visited: {len(cells_visited)}/8 (revisits: {revisits})")
        out(f"    Distinct relations: {unique_rels}/5")
        out(f"    Relations: {[REL_SHORT.get(r, r) for r in rels]}")

        # Z₅ distances between consecutive steps
        dists = []
        for i in range(7):
            lo1, up1 = traj[i]
            lo2, up2 = traj[i+1]
            d_lo = (ELEM_Z5[lo2] - ELEM_Z5[lo1]) % 5
            d_up = (ELEM_Z5[up2] - ELEM_Z5[up1]) % 5
            dists.append((d_lo, d_up))
        out(f"    Z₅ step distances (lo,up): {dists}")
        out()

    # Coverage analysis
    out("### Torus coverage")
    out()
    all_cells = set()
    for trig, traj in palace_traj.items():
        for cell in traj:
            all_cells.add(cell)
    out(f"  Total Z₅×Z₅ cells visited across all palaces: {len(all_cells)}/25")
    out()

    # Cell occupancy
    cell_count = Counter()
    for trig, traj in palace_traj.items():
        for cell in traj:
            cell_count[cell] += 1
    out(f"  Cell occupancy distribution:")
    for occ in sorted(set(cell_count.values())):
        cells_with_occ = sum(1 for c, n in cell_count.items() if n == occ)
        out(f"    {occ} visit(s): {cells_with_occ} cells")
    unvisited = 25 - len(all_cells)
    if unvisited:
        out(f"    0 visits: {unvisited} cells")
    out()

    # Which cells are unvisited?
    if unvisited:
        out("  Unvisited Z₅×Z₅ cells:")
        for lo_e in SHENG_ORDER:
            for up_e in SHENG_ORDER:
                if (lo_e, up_e) not in all_cells:
                    rel = five_phase_relation(lo_e, up_e)
                    out(f"    ({lo_e}, {up_e}) → {rel}")
        out()

    # Compare by basin-trajectory class
    out("### Coverage by basin-trajectory class")
    out()

    # From Task 2 of 07: 4 classes
    # Kun-type (坤,坎): visit all 3 basins
    # Qian-type (離,乾): visit all 3 basins
    # KanLi+Qian (震,兌): visit 2 basins (KanLi + Qian)
    # KanLi+Kun (艮,巽): visit 2 basins (KanLi + Kun)
    basin_classes = {
        "3-basin Kun-type": [0, 2],     # 坤, 坎
        "3-basin Qian-type": [5, 7],    # 離, 乾
        "2-basin KanLi+Qian": [1, 3],   # 震, 兌
        "2-basin KanLi+Kun": [4, 6],    # 艮, 巽
    }

    for cls_name, trigs in basin_classes.items():
        cls_cells = set()
        for t in trigs:
            for cell in palace_traj[t]:
                cls_cells.add(cell)
        out(f"  {cls_name} ({','.join(TRIG_NAME[t] for t in trigs)}): "
            f"{len(cls_cells)} Z₅×Z₅ cells")

    out()

    # Complement-paired palaces
    out("### Complement-paired palace trajectories")
    out()
    comp_pairs = [(0, 7), (2, 5), (1, 6), (3, 4)]  # 坤↔乾, 坎↔離, 震↔巽, 兌↔艮
    for t1, t2 in comp_pairs:
        traj1 = palace_traj[t1]
        traj2 = palace_traj[t2]
        # Does complement relate the trajectories?
        # comp maps (lo_e, up_e) → (neg(lo_e), neg(up_e))
        neg = {"Wood": "Wood", "Fire": "Water", "Water": "Fire",
               "Earth": "Metal", "Metal": "Earth"}  # -x mod 5
        comp_traj1 = [(neg[lo], neg[up]) for lo, up in traj1]
        matches = sum(1 for a, b in zip(comp_traj1, traj2) if a == b)
        out(f"  {TRIG_NAME[t1]}↔{TRIG_NAME[t2]}: "
            f"comp(traj₁) == traj₂ at {matches}/8 ranks")
        if matches < 8:
            out(f"    comp(traj₁): {[f'{lo[:2]}/{up[:2]}' for lo, up in comp_traj1]}")
            out(f"    traj₂:       {[f'{lo[:2]}/{up[:2]}' for lo, up in traj2]}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Task 3: What selects the KW pairing?
    # ════════════════════════════════════════════════════════════════════════
    out("## Task 3: Selecting the KW Pairing")
    out()

    # Build all 3 "pure" pairings (same involution for all orbits)
    def build_pairing(inv_idx):
        """Build pairing using involution inv_idx for all size-4 orbits."""
        pairing = {}
        for orb in size2_orbits:
            pairing[orb[0]] = orb[1]
            pairing[orb[1]] = orb[0]
        for oi in range(12):
            _, pairs = orbit_splittings[oi][inv_idx]
            for p in pairs:
                pairing[p[0]] = p[1]
                pairing[p[1]] = p[0]
        return pairing

    comp_pairing = build_pairing(0)  # complement
    rev_pairing = build_pairing(1)   # reversal (= KW)
    cr_pairing = build_pairing(2)    # comp∘rev

    # Verify KW = reversal pairing
    kw_is_rev = all(kw_pairs[h] == rev_pairing[h] for h in range(64))
    out(f"  KW pairing == pure reversal pairing: {kw_is_rev}")
    out()

    # Constraint A: Total Hamming distance
    out("### Constraint A: Total Hamming distance")
    out()

    def total_hamming(pairing):
        total = 0
        seen = set()
        for h in range(64):
            if h in seen:
                continue
            partner = pairing[h]
            seen.add(h)
            seen.add(partner)
            total += hamming6(h, partner)
        return total

    for name, pair_fn in [("complement", comp_pairing),
                           ("reversal (KW)", rev_pairing),
                           ("comp∘rev", cr_pairing)]:
        th = total_hamming(pair_fn)
        out(f"  {name}: total Hamming = {th}, avg = {th/32:.2f}")
    out()

    # Hamming distance distribution for each pairing
    out("  Hamming distance distribution per pair:")
    for name, pair_fn in [("complement", comp_pairing),
                           ("reversal (KW)", rev_pairing),
                           ("comp∘rev", cr_pairing)]:
        dists = []
        seen = set()
        for h in range(64):
            if h in seen:
                continue
            partner = pair_fn[h]
            seen.add(h)
            seen.add(partner)
            dists.append(hamming6(h, partner))
        dist_count = Counter(dists)
        out(f"    {name}: {dict(sorted(dist_count.items()))}")
    out()

    # Explore ALL 3^12 pairings for Hamming distance
    out("### Hamming distance across all 3^12 pairings")
    out()

    # We can enumerate 3^12 = 531441 — feasible
    hamming_dist = defaultdict(int)
    min_hamming = float('inf')
    max_hamming = 0
    min_choices = None
    max_choices = None

    for combo in iproduct(range(3), repeat=12):
        total = 0
        # Size-2 orbit contributions (fixed)
        seen = set()
        for orb in size2_orbits:
            a, b = orb
            if a not in seen:
                total += hamming6(a, b)
                seen.add(a)
                seen.add(b)
        # Size-4 orbit contributions
        for oi, choice in enumerate(combo):
            _, pairs = orbit_splittings[oi][choice]
            for p in pairs:
                total += hamming6(p[0], p[1])

        hamming_dist[total] += 1
        if total < min_hamming:
            min_hamming = total
            min_choices = combo
        if total > max_hamming:
            max_hamming = total
            max_choices = combo

    out(f"  Range: [{min_hamming}, {max_hamming}]")
    out(f"  Distribution:")
    for h_val in sorted(hamming_dist.keys()):
        count = hamming_dist[h_val]
        marker = " ← KW" if h_val == total_hamming(rev_pairing) else ""
        marker += " ← comp" if h_val == total_hamming(comp_pairing) else ""
        marker += " ← c∘r" if h_val == total_hamming(cr_pairing) else ""
        out(f"    H={h_val}: {count:>6} pairings{marker}")
    out()

    kw_hamming = total_hamming(rev_pairing)
    rank = sum(1 for h_val in hamming_dist if h_val < kw_hamming)
    out(f"  KW Hamming total: {kw_hamming}")
    out(f"  Rank among all 3^12: {rank+1}/{len(hamming_dist)} distinct values")
    out(f"  KW is {'minimum' if kw_hamming == min_hamming else 'NOT minimum'} Hamming")
    out()

    # Constraint B: Same-basin pairs
    out("### Constraint B: Same-basin pairs")
    out()

    def count_same_basin(pairing):
        count = 0
        seen = set()
        for h in range(64):
            if h in seen:
                continue
            partner = pairing[h]
            seen.add(h)
            seen.add(partner)
            if basin_int(h) == basin_int(partner):
                count += 1
        return count

    for name, pair_fn in [("complement", comp_pairing),
                           ("reversal (KW)", rev_pairing),
                           ("comp∘rev", cr_pairing)]:
        sb = count_same_basin(pair_fn)
        out(f"  {name}: {sb}/32 same-basin pairs")
    out()

    # Constraint C: Per-orbit, is reversal the minimum-Hamming involution?
    out("### Constraint C: Per-orbit minimum-Hamming involution")
    out()

    rev_wins = 0
    for oi in range(12):
        inv_hammings = []
        for ci, (inv_name, pairs) in enumerate(orbit_splittings[oi]):
            h_sum = sum(hamming6(p[0], p[1]) for p in pairs)
            inv_hammings.append((h_sum, inv_name))
        inv_hammings.sort()
        min_h = inv_hammings[0][0]
        winners = [name for h, name in inv_hammings if h == min_h]
        is_rev_min = "rev" in winners
        if is_rev_min:
            rev_wins += 1

        orb = size4_orbits[oi]
        out(f"  Orbit {oi+1} ({hex_label(orb[0])}...): "
            f"{[(name, h) for h, name in inv_hammings]}, "
            f"min={winners}")
    out()
    out(f"  Reversal is minimum-Hamming in {rev_wins}/12 orbits")
    out()

    # Constraint D: Element-relation inversion
    out("### Constraint D: Relation inversion in pairs")
    out()

    for name, pair_fn in [("complement", comp_pairing),
                           ("reversal (KW)", rev_pairing),
                           ("comp∘rev", cr_pairing)]:
        inv_count = 0
        same_count = 0
        other_count = 0
        seen = set()
        for h in range(64):
            if h in seen:
                continue
            partner = pair_fn[h]
            seen.add(h)
            seen.add(partner)
            r1 = directed_rel(h)
            r2 = directed_rel(partner)
            if r2 == INV_REL[r1]:
                inv_count += 1
            elif r2 == r1:
                same_count += 1
            else:
                other_count += 1
        out(f"  {name}:")
        out(f"    Inverse relations: {inv_count}/32")
        out(f"    Same relation: {same_count}/32")
        out(f"    Other: {other_count}/32")
    out()

    # Constraint E: Same-palace pairs
    out("### Constraint E: Same-palace pairs")
    out()

    for name, pair_fn in [("complement", comp_pairing),
                           ("reversal (KW)", rev_pairing),
                           ("comp∘rev", cr_pairing)]:
        sp = 0
        seen = set()
        for h in range(64):
            if h in seen:
                continue
            partner = pair_fn[h]
            seen.add(h)
            seen.add(partner)
            if hex_info[h]['palace'] == hex_info[partner]['palace']:
                sp += 1
        out(f"  {name}: {sp}/32 same-palace pairs")
    out()

    # Find minimum Hamming across all 3^12
    out("### Minimum-Hamming pairings")
    out()

    # Count how many achieve minimum
    min_count = hamming_dist[min_hamming]
    out(f"  Minimum total Hamming: {min_hamming}")
    out(f"  Number of pairings achieving minimum: {min_count}")

    # Decode one minimum-Hamming pairing
    out(f"  One minimum-Hamming choice: {min_choices}")
    inv_labels = [INVOLUTION_NAMES[c] for c in min_choices]
    out(f"  Involution choices: {inv_labels}")
    out()

    # Count how many achieve maximum
    max_count = hamming_dist[max_hamming]
    out(f"  Maximum total Hamming: {max_hamming}")
    out(f"  Achieved by: {max_count} pairings")
    out(f"  One max choice: {[INVOLUTION_NAMES[c] for c in max_choices]}")
    out()

    # ════════════════════════════════════════════════════════════════════════
    # Summary
    # ════════════════════════════════════════════════════════════════════════
    out("## Summary")
    out()

    out("### V₄-compatible pairings")
    out(f"  Total: 3^12 = {total_pairings:,}")
    out(f"  Choices are independent across orbits (verified by 1000 random tests)")
    out(f"  KW pairing uses reversal for ALL 12 size-4 orbits")
    out()

    out("### What selects KW?")
    out(f"  A. Hamming distance: KW total = {kw_hamming}")
    out(f"     {'Minimum' if kw_hamming == min_hamming else 'NOT minimum'} "
        f"(min = {min_hamming}, max = {max_hamming})")

    kw_basin = count_same_basin(rev_pairing)
    comp_basin = count_same_basin(comp_pairing)
    cr_basin = count_same_basin(cr_pairing)
    out(f"  B. Same-basin pairs: KW={kw_basin}, comp={comp_basin}, c∘r={cr_basin}")
    out(f"  C. Reversal is minimum-Hamming in {rev_wins}/12 orbits")
    out(f"  D. Relation inversion: complement perfectly inverts (by algebra),"
        f" reversal does not")
    out()

    out("### Palace torus")
    out(f"  All palaces cover {len(all_cells)}/25 Z₅×Z₅ cells")
    out(f"  Complement-paired palaces have comp-related trajectories")
    out()

    # Write
    results_path = OUT_DIR / "08_pairing_torus_results.md"
    with open(results_path, "w") as f:
        f.write("\n".join(out_lines))
    print(f"\n→ Written to {results_path}")


if __name__ == "__main__":
    main()
