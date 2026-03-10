#!/usr/bin/env python3
"""
Alternative 五行 Assignment Discrimination Test

Tests whether the traditional trigram→element assignment is unique or arbitrary.
Compares traditional (A) with alternative assignments (B, C) on:
  1. Textual bridge: 吉×生体 Fisher exact test
  2. Algebraic coherence: complement=negation, cycle attractor relations
  3. Structural invariants: zero residual, 互 well-definedness, 六親 injectivity

Also: He Tu vs 生-cycle Z₅ verification and D₅ group computation.
"""

import sys
import json
from pathlib import Path
from collections import Counter, defaultdict
from itertools import permutations

import numpy as np
from scipy import stats

# ─── Infrastructure ──────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent.parent  # memories/
ICHING = ROOT / "iching"
TEXTS_DIR = ROOT / "texts" / "iching"
OUT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(ICHING / "opposition-theory" / "phase4"))
sys.path.insert(0, str(ICHING / "kingwen"))

from cycle_algebra import (
    NUM_HEX, MASK3, TRIGRAM_ELEMENT, TRIGRAM_NAMES, ELEMENTS,
    lower_trigram, upper_trigram, hugua, five_phase_relation,
    tiyong_relation, fmt6, fmt3, bit, kw_partner,
    SHENG_CYCLE, SHENG_MAP, KE_MAP,
)
from sequence import KING_WEN

sys.path.insert(0, str(ICHING / "huozhulin"))
from importlib import import_module
import importlib.util
spec = importlib.util.spec_from_file_location("p2", str(ICHING / "huozhulin" / "02_palace_kernel.py"))
p2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p2)

# ─── Constants ───────────────────────────────────────────────────────────────

VALENCE_MARKERS = ["吉", "凶", "悔", "吝", "无咎", "無咎", "厲", "利", "亨"]
TIYONG_CATEGORIES = ["比和", "生体", "体生用", "克体", "体克用"]

# Trigram values (bit0=bottom)
KAN, LI, ZHEN, XUN = 0b010, 0b101, 0b001, 0b110
KUN, GEN, DUI, QIAN = 0b000, 0b100, 0b011, 0b111

COMPLEMENT_PAIRS = [  # (a, a^111)
    (KUN, QIAN),   # 000, 111
    (ZHEN, XUN),   # 001, 110
    (KAN, LI),     # 010, 101
    (GEN, DUI),    # 100, 011
]

# ─── Data Loading ────────────────────────────────────────────────────────────

def build_kw_lookup():
    bin_to_kw, kw_to_bin, kw_to_name = {}, {}, {}
    for _, (kw_num, name, bits_str) in enumerate(KING_WEN):
        h = sum(int(c) << j for j, c in enumerate(bits_str))
        bin_to_kw[h] = kw_num
        kw_to_bin[kw_num] = h
        kw_to_name[kw_num] = name
    return bin_to_kw, kw_to_bin, kw_to_name

def load_yaoci():
    with open(TEXTS_DIR / "yaoci.json") as f:
        data = json.load(f)
    yaoci = {}
    for e in data['entries']:
        yaoci[e['number']] = [line['text'] for line in e['lines']]
    return yaoci

def extract_valence_markers(text):
    found = set()
    if "无咎" in text or "無咎" in text:
        found.add("无咎")
    for m in VALENCE_MARKERS:
        if m in ("无咎", "無咎"):
            continue
        if m in text:
            found.add(m)
    return found

# ─── Generic 五行 Engine ─────────────────────────────────────────────────────

class WuxingAssignment:
    """A trigram→element mapping with a 生-cycle ordering."""
    
    def __init__(self, name, trig_elem, cycle):
        """
        trig_elem: dict {trigram_val → element_name}
        cycle: list of 5 element names in 生-cycle order
        """
        self.name = name
        self.trig_elem = trig_elem
        self.cycle = cycle
        self.idx = {e: i for i, e in enumerate(cycle)}
        
        # Build 生 and 克 maps from cycle
        self.sheng_map = {cycle[i]: cycle[(i+1) % 5] for i in range(5)}
        self.ke_map = {cycle[i]: cycle[(i+2) % 5] for i in range(5)}
    
    def relation(self, ti_elem, yong_elem):
        if ti_elem == yong_elem: return "比和"
        if self.sheng_map[yong_elem] == ti_elem: return "生体"
        if self.ke_map[yong_elem] == ti_elem: return "克体"
        if self.sheng_map[ti_elem] == yong_elem: return "体生用"
        if self.ke_map[ti_elem] == yong_elem: return "体克用"
        raise ValueError(f"No relation: {ti_elem} vs {yong_elem}")
    
    def tiyong(self, hex_val, line):
        lo, up = lower_trigram(hex_val), upper_trigram(hex_val)
        if line <= 3:
            ti, yong = up, lo
        else:
            ti, yong = lo, up
        return self.relation(self.trig_elem[ti], self.trig_elem[yong])
    
    def surface_relation(self, hex_val):
        lo, up = lower_trigram(hex_val), upper_trigram(hex_val)
        return self.relation(self.trig_elem[lo], self.trig_elem[up])
    
    def hu_relation(self, hex_val):
        hg = hugua(hex_val)
        lo, up = lower_trigram(hg), upper_trigram(hg)
        return self.relation(self.trig_elem[lo], self.trig_elem[up])
    
    def complement_is_negation(self):
        """Check if complement (XOR 111) acts as x → -x on the cycle ring."""
        for trig in range(8):
            comp = trig ^ 0b111
            e1 = self.trig_elem[trig]
            e2 = self.trig_elem[comp]
            i1, i2 = self.idx[e1], self.idx[e2]
            if (i1 + i2) % 5 != 0:
                return False
        return True
    
    def liuqin_word(self, hex_val):
        """Compute the 六親 5-letter word for a hexagram."""
        palace_root = self._palace_root(hex_val)
        palace_elem = self.trig_elem[lower_trigram(palace_root)]
        word = []
        for line in range(1, 7):
            lo, up = lower_trigram(hex_val), upper_trigram(hex_val)
            if line <= 3:
                trig = lo
            else:
                trig = up
            line_elem = self.trig_elem[trig]
            rel = self.relation(palace_elem, line_elem)
            word.append(rel)
        return tuple(word)
    
    def _palace_root(self, hex_val):
        """Find palace root (standard 八宫 system)."""
        # Palace roots are doubled trigrams
        for root_trig in range(8):
            root = root_trig | (root_trig << 3)
            # Check all 8 ranks
            masks = [0b000000, 0b000001, 0b000011, 0b000111,
                     0b001111, 0b011111, 0b010111, 0b010000]
            for mask in masks:
                if root ^ mask == hex_val:
                    return root
        return hex_val  # fallback


# ─── Build Traditional Assignment (A) ────────────────────────────────────────

TRAD = WuxingAssignment(
    "Traditional (A)",
    trig_elem=dict(TRIGRAM_ELEMENT),
    cycle=list(SHENG_CYCLE),
)

# ─── Build Alternative B: Pair {Kan, Li} ─────────────────────────────────────

def build_assignment_b():
    """
    Keep {Kan(010), Li(101)} together as complement-fixed element.
    Split {Zhen(001)} and {Xun(110)} as singletons.
    Even coset fixed: {Kun,Gen}=one element, {Dui,Qian}=another.
    
    Enumerate all valid cycle orderings where complement = negation.
    """
    # The paired element (Kan+Li) must be at cycle position 0 (fixed by π: -0=0 mod 5)
    # The even pairs {Kun,Gen} and {Dui,Qian} can be at positions {i, -i mod 5}
    # The singletons Zhen and Xun can be at remaining positions
    
    # Name the elements abstractly: E0=paired(Kan,Li), E1..E4 = others
    # We need: for each trigram pair (a, a^111), their elements sum to 0 mod 5
    # Complement pairs and their assignments:
    #   {Kan, Li} → same element → position 0 (trivially 0+0=0)
    #   {Kun, Gen} → same element → position p1 (must have p1 + p1 = 0 mod 5 → 2*p1 = 0 → p1 = 0. 
    #                                  But position 0 is taken! So they can't be at same position...
    #   Wait. Complement-closure means each complement pair maps to {e, π(e)}.
    #   For pairs at the same element: that element must be self-conjugate under π (= negation).
    #   Self-conjugate means idx = -idx mod 5, i.e. idx = 0.
    #   Only one position (0) is self-conjugate! 
    #   In traditional: Wood is at idx 0 = self-conjugate. {Zhen, Xun} are both Wood.
    #   So ONLY ONE pair can be complement-closed (mapped to same element).
    #   The other pairs must have their two trigrams in elements that are negations of each other.
    
    # For assignment B:
    #   {Kan, Li} → position 0 (the self-conjugate slot)
    #   {Kun, Gen} → positions {p, -p mod 5} where p ≠ 0
    #   {Dui, Qian} → positions {q, -q mod 5} where q ≠ 0, q ≠ p, q ≠ -p
    #   {Zhen} → position r (singleton)
    #   {Xun} → position -r mod 5 (since Zhen^111=Xun, they must be at conjugate positions)
    
    # Wait — Zhen(001) ^ 111 = Xun(110). So {Zhen, Xun} is a complement pair.
    # Under π: their elements must be at positions {r, -r mod 5}.
    # Since they're singletons, they CAN be at different positions as long as those positions
    # are negations of each other. If r ≠ 0 and r ≠ -r (i.e. r ≠ 0), this works.
    
    # Similarly {Kun, Gen}: Kun(000)^111 = Qian(111). Wait! Kun^111 = Qian, NOT Gen.
    # Let me re-check complement pairs:
    #   000 ^ 111 = 111 → {Kun, Qian}
    #   001 ^ 111 = 110 → {Zhen, Xun}
    #   010 ^ 111 = 101 → {Kan, Li}
    #   011 ^ 111 = 100 → {Dui, Gen}
    
    # So complement pairs are: {Kun,Qian}, {Zhen,Xun}, {Kan,Li}, {Dui,Gen}
    # NOT {Kun,Gen} and {Dui,Qian}!
    
    # In the traditional assignment:
    #   {Kun(000), Gen(100)} = Earth — but these are NOT complement pairs!
    #   Complement: Kun^111=Qian, Gen^111=Dui.
    #   So {Kun,Gen}=Earth forces {Qian,Dui}=Metal (complement of Earth on the cycle).
    #   Earth is at idx 2, Metal at idx 3. Check: 2+3=5=0 mod 5. ✓
    
    # For complement = negation, we need:
    # For each complement pair (a, a^111): idx(elem(a)) + idx(elem(a^111)) = 0 mod 5
    
    # Complement pairs: {Kun,Qian}, {Zhen,Xun}, {Kan,Li}, {Dui,Gen}
    
    # Assignment B structure:
    #   {Kan, Li} at SAME element = position 0 (self-conjugate)
    #   For {Kun, Qian}: they're in the SAME-element pairs in traditional ({Kun,Gen}=Earth, {Qian,Dui}=Metal)
    #   but {Kun, Qian} is a complement pair — they need elements at conjugate positions.
    #   Kun and Qian are in DIFFERENT elements in traditional. Good.
    
    # In assignment B, the even coset is still {Kun, Gen, Dui, Qian} (parity-0 trigrams).
    # The partition must be {2,2,2,1,1} with 3 pairs and 2 singletons.
    # Pairs in B: {Kan,Li}=one, {Kun,?}=another, {?,?}=another. Singletons: remaining two.
    
    # Actually, let me think about this differently.
    # The even-parity coset is: {000, 011, 100, 111} = {Kun, Dui, Gen, Qian}
    # The odd-parity coset is: {001, 010, 101, 110} = {Zhen, Kan, Li, Xun}
    
    # The captain says: "The even-parity coset is forced: {Kun,Gen}=Earth, {Dui,Qian}=Metal."
    # This is about the PARITY SEPARATION of the XOR masks.
    # 
    # Wait, let me re-read: "Only the odd-parity coset has freedom."
    # So the even coset assignment is fixed regardless of which odd-coset pairing we choose?
    # That's only true if the even coset pairs are forced by the complement constraint.
    # 
    # Actually the captain's claim about even coset being forced may be specific to the 
    # parity-separation property, not complement closure. Let me not assume that and 
    # enumerate properly.
    
    # For assignment B: {Kan, Li} are paired (same element).
    # {Zhen, Xun} are split (different elements, as singletons).
    # We need to find which 5-element cycle orderings make complement = negation.
    
    results = []
    elements = ["E0", "E1", "E2", "E3", "E4"]
    
    # We need to assign each of the 8 trigrams to one of 5 elements 
    # such that partition is {2,2,2,1,1} and:
    # 1. {Kan, Li} are in the same element (the paired odd-coset element)
    # 2. {Zhen, Xun} are singletons
    # 3. Even coset: two pairs from {Kun, Gen, Dui, Qian}
    # 4. Complement pairs {Kun,Qian} and {Dui,Gen} must have elements at conjugate cycle positions
    # 5. {Zhen,Xun} as complement pair must have elements at conjugate positions
    # 6. {Kan,Li} at position 0 (self-conjugate)
    
    # Even coset pairs that respect complement: 
    # {Kun,Qian} is a complement pair → their elements are at {p, -p}
    # {Dui,Gen} is a complement pair → their elements are at {q, -q}
    # We need exactly 2 pairs from the even coset. Options:
    #   Option i: {Kun,Gen} paired, {Dui,Qian} paired (traditional)
    #   Option ii: {Kun,Dui} paired, {Gen,Qian} paired
    #   Option iii: {Kun,Qian} paired, {Dui,Gen} paired
    #   Option iv: All other pairings with singletons from even coset
    
    # But we need total partition {2,2,2,1,1}. We have 3 pairs and 2 singletons.
    # Pairs: {Kan,Li} + 2 even-coset pairs. Singletons: {Zhen} + {Xun}.
    # Even coset has 4 trigrams → exactly 2 pairs (using all 4).
    # 3 ways to partition 4 items into 2 pairs: {ab,cd}, {ac,bd}, {ad,bc}
    
    even_trigrams = [KUN, GEN, DUI, QIAN]  # 000, 100, 011, 111
    even_pairings = [
        [(KUN, GEN), (DUI, QIAN)],    # Traditional
        [(KUN, DUI), (GEN, QIAN)],
        [(KUN, QIAN), (DUI, GEN)],     # Complement pairs together
    ]
    
    for even_pairing in even_pairings:
        (e1a, e1b), (e2a, e2b) = even_pairing
        # 5 elements. Kan+Li at pos 0. 
        # Even pair 1 at some element. Even pair 2 at some element.
        # Zhen at some element. Xun at some element.
        # Constraint: complement = negation.
        
        # Try all possible position assignments.
        # Positions 1,2,3,4 for the remaining 4 groups.
        for perm in permutations([1, 2, 3, 4]):
            pos_e1, pos_e2, pos_zhen, pos_xun = perm
            
            # Check complement constraints:
            # {Kan, Li} at pos 0 → Kan^111=Li, both at 0 → 0+0=0 mod 5 ✓
            
            # Kun(000)^111 = Qian(111). Need pos(Kun) + pos(Qian) = 0 mod 5
            pos_kun = pos_e1 if KUN in (e1a, e1b) else pos_e2
            pos_qian = pos_e1 if QIAN in (e1a, e1b) else pos_e2
            if (pos_kun + pos_qian) % 5 != 0:
                continue
            
            # Dui(011)^111 = Gen(100). Need pos(Dui) + pos(Gen) = 0 mod 5
            pos_dui = pos_e1 if DUI in (e1a, e1b) else pos_e2
            pos_gen = pos_e1 if GEN in (e1a, e1b) else pos_e2
            if (pos_dui + pos_gen) % 5 != 0:
                continue
            
            # Zhen(001)^111 = Xun(110). Need pos(Zhen) + pos(Xun) = 0 mod 5
            if (pos_zhen + pos_xun) % 5 != 0:
                continue
            
            # Build the assignment
            trig_pos = {
                KAN: 0, LI: 0,
                e1a: pos_e1, e1b: pos_e1,
                e2a: pos_e2, e2b: pos_e2,
                ZHEN: pos_zhen, XUN: pos_xun,
            }
            
            # Name elements by position
            cycle = [None] * 5
            for trig, pos in trig_pos.items():
                name = TRIGRAM_NAMES[trig].split()[0]
                if cycle[pos] is None:
                    cycle[pos] = f"Pos{pos}"
            
            # Build trig→element map using position names
            elem_names = [f"P{i}" for i in range(5)]
            trig_elem = {trig: elem_names[pos] for trig, pos in trig_pos.items()}
            
            results.append({
                'even_pairing': even_pairing,
                'trig_pos': trig_pos,
                'trig_elem': trig_elem,
                'cycle': elem_names,
                'positions': {
                    'Kan+Li': 0,
                    f'{TRIGRAM_NAMES[e1a].split()[0]}+{TRIGRAM_NAMES[e1b].split()[0]}': pos_e1,
                    f'{TRIGRAM_NAMES[e2a].split()[0]}+{TRIGRAM_NAMES[e2b].split()[0]}': pos_e2,
                    TRIGRAM_NAMES[ZHEN].split()[0]: pos_zhen,
                    TRIGRAM_NAMES[XUN].split()[0]: pos_xun,
                },
            })
    
    return results


def build_assignment_c():
    """
    Cross-pair: e.g. {Kan(010), Zhen(001)} and {Li(101), Xun(110)}.
    These are NOT complement pairs. Check if complement=negation is possible.
    """
    # {Kan, Zhen} paired, {Li, Xun} paired.
    # Complement pairs: Kan^111=Li, Zhen^111=Xun.
    # So Kan and Li are in DIFFERENT elements. Zhen and Xun are in DIFFERENT elements.
    # For complement=negation: pos(Kan)+pos(Li)=0, pos(Zhen)+pos(Xun)=0.
    # But Kan and Zhen are in the SAME element: pos(Kan)=pos(Zhen).
    # And Li and Xun are in the SAME element: pos(Li)=pos(Xun).
    # So: pos(Kan)+pos(Li)=0 and pos(Zhen)+pos(Xun)=0
    # → pos(Kan)+pos(Li)=0 and pos(Kan)+pos(Li)=0 ← same constraint. OK so far.
    # Let pos(Kan)=pos(Zhen)=a, pos(Li)=pos(Xun)=b, a+b=0 mod 5, a≠b.
    # This means a≠0 (since if a=0 then b=0, contradiction a≠b).
    # So neither {Kan,Zhen} nor {Li,Xun} is at the self-conjugate position.
    
    # We also need a self-conjugate element (position 0). It must come from even coset.
    # Even coset: {Kun, Gen, Dui, Qian}. Need one pair at position 0.
    # Complement pairs in even: {Kun,Qian}, {Dui,Gen}.
    # For a pair at position 0 (self-conjugate): both members must be complement-conjugate
    # at position 0, meaning their complement partner is also at 0.
    # {Kun,Qian}: if both at 0, complement satisfied. ✓
    # But {Kun,Qian} isn't usually a pair in {2,2,2,1,1} ... unless we pair them.
    
    # Total structure: 3 pairs + 2 singletons = 8 trigrams.
    # Odd coset: {Kan,Zhen} and {Li,Xun} → 2 pairs using all 4 odd trigrams.
    # Even coset: need 1 more pair + 2 singletons, or we could have 1 pair from even.
    # Wait: we have 3 pairs total. 2 from odd. 1 from even. Plus 2 singletons from even.
    
    # Even coset pairings for the 1 pair:
    # {Kun,Gen}, {Kun,Dui}, {Kun,Qian}, {Gen,Dui}, {Gen,Qian}, {Dui,Qian}
    # The remaining 2 are singletons.
    
    results = []
    even_pairs_options = [
        ((KUN, GEN), [DUI, QIAN]),
        ((KUN, DUI), [GEN, QIAN]),
        ((KUN, QIAN), [GEN, DUI]),
        ((GEN, DUI), [KUN, QIAN]),
        ((GEN, QIAN), [KUN, DUI]),
        ((DUI, QIAN), [KUN, GEN]),
    ]
    
    for (ep_a, ep_b), singletons in even_pairs_options:
        s1, s2 = singletons
        # Positions: 5 elements at positions 0..4
        # Groups: {Kan,Zhen}=a, {Li,Xun}=b, {ep_a,ep_b}=c, {s1}=d, {s2}=e
        # Constraints:
        #   a + b = 0 mod 5 (Kan-Li and Zhen-Xun complement constraints)
        #   For {ep_a, ep_b}: check their complement relationships
        #     ep_a^111 and ep_b^111 — are they related?
        #   For s1, s2: s1^111 and s2^111 need complement constraint
        
        for perm in permutations(range(5)):
            pos_a, pos_b, pos_c, pos_d, pos_e = perm
            
            # Constraint: a + b = 0 mod 5 (Kan↔Li complement, Zhen↔Xun complement)
            if (pos_a + pos_b) % 5 != 0:
                continue
            
            # Build position map for all trigrams
            trig_pos = {
                KAN: pos_a, ZHEN: pos_a,
                LI: pos_b, XUN: pos_b,
                ep_a: pos_c, ep_b: pos_c,
                s1: pos_d, s2: pos_e,
            }
            
            # Check complement constraints for even trigrams:
            # Kun^111=Qian: pos(Kun)+pos(Qian)=0
            if (trig_pos[KUN] + trig_pos[QIAN]) % 5 != 0:
                continue
            # Dui^111=Gen: pos(Dui)+pos(Gen)=0
            if (trig_pos[DUI] + trig_pos[GEN]) % 5 != 0:
                continue
            
            # Valid! Build assignment
            elem_names = [f"P{i}" for i in range(5)]
            trig_elem = {trig: elem_names[pos] for trig, pos in trig_pos.items()}
            
            results.append({
                'trig_pos': trig_pos,
                'trig_elem': trig_elem,
                'cycle': elem_names,
                'description': (
                    f"{{Kan,Zhen}}@{pos_a} {{Li,Xun}}@{pos_b} "
                    f"{{{TRIGRAM_NAMES[ep_a].split()[0]},{TRIGRAM_NAMES[ep_b].split()[0]}}}@{pos_c} "
                    f"{TRIGRAM_NAMES[s1].split()[0]}@{pos_d} {TRIGRAM_NAMES[s2].split()[0]}@{pos_e}"
                ),
            })
    
    return results


# ─── Parity Separation Check ────────────────────────────────────────────────

def check_parity_separation(assignment):
    """
    Check if the 生-cycle has the parity separation property:
    b₀⊕b₁ parity separates 生-exclusive from 克-exclusive XOR masks.
    
    For each edge type (生 or 克), collect all XOR masks between trigram pairs.
    Check if 生-only masks have one parity and 克-only masks have the other.
    """
    elem_trigs = defaultdict(list)
    for trig, elem in assignment.trig_elem.items():
        elem_trigs[elem].append(trig)
    
    cycle = assignment.cycle
    sheng_edges = [(cycle[i], cycle[(i+1) % 5]) for i in range(5)]
    ke_edges = [(cycle[i], cycle[(i+2) % 5]) for i in range(5)]
    
    sheng_masks = set()
    for src, tgt in sheng_edges:
        for ts in elem_trigs[src]:
            for tt in elem_trigs[tgt]:
                sheng_masks.add(ts ^ tt)
    sheng_masks.discard(0)
    
    ke_masks = set()
    for src, tgt in ke_edges:
        for ts in elem_trigs[src]:
            for tt in elem_trigs[tgt]:
                ke_masks.add(ts ^ tt)
    ke_masks.discard(0)
    
    sheng_only = sheng_masks - ke_masks
    ke_only = ke_masks - sheng_masks
    both = sheng_masks & ke_masks
    
    if not sheng_only or not ke_only:
        return False, "empty exclusive set"
    
    # Check parity separation (b₀⊕b₁ of each mask)
    def parity(mask):
        return (mask & 1) ^ ((mask >> 1) & 1)
    
    sheng_parities = {parity(m) for m in sheng_only}
    ke_parities = {parity(m) for m in ke_only}
    
    separated = len(sheng_parities) == 1 and len(ke_parities) == 1 and sheng_parities != ke_parities
    return separated, {
        'sheng_only': sheng_only, 'ke_only': ke_only, 'both': both,
        'sheng_parities': sheng_parities, 'ke_parities': ke_parities,
    }


# ─── Tests ───────────────────────────────────────────────────────────────────

def test_textual_bridge(assignment, bin_to_kw, yaoci):
    """Cross-tabulate tiyong relation × valence markers. Return Fisher test for 吉×生体."""
    records = []
    for h in range(NUM_HEX):
        kw = bin_to_kw[h]
        for line_idx, text in enumerate(yaoci[kw]):
            line_pos = line_idx + 1
            rel = assignment.tiyong(h, line_pos)
            markers = extract_valence_markers(text)
            records.append({'relation': rel, 'markers': markers})
    
    # Cross-tab
    rel_counts = Counter(r['relation'] for r in records)
    cross = defaultdict(lambda: defaultdict(int))
    for r in records:
        for m in r['markers']:
            cross[r['relation']][m] += 1
    
    # Fisher: 生体 vs rest for 吉
    shengti = [r for r in records if r['relation'] == "生体"]
    rest = [r for r in records if r['relation'] != "生体"]
    st_ji = sum(1 for r in shengti if "吉" in r['markers'])
    rest_ji = sum(1 for r in rest if "吉" in r['markers'])
    table = np.array([
        [st_ji, len(shengti) - st_ji],
        [rest_ji, len(rest) - rest_ji],
    ])
    if len(shengti) > 0 and len(rest) > 0:
        odds, p = stats.fisher_exact(table)
    else:
        odds, p = float('nan'), 1.0
    
    # Also: 生体 吉 rate, 比和 凶 rate, 克体 吉 rate
    def rate(rel, marker):
        n = rel_counts[rel]
        if n == 0: return 0.0
        return cross[rel][marker] / n
    
    return {
        'n_shengti': len(shengti),
        'shengti_ji_rate': rate("生体", "吉"),
        'shengti_ji_n': cross["生体"]["吉"],
        'bihe_xiong_rate': rate("比和", "凶"),
        'keti_ji_rate': rate("克体", "吉"),
        'fisher_or': odds,
        'fisher_p': p,
        'rel_counts': dict(rel_counts),
        'cross': {rel: dict(markers) for rel, markers in cross.items()},
    }


def test_cycle_attractors(assignment):
    """Check surface relation of 既濟 and 未濟."""
    jiji = 0b010101    # hex 63: Water(010) over Fire(101)
    weiji = 0b101010   # hex 64: Fire(101) over Water(010)
    
    rel_jiji = assignment.surface_relation(jiji)
    rel_weiji = assignment.surface_relation(weiji)
    return rel_jiji, rel_weiji


def test_zero_residual(assignment):
    """Check if (surface_cell, hu_cell, basin, palace_element) uniquely identifies all 64 hexagrams."""
    profiles = defaultdict(list)
    for h in range(NUM_HEX):
        lo_elem = assignment.trig_elem[lower_trigram(h)]
        up_elem = assignment.trig_elem[upper_trigram(h)]
        hg = hugua(h)
        hu_lo_elem = assignment.trig_elem[lower_trigram(hg)]
        hu_up_elem = assignment.trig_elem[upper_trigram(hg)]
        b = p2.basin(h)
        # Palace element: element of the palace root's lower trigram
        palace_root = assignment._palace_root(h)
        pe = assignment.trig_elem[lower_trigram(palace_root)]
        
        profile = (lo_elem, up_elem, hu_lo_elem, hu_up_elem, b, pe)
        profiles[profile].append(h)
    
    n_unique = sum(1 for v in profiles.values() if len(v) == 1)
    n_collisions = sum(1 for v in profiles.values() if len(v) > 1)
    max_collision = max(len(v) for v in profiles.values())
    return n_unique, n_collisions, max_collision, len(profiles)


def test_hu_welldefined(assignment):
    """Count how many of 25 torus cells are hu-well-defined."""
    # Torus cell = (lower_element, upper_element)
    # For each cell, check if all hexagrams in it map to the same hu_cell.
    cells = defaultdict(set)
    for h in range(NUM_HEX):
        lo = assignment.trig_elem[lower_trigram(h)]
        up = assignment.trig_elem[upper_trigram(h)]
        hg = hugua(h)
        hu_lo = assignment.trig_elem[lower_trigram(hg)]
        hu_up = assignment.trig_elem[upper_trigram(hg)]
        cells[(lo, up)].add((hu_lo, hu_up))
    
    well_defined = sum(1 for v in cells.values() if len(v) == 1)
    return well_defined, len(cells)


def test_liuqin_injectivity(assignment):
    """Count unique 六親 words across all 64 hexagrams."""
    words = {}
    for h in range(NUM_HEX):
        w = assignment.liuqin_word(h)
        words[h] = w
    unique = len(set(words.values()))
    return unique


# ─── Part 4: He Tu vs 生-cycle D₅ ────────────────────────────────────────────

def group_from_generators(gens, n=5):
    """Compute group generated by permutations (as dicts on Z_n)."""
    # Represent permutations as tuples
    def perm_to_tuple(d):
        return tuple(d[i] for i in range(n))
    
    def compose(a, b):
        # a then b
        return tuple(b[a[i]] for i in range(n))
    
    identity = tuple(range(n))
    gen_tuples = [perm_to_tuple(g) for g in gens]
    
    group = {identity}
    queue = list(gen_tuples)
    group.update(queue)
    
    while queue:
        current = queue.pop(0)
        for g in gen_tuples + [identity]:
            for new in [compose(current, g), compose(g, current)]:
                if new not in group:
                    group.add(new)
                    queue.append(new)
    
    return group


def part4_hetu_verification():
    """Verify He Tu vs 生-cycle Z₅ properties."""
    results = []
    w = results.append
    
    w("## Part 4: He Tu vs 生-cycle Z₅\n")
    
    # 生-cycle: Wood=0, Fire=1, Earth=2, Metal=3, Water=4
    sheng_idx = {e: i for i, e in enumerate(SHENG_CYCLE)}
    
    # He Tu: Earth=0, Water=1, Fire=2, Wood=3, Metal=4
    hetu_order = ["Earth", "Water", "Fire", "Wood", "Metal"]
    hetu_idx = {e: i for i, e in enumerate(hetu_order)}
    
    # π (complement anti-automorphism): Wood↔Wood, Fire↔Water, Earth↔Metal
    pi_map = {"Wood": "Wood", "Fire": "Water", "Water": "Fire", "Earth": "Metal", "Metal": "Earth"}
    
    # 1. Confirm π = -x on 生-cycle
    w("### 1. π = -x mod 5 on 生-cycle ring\n")
    w("| Element | x (生) | π(x) | -x mod 5 | Match |")
    w("|---------|--------|------|----------|-------|")
    all_match = True
    for e in SHENG_CYCLE:
        x = sheng_idx[e]
        pi_x = sheng_idx[pi_map[e]]
        neg_x = (-x) % 5
        match = pi_x == neg_x
        all_match &= match
        w(f"| {e} | {x} | {pi_x} | {neg_x} | {'✓' if match else '✗'} |")
    w(f"\n**Result: π = -x mod 5 on 生-cycle: {all_match}**\n")
    
    # 2. π is not affine on He Tu
    w("### 2. π on He Tu ring\n")
    w("| Element | x (HeTu) | π(x) | ")
    w("|---------|----------|------|")
    pi_hetu = {}
    for e in hetu_order:
        x = hetu_idx[e]
        pi_x = hetu_idx[pi_map[e]]
        pi_hetu[x] = pi_x
        w(f"| {e} | {x} | {pi_x} |")
    
    w("\nSearching all 25 affine maps f(x) = ax + b mod 5:")
    found_affine = False
    for a in range(5):
        for b in range(5):
            if all((a * x + b) % 5 == pi_hetu[x] for x in range(5)):
                w(f"  MATCH: f(x) = {a}x + {b}")
                found_affine = True
    if not found_affine:
        w("  NO affine map matches. **π is not affine on He Tu.**")
    w("")
    
    # 3. Generate D₅ on both labelings
    w("### 3. D₅ generation\n")
    
    # σ = 生-step on 生-cycle: x → x+1 mod 5
    sigma_sheng = {i: (i + 1) % 5 for i in range(5)}
    pi_sheng = {i: (-i) % 5 for i in range(5)}
    
    group_sheng = group_from_generators([sigma_sheng, pi_sheng])
    w(f"On 生-cycle: |⟨σ, π⟩| = {len(group_sheng)}")
    w(f"  D₅ has order 10: {'✓' if len(group_sheng) == 10 else '✗'}")
    
    # σ on He Tu = 生-step expressed in He Tu coordinates
    # 生-step maps element e to SHENG_MAP[e]. Translate to He Tu indices.
    sigma_hetu = {}
    for e in SHENG_CYCLE:
        src = hetu_idx[e]
        tgt = hetu_idx[SHENG_MAP[e]]
        sigma_hetu[src] = tgt
    
    pi_hetu_dict = {hetu_idx[e]: hetu_idx[pi_map[e]] for e in SHENG_CYCLE}
    
    group_hetu = group_from_generators([sigma_hetu, pi_hetu_dict])
    w(f"On He Tu: |⟨σ, π⟩| = {len(group_hetu)}")
    w(f"  D₅ has order 10: {'✓' if len(group_hetu) == 10 else '✗'}")
    w("")
    
    # 4. Conjugating permutation γ
    w("### 4. Conjugating permutation γ\n")
    # γ maps 生-cycle index → He Tu index for same element
    gamma = {}
    for e in SHENG_CYCLE:
        gamma[sheng_idx[e]] = hetu_idx[e]
    w(f"γ: 生-cycle → He Tu")
    for e in SHENG_CYCLE:
        w(f"  {e}: {sheng_idx[e]} → {hetu_idx[e]}")
    
    # Verify: γ σ_sheng γ⁻¹ = σ_hetu
    gamma_inv = {v: k for k, v in gamma.items()}
    conjugated_sigma = {}
    for x in range(5):
        conjugated_sigma[x] = gamma[sigma_sheng[gamma_inv[x]]]
    match_sigma = all(conjugated_sigma[x] == sigma_hetu[x] for x in range(5))
    w(f"\nγ σ_sheng γ⁻¹ = σ_hetu: {match_sigma}")
    
    conjugated_pi = {}
    for x in range(5):
        conjugated_pi[x] = gamma[pi_sheng[gamma_inv[x]]]
    match_pi = all(conjugated_pi[x] == pi_hetu_dict[x] for x in range(5))
    w(f"γ π_sheng γ⁻¹ = π_hetu: {match_pi}")
    
    w(f"\n**Both actions are D₅, conjugated by γ = {[gamma[i] for i in range(5)]}**")
    w(f"**γ as cycle notation:** {gamma}")
    w("")
    
    return '\n'.join(results)


# ─── Part 5: 3×5 Grid ────────────────────────────────────────────────────────

def part5_grid(assignment, bin_to_kw, yaoci):
    """Project hexagrams into (lower_element, hu_relation, upper_element) space."""
    results = []
    w = results.append
    
    w("## Part 5: Z₅ × Z₅ × Z₅ Grid (surface × hu × surface)\n")
    
    cells = defaultdict(list)
    for h in range(NUM_HEX):
        lo = assignment.trig_elem[lower_trigram(h)]
        up = assignment.trig_elem[upper_trigram(h)]
        hu_rel = assignment.hu_relation(h)
        cells[(lo, hu_rel, up)].append(h)
    
    w(f"Total cells realized: {len(cells)} of {5*5*5} = 125 possible\n")
    
    # Population distribution
    pops = [len(v) for v in cells.values()]
    w(f"Population: min={min(pops)}, max={max(pops)}, mean={np.mean(pops):.1f}, median={np.median(pops):.0f}")
    pop_dist = Counter(pops)
    w(f"Population distribution: {dict(sorted(pop_dist.items()))}\n")
    
    # By hu_relation
    w("### Hexagrams per hu_relation\n")
    hu_rel_counts = Counter()
    for (lo, hu_rel, up), hexes in cells.items():
        hu_rel_counts[hu_rel] += len(hexes)
    w("| hu_relation | n_hex |")
    w("|-------------|-------|")
    for rel in TIYONG_CATEGORIES:
        w(f"| {rel} | {hu_rel_counts.get(rel, 0)} |")
    w("")
    
    # Cross-tabulate with valence
    w("### Valence by hu_relation (middle coordinate)\n")
    hu_ji = defaultdict(int)
    hu_xiong = defaultdict(int)
    hu_total = defaultdict(int)
    
    for h in range(NUM_HEX):
        hu_rel = assignment.hu_relation(h)
        kw = bin_to_kw[h]
        for line_idx, text in enumerate(yaoci[kw]):
            markers = extract_valence_markers(text)
            hu_total[hu_rel] += 1
            if "吉" in markers: hu_ji[hu_rel] += 1
            if "凶" in markers: hu_xiong[hu_rel] += 1
    
    w("| hu_relation | n | 吉 | 吉 rate | 凶 | 凶 rate |")
    w("|-------------|---|---|---------|---|---------|")
    for rel in TIYONG_CATEGORIES:
        n = hu_total[rel]
        ji = hu_ji[rel]
        xi = hu_xiong[rel]
        if n > 0:
            w(f"| {rel} | {n} | {ji} | {ji/n:.3f} | {xi} | {xi/n:.3f} |")
    w("")
    
    # Does hu_relation add discriminative power?
    # χ² test: 吉 distribution across hu_relation categories
    table = []
    for rel in TIYONG_CATEGORIES:
        n = hu_total[rel]
        ji = hu_ji[rel]
        if n > 0:
            table.append([ji, n - ji])
    if len(table) >= 2:
        chi2, p, dof, _ = stats.chi2_contingency(np.array(table))
        w(f"χ² test (吉 across hu_relation): χ²={chi2:.3f}, p={p:.4f}, dof={dof}")
    
    # Forbidden cells analysis
    w("\n### Forbidden cells analysis\n")
    all_possible = set()
    for lo in assignment.cycle:
        for hu_rel in TIYONG_CATEGORIES:
            for up in assignment.cycle:
                all_possible.add((lo, hu_rel, up))
    forbidden = all_possible - set(cells.keys())
    w(f"Forbidden cells: {len(forbidden)} of 125")
    w(f"Realized cells: {len(cells)} of 125")
    w(f"Occupancy rate: {len(cells)/125:.3f}\n")
    
    return '\n'.join(results)


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("ALTERNATIVE 五行 ASSIGNMENT DISCRIMINATION TEST")
    print("=" * 70)
    
    bin_to_kw, kw_to_bin, kw_to_name = build_kw_lookup()
    yaoci = load_yaoci()
    
    md = []
    w = md.append
    w("# Alternative 五行 Assignment Discrimination Test\n")
    w("Tests whether the traditional trigram→element assignment is uniquely forced.\n")
    
    # ═══════════════════════════════════════════════════════════════════════
    # Part 1: Enumerate alternatives
    # ═══════════════════════════════════════════════════════════════════════
    
    w("## Part 1: Alternative Assignments\n")
    
    # Traditional
    w("### Assignment A (Traditional)\n")
    w("| Trigram | Binary | Element |")
    w("|---------|--------|---------|")
    for trig in sorted(TRIGRAM_ELEMENT.keys()):
        w(f"| {TRIGRAM_NAMES[trig]} | {fmt3(trig)} | {TRIGRAM_ELEMENT[trig]} |")
    w(f"\n生-cycle: {' → '.join(SHENG_CYCLE)}")
    w(f"Complement = negation: {TRAD.complement_is_negation()}\n")
    
    # Assignment B
    w("### Assignment B: Pair {Kan, Li}\n")
    b_configs = build_assignment_b()
    w(f"Total complement-respecting configurations: {len(b_configs)}\n")
    
    if b_configs:
        # Show first few
        for i, cfg in enumerate(b_configs[:6]):
            w(f"**B.{i+1}**: positions = {cfg['positions']}")
    
    # For testing, we need concrete element names. Use positional names.
    # Pick the first valid B configuration and build a WuxingAssignment.
    b_assignments = []
    for cfg in b_configs:
        elem_names = cfg['cycle']
        trig_elem = cfg['trig_elem']
        try:
            wa = WuxingAssignment(f"B", trig_elem, elem_names)
            b_assignments.append((cfg, wa))
        except Exception as e:
            pass
    
    w(f"\nValid B assignments built: {len(b_assignments)}")
    
    # Assignment C
    w("\n### Assignment C: Cross-pair {Kan, Zhen} + {Li, Xun}\n")
    c_configs = build_assignment_c()
    w(f"Total complement-respecting configurations: {len(c_configs)}\n")
    
    if c_configs:
        for i, cfg in enumerate(c_configs[:4]):
            w(f"**C.{i+1}**: {cfg['description']}")
    
    c_assignments = []
    for cfg in c_configs:
        try:
            wa = WuxingAssignment("C", cfg['trig_elem'], cfg['cycle'])
            c_assignments.append((cfg, wa))
        except Exception as e:
            pass
    
    w(f"\nValid C assignments built: {len(c_assignments)}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # Part 2: Discriminating test
    # ═══════════════════════════════════════════════════════════════════════
    
    w("\n## Part 2: 吉×生体 Discriminating Test\n")
    
    # Traditional
    print("Testing traditional assignment...")
    trad_result = test_textual_bridge(TRAD, bin_to_kw, yaoci)
    
    w("### Traditional (A)\n")
    w(f"- 生体 count: {trad_result['n_shengti']}")
    w(f"- 生体 吉 rate: {trad_result['shengti_ji_rate']:.3f} ({trad_result['shengti_ji_n']}/{trad_result['n_shengti']})")
    w(f"- Fisher (生体 vs rest, 吉): OR={trad_result['fisher_or']:.2f}, p={trad_result['fisher_p']:.4f}")
    w(f"- 比和 凶 rate: {trad_result['bihe_xiong_rate']:.3f}")
    w(f"- 克体 吉 rate: {trad_result['keti_ji_rate']:.3f}")
    w(f"- Relation distribution: {trad_result['rel_counts']}\n")
    
    # Full cross-tab for traditional
    w("**Full cross-tab (Traditional):**\n")
    all_markers_in_cross = sorted(set(m for rels in trad_result['cross'].values() for m in rels))
    w("| Relation | n |" + "|".join(f" {m} " for m in all_markers_in_cross) + "|")
    w("|----------|---|" + "|".join("---" for _ in all_markers_in_cross) + "|")
    for rel in TIYONG_CATEGORIES:
        n = trad_result['rel_counts'].get(rel, 0)
        counts = [trad_result['cross'].get(rel, {}).get(m, 0) for m in all_markers_in_cross]
        rates = [c/n if n > 0 else 0 for c in counts]
        w(f"| {rel} | {n} |" + "|".join(f" {c}({r:.2f}) " for c, r in zip(counts, rates)) + "|")
    w("")
    
    # Test all B assignments
    w("### Assignment B variants\n")
    print(f"Testing {len(b_assignments)} B assignments...")
    
    b_results = []
    for i, (cfg, wa) in enumerate(b_assignments):
        result = test_textual_bridge(wa, bin_to_kw, yaoci)
        result['config'] = cfg
        b_results.append(result)
    
    if b_results:
        w("| Variant | n(生体) | 生体 吉 rate | OR | p | 比和 凶 | 克体 吉 |")
        w("|---------|---------|-------------|-----|---|---------|---------|")
        for i, r in enumerate(b_results):
            w(f"| B.{i+1} | {r['n_shengti']} | {r['shengti_ji_rate']:.3f} | "
              f"{r['fisher_or']:.2f} | {r['fisher_p']:.4f} | "
              f"{r['bihe_xiong_rate']:.3f} | {r['keti_ji_rate']:.3f} |")
        w("")
        
        # Summary statistics
        ors = [r['fisher_or'] for r in b_results]
        ps = [r['fisher_p'] for r in b_results]
        w(f"B summary: OR range [{min(ors):.2f}, {max(ors):.2f}], "
          f"p range [{min(ps):.4f}, {max(ps):.4f}]")
        w(f"Any B with p < 0.05: {any(p < 0.05 for p in ps)}")
        w(f"Any B with OR > 1.5: {any(o > 1.5 for o in ors)}\n")
    
    # Test sample C assignments (there may be many)
    w("### Assignment C variants (sample)\n")
    n_c_test = min(len(c_assignments), 20)
    print(f"Testing {n_c_test} C assignments...")
    
    c_results = []
    for i, (cfg, wa) in enumerate(c_assignments[:n_c_test]):
        result = test_textual_bridge(wa, bin_to_kw, yaoci)
        result['config'] = cfg
        c_results.append(result)
    
    if c_results:
        w("| Variant | n(生体) | 生体 吉 rate | OR | p | 比和 凶 | 克体 吉 |")
        w("|---------|---------|-------------|-----|---|---------|---------|")
        for i, r in enumerate(c_results):
            w(f"| C.{i+1} | {r['n_shengti']} | {r['shengti_ji_rate']:.3f} | "
              f"{r['fisher_or']:.2f} | {r['fisher_p']:.4f} | "
              f"{r['bihe_xiong_rate']:.3f} | {r['keti_ji_rate']:.3f} |")
        w("")
        
        ors = [r['fisher_or'] for r in c_results]
        ps = [r['fisher_p'] for r in c_results]
        w(f"C summary: OR range [{min(ors):.2f}, {max(ors):.2f}], "
          f"p range [{min(ps):.4f}, {max(ps):.4f}]")
        w(f"Any C with p < 0.05: {any(p < 0.05 for p in ps)}")
        w(f"Any C with OR > 1.5: {any(o > 1.5 for o in ors)}\n")
    
    # ═══════════════════════════════════════════════════════════════════════
    # Comparison table
    # ═══════════════════════════════════════════════════════════════════════
    
    w("### Side-by-side comparison\n")
    w("| Metric | Traditional (A) | Best B | Best C |")
    w("|--------|----------------|--------|--------|")
    
    best_b = min(b_results, key=lambda r: r['fisher_p']) if b_results else None
    best_c = min(c_results, key=lambda r: r['fisher_p']) if c_results else None
    
    def fmt_or_na(val, fmt_str="{:.3f}"):
        return fmt_str.format(val) if val is not None else "N/A"
    
    rows = [
        ("生体 吉 rate", trad_result['shengti_ji_rate'],
         best_b['shengti_ji_rate'] if best_b else None,
         best_c['shengti_ji_rate'] if best_c else None),
        ("Fisher OR", trad_result['fisher_or'],
         best_b['fisher_or'] if best_b else None,
         best_c['fisher_or'] if best_c else None),
        ("Fisher p", trad_result['fisher_p'],
         best_b['fisher_p'] if best_b else None,
         best_c['fisher_p'] if best_c else None),
        ("比和 凶 rate", trad_result['bihe_xiong_rate'],
         best_b['bihe_xiong_rate'] if best_b else None,
         best_c['bihe_xiong_rate'] if best_c else None),
        ("克体 吉 rate", trad_result['keti_ji_rate'],
         best_b['keti_ji_rate'] if best_b else None,
         best_c['keti_ji_rate'] if best_c else None),
    ]
    for label, a_val, b_val, c_val in rows:
        w(f"| {label} | {fmt_or_na(a_val)} | {fmt_or_na(b_val)} | {fmt_or_na(c_val)} |")
    w("")
    
    # ═══════════════════════════════════════════════════════════════════════
    # Part 3: Structural checks
    # ═══════════════════════════════════════════════════════════════════════
    
    w("## Part 3: Structural Checks\n")
    
    assignments_to_test = [("Traditional (A)", TRAD)]
    if b_assignments:
        assignments_to_test.append(("B (first)", b_assignments[0][1]))
    if c_assignments:
        assignments_to_test.append(("C (first)", c_assignments[0][1]))
    
    # 3.1 Cycle attractor relations
    w("### 3.1 Cycle Attractor Relations (既濟/未濟)\n")
    w("| Assignment | 既濟 relation | 未濟 relation |")
    w("|------------|-------------|-------------|")
    for name, wa in assignments_to_test:
        jj, wj = test_cycle_attractors(wa)
        w(f"| {name} | {jj} | {wj} |")
    w("")
    
    # 3.2 Complement = negation
    w("### 3.2 Complement = Negation on Cycle Ring\n")
    w("| Assignment | π = -x mod 5 |")
    w("|------------|-------------|")
    for name, wa in assignments_to_test:
        w(f"| {name} | {wa.complement_is_negation()} |")
    w("")
    
    # 3.3 Zero residual
    w("### 3.3 Zero Residual (profile uniqueness)\n")
    w("| Assignment | Unique | Collisions | Max collision | Distinct profiles |")
    w("|------------|--------|------------|---------------|-------------------|")
    for name, wa in assignments_to_test:
        nu, nc, mc, dp = test_zero_residual(wa)
        w(f"| {name} | {nu}/64 | {nc} | {mc} | {dp} |")
    w("")
    
    # 3.4 互 well-definedness
    w("### 3.4 互 Well-Definedness (torus cells)\n")
    w("| Assignment | Well-defined | Total realized |")
    w("|------------|-------------|----------------|")
    for name, wa in assignments_to_test:
        wd, total = test_hu_welldefined(wa)
        w(f"| {name} | {wd}/{total} | {total}/25 |")
    w("")
    
    # 3.5 六親 injectivity
    w("### 3.5 六親 Injectivity\n")
    w("| Assignment | Unique words / 64 |")
    w("|------------|-------------------|")
    for name, wa in assignments_to_test:
        uniq = test_liuqin_injectivity(wa)
        w(f"| {name} | {uniq} |")
    w("")
    
    # 3.6 Parity separation
    w("### 3.6 Parity Separation (XOR masks)\n")
    w("| Assignment | Parity separated |")
    w("|------------|-----------------|")
    for name, wa in assignments_to_test:
        sep, info = check_parity_separation(wa)
        detail = ""
        if isinstance(info, dict):
            detail = f" (生-only parities: {info['sheng_parities']}, 克-only: {info['ke_parities']})"
        w(f"| {name} | {sep}{detail} |")
    w("")
    
    # ═══════════════════════════════════════════════════════════════════════
    # Part 4: He Tu verification
    # ═══════════════════════════════════════════════════════════════════════
    
    print("Computing Part 4: He Tu verification...")
    w(part4_hetu_verification())
    
    # ═══════════════════════════════════════════════════════════════════════
    # Part 5: 3×5 Grid
    # ═══════════════════════════════════════════════════════════════════════
    
    print("Computing Part 5: 3×5 grid...")
    w(part5_grid(TRAD, bin_to_kw, yaoci))
    
    # ═══════════════════════════════════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════════════════════════════════
    
    w("## Summary\n")
    w("### Predictions vs Results\n")
    w("| Prediction | Result |")
    w("|------------|--------|")
    
    # B loses textual bridge
    if b_results:
        b_any_sig = any(r['fisher_p'] < 0.05 for r in b_results)
        b_any_strong_or = any(r['fisher_or'] > 1.5 for r in b_results)
        w(f"| B loses 吉×生体 bridge | {'✓ Confirmed' if not b_any_sig else '✗ Some B variants retain signal'} "
          f"(best p={min(r['fisher_p'] for r in b_results):.4f}) |")
    
    # B loses cycle attractor 克
    if b_assignments:
        jj, wj = test_cycle_attractors(b_assignments[0][1])
        w(f"| B loses cycle attractor 克 | {'✓ Confirmed: '+jj+'/'+wj if jj != '克体' and jj != '体克用' else '✗: '+jj+'/'+wj} |")
    
    # C breaks complement closure
    if c_assignments:
        c_comp = c_assignments[0][1].complement_is_negation()
        w(f"| C breaks complement closure | {'✗ C still has complement=negation' if c_comp else '✓ Confirmed'} |")
    
    # Zero residual survives
    w(f"| Zero residual survives for all | Check table 3.3 above |")
    
    # Traditional unique
    trad_sig = trad_result['fisher_p'] < 0.05
    trad_comp = TRAD.complement_is_negation()
    w(f"| Traditional unique: textual + algebraic | Textual (p={trad_result['fisher_p']:.4f}): {'✓' if trad_sig else '✗'}, "
      f"Algebraic (π=-x): {'✓' if trad_comp else '✗'} |")
    w("")
    
    # Write output
    out_path = OUT_DIR / "01_results.md"
    out_path.write_text('\n'.join(md))
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    main()
