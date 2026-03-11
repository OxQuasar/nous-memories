#!/usr/bin/env python3
"""
hexagram_wuxing.py — Hexagram-level 五行 relation algebra.

Tasks:
1. Z₅ × Z₅ hexagram relation matrix
2. 互 transition matrix in Z₅ language
3. P/H/Q parity vs Z₅ difference
4. 先天/後天 orderings and Z₅
5. Complement/reversal and Z₅
"""

from collections import Counter, defaultdict

# ═══════════════════════════════════════════════════════════
# Data: the 五行 map (complement-respecting surjection)
# ═══════════════════════════════════════════════════════════

# Encoding: b₂b₁b₀ where b₀ = bottom line
# 五行 map with Wood=0 in Z₅ (生-cycle numbering: Wood=0, Fire=1, Earth=2, Metal=3, Water=4)
WUXING_MAP = {
    0b000: 2,  # 坤 → Earth
    0b001: 0,  # 震 → Wood
    0b010: 4,  # 坎 → Water
    0b011: 3,  # 兌 → Metal
    0b100: 2,  # 艮 → Earth
    0b101: 1,  # 離 → Fire
    0b110: 0,  # 巽 → Wood
    0b111: 3,  # 乾 → Metal
}

ELEMENT_NAMES = {0: 'Wood', 1: 'Fire', 2: 'Earth', 3: 'Metal', 4: 'Water'}
TRIGRAM_NAMES = {
    0b000: '坤', 0b001: '震', 0b010: '坎', 0b011: '兌',
    0b100: '艮', 0b101: '離', 0b110: '巽', 0b111: '乾',
}

# 五行 relation by Z₅ difference (in 生-cycle: stride-1 = 生, stride-2 = 克)
RELATION_NAMES = {0: '同', 1: '生', 2: '克', 3: '被克', 4: '被生'}

# 先天八卦 (Fu Xi) circular ordering
XIANTIAN_ORDER = [0b111, 0b110, 0b101, 0b100, 0b000, 0b001, 0b010, 0b011]
# 後天八卦 (King Wen) circular ordering  
HOUTIAN_ORDER = [0b010, 0b100, 0b001, 0b110, 0b111, 0b011, 0b101, 0b000]


def f(x):
    """五行 map on trigrams."""
    return WUXING_MAP[x]


def nuclear(h):
    """互 (nuclear extraction) on hexagram h = (lower, upper) as 6-bit int.
    Lines: L₁L₂L₃L₄L₅L₆ where L₁ = bit 0 (bottom).
    Nuclear lower = L₂L₃L₄, nuclear upper = L₃L₄L₅.
    """
    L = [(h >> i) & 1 for i in range(6)]
    nuc_lower = (L[1]) | (L[2] << 1) | (L[3] << 2)
    nuc_upper = (L[2]) | (L[3] << 1) | (L[4] << 2)
    return nuc_lower | (nuc_upper << 3)


def hex_lower(h):
    return h & 0b111

def hex_upper(h):
    return (h >> 3) & 0b111

def hex_complement(h):
    return h ^ 0b111111

def hex_reversal(h):
    """Reverse line order: L₁L₂L₃L₄L₅L₆ → L₆L₅L₄L₃L₂L₁"""
    L = [(h >> i) & 1 for i in range(6)]
    return sum(L[5-i] << i for i in range(6))

def hex_d(h):
    """Z₅ difference: f(upper) - f(lower) mod 5."""
    return (f(hex_upper(h)) - f(hex_lower(h))) % 5

def P_parity(x):
    """P-parity of trigram: b₀ ⊕ b₁"""
    return ((x >> 0) & 1) ^ ((x >> 1) & 1)

def H_parity(x):
    """H-parity of trigram: b₁ ⊕ b₂"""
    return ((x >> 1) & 1) ^ ((x >> 2) & 1)

def Q_parity(x):
    """Q-parity of trigram: b₀ ⊕ b₂"""
    return ((x >> 0) & 1) ^ ((x >> 2) & 1)


# ═══════════════════════════════════════════════════════════
# Task 1: Z₅ × Z₅ hexagram relation matrix
# ═══════════════════════════════════════════════════════════

def task1(out):
    out.append("## Task 1: Z₅ × Z₅ Hexagram Relation Matrix")
    out.append("")
    
    # 8×8 difference matrix
    out.append("### 8×8 trigram-pair Z₅ difference matrix")
    out.append("")
    out.append("d = f(upper) − f(lower) mod 5.  Rows = lower trigram, Cols = upper trigram.")
    out.append("")
    
    header = "| Lower\\Upper |"
    for u in range(8):
        header += f" {TRIGRAM_NAMES[u]} |"
    out.append(header)
    out.append("|" + "---|" * 9)
    
    for lo in range(8):
        row = f"| **{TRIGRAM_NAMES[lo]}** ({ELEMENT_NAMES[f(lo)]}) |"
        for up in range(8):
            d = (f(up) - f(lo)) % 5
            row += f" {d}({RELATION_NAMES[d][0]}) |"
        out.append(row)
    out.append("")
    
    # Count relations
    rel_counts = Counter()
    for h in range(64):
        d = hex_d(h)
        rel_counts[d] += 1
    
    out.append("### Relation counts")
    out.append("")
    out.append("| d | Relation | Count | Fraction |")
    out.append("|---|----------|-------|----------|")
    for d in range(5):
        out.append(f"| {d} | {RELATION_NAMES[d]} | {rel_counts[d]} | {rel_counts[d]/64:.4f} |")
    out.append("")
    
    # Verify 同 count: self-pairs + same-element cross-pairs
    same_count = sum(1 for h in range(64) if f(hex_lower(h)) == f(hex_upper(h)))
    out.append(f"**同 count verification:** {same_count} = "
               f"8 (self-pairs) + 6 (cross: 2×C(2,2) for Wood,Earth,Metal + 0 for Fire,Water)")
    out.append(f"  Wood×Wood: 2×2=4, Earth×Earth: 2×2=4, Metal×Metal: 2×2=4, "
               f"Fire×Fire: 1, Water×Water: 1 → total = 14 ✓")
    out.append("")
    
    # Position vs orbit decomposition
    out.append("### d determined by position or orbit?")
    out.append("")
    out.append("The factored basis splits hexagram h into (pos, orb) where:")
    out.append("- pos = lower trigram (bits 0-2)")
    out.append("- orb = lower XOR upper = palindromic signature (bits 3-5 XOR bits 0-2)")
    out.append("")
    
    # For each hexagram, compute d and check if it depends on pos only, orb only, or both
    # d = f(upper) - f(lower) = f(lower XOR orb_mask) - f(lower)
    # Since f is non-linear, d depends on BOTH lower and the XOR mask
    
    # Demonstrate: same orbit, different d
    out.append("**Same orbit (XOR mask), different d?**")
    out.append("")
    examples = defaultdict(list)
    for h in range(64):
        lo, up = hex_lower(h), hex_upper(h)
        mask = lo ^ up
        d = hex_d(h)
        examples[mask].append((lo, up, d))
    
    for mask in sorted(examples.keys()):
        ds = set(d for _, _, d in examples[mask])
        if len(ds) > 1:
            out.append(f"  Mask {mask:03b}: d values = {sorted(ds)} "
                       f"(e.g., {TRIGRAM_NAMES[examples[mask][0][0]]}×{TRIGRAM_NAMES[examples[mask][0][1]]}→d={examples[mask][0][2]}, "
                       f"{TRIGRAM_NAMES[examples[mask][1][0]]}×{TRIGRAM_NAMES[examples[mask][1][1]]}→d={examples[mask][1][2]})")
    
    # Count how many masks give constant d
    const_masks = [(mask, list(ds)[0]) for mask in sorted(examples.keys()) 
                   if len(set(d for _, _, d in examples[mask])) == 1
                   for ds in [set(d for _, _, d in examples[mask])]]
    
    out.append("")
    out.append(f"**Masks with constant d (all lower trigrams give same relation):**")
    for mask, d_val in const_masks:
        out.append(f"  Mask {mask:03b} ({TRIGRAM_NAMES.get(mask, '???')}): always d={d_val} ({RELATION_NAMES[d_val]})")
    out.append("")
    
    var_masks = [mask for mask in sorted(examples.keys())
                 if len(set(d for _, _, d in examples[mask])) > 1]
    out.append(f"**Masks with variable d:** {len(var_masks)}/8")
    out.append(f"**Masks with constant d:** {len(const_masks)}/8")
    out.append("")
    out.append("**Conclusion:** d depends on BOTH the lower trigram and the XOR mask.")
    out.append("The 五行 relation is NOT determined by orbit alone (because f is non-linear).")
    out.append("Only mask=000 gives constant d=0 (同).")
    out.append("")


# ═══════════════════════════════════════════════════════════
# Task 2: 互 transition matrix in Z₅ perspective
# ═══════════════════════════════════════════════════════════

def task2(out):
    out.append("## Task 2: 五行 Relations Under 互 — Z₅ Perspective")
    out.append("")
    
    # Build transition matrix d(h) → d(互(h))
    transition = defaultdict(lambda: Counter())
    for h in range(64):
        d_orig = hex_d(h)
        nh = nuclear(h)
        d_nuc = hex_d(nh)
        transition[d_orig][d_nuc] += 1
    
    out.append("### Transition matrix: d(h) → d(互(h))")
    out.append("")
    header = "| d(h)\\d(互) |"
    for d2 in range(5):
        header += f" {d2}({RELATION_NAMES[d2]}) |"
    header += " Total |"
    out.append(header)
    out.append("|" + "---|" * 7)
    
    for d1 in range(5):
        row = f"| **{d1}({RELATION_NAMES[d1]})** |"
        for d2 in range(5):
            row += f" {transition[d1][d2]} |"
        row += f" {sum(transition[d1].values())} |"
        out.append(row)
    
    # Column totals
    row = "| **Nuclear** |"
    for d2 in range(5):
        col_total = sum(transition[d1][d2] for d1 in range(5))
        row += f" {col_total} |"
    row += " 64 |"
    out.append(row)
    out.append("")
    
    # Check if transition is a linear map on Z₅
    out.append("### Is d(互(h)) = c × d(h) mod 5?")
    out.append("")
    
    # For each hexagram, check d_nuc vs c*d_orig for each candidate c
    for c in range(5):
        matches = 0
        for h in range(64):
            d_orig = hex_d(h)
            d_nuc = hex_d(nuclear(h))
            if (c * d_orig) % 5 == d_nuc:
                matches += 1
        out.append(f"  c={c}: {matches}/64 match ({matches/64*100:.1f}%)")
    
    out.append("")
    out.append("**Conclusion:** No single constant c makes d(互(h)) = c·d(h) mod 5.")
    out.append("The nuclear map is NOT a Z₅-linear operation on the relation index.")
    out.append("")
    
    # What IS the structure?
    out.append("### Structure of the transition")
    out.append("")
    
    # Check: is d_nuc determined by (d_orig, some additional bit)?
    # Try: (d_orig, P-parity of lower)
    out.append("**Conditioning on P-parity of lower trigram:**")
    out.append("")
    
    for pval in [0, 1]:
        out.append(f"  P-parity = {pval}:")
        trans_p = defaultdict(lambda: Counter())
        count_p = 0
        for h in range(64):
            if P_parity(hex_lower(h)) != pval:
                continue
            count_p += 1
            d_orig = hex_d(h)
            d_nuc = hex_d(nuclear(h))
            trans_p[d_orig][d_nuc] += 1
        
        header = f"    | d(h)\\d(互) |"
        for d2 in range(5):
            header += f" {d2} |"
        out.append(header)
        out.append("    |" + "---|" * 6)
        for d1 in range(5):
            row = f"    | {d1} |"
            for d2 in range(5):
                row += f" {trans_p[d1][d2]} |"
            out.append(row)
        out.append(f"    ({count_p} hexagrams)")
        out.append("")
    
    # The key question: does the transition respect the Z₅ addition structure?
    # Check: d(互(h₁ ⊕ h₂)) vs d(互(h₁)) + d(互(h₂))
    # This tests whether the nuclear map is "Z₅-additive" on hexagrams
    out.append("### Transition matrix structure analysis")
    out.append("")
    
    # Check symmetries of the transition matrix
    out.append("**Symmetry check:**")
    for d1 in range(5):
        for d2 in range(5):
            neg_d1 = (-d1) % 5
            neg_d2 = (-d2) % 5
            if transition[d1][d2] != transition[neg_d1][neg_d2]:
                out.append(f"  T[{d1}][{d2}] = {transition[d1][d2]} ≠ "
                           f"T[{neg_d1}][{neg_d2}] = {transition[neg_d1][neg_d2]}")
    
    # Check: T[d][d'] = T[-d][-d'] (negation symmetry)
    neg_sym = all(transition[d1][d2] == transition[(-d1)%5][(-d2)%5]
                  for d1 in range(5) for d2 in range(5))
    out.append(f"  Negation symmetry T[d][d'] = T[-d][-d']: {'✓' if neg_sym else '✗'}")
    out.append("")
    
    # Verify against known matrix from framework_strengthening_findings.md
    # The known matrix (同=0, 生=1, 被生=4, 克=2, 被克=3):
    expected = {
        0: {0:6, 1:2, 2:2, 3:2, 4:2},
        1: {0:1, 1:2, 2:3, 3:6, 4:0},
        4: {0:1, 1:0, 2:6, 3:3, 4:2},
        2: {0:4, 1:0, 2:4, 3:5, 4:0},
        3: {0:4, 1:0, 2:5, 3:4, 4:0},
    }
    match = all(transition[d1][d2] == expected[d1][d2] 
                for d1 in range(5) for d2 in range(5))
    mstr = '✓ MATCH' if match else '✗ MISMATCH'
    out.append("**Cross-check with existing findings:**")
    out.append(f"  Same transition matrix as in framework_strengthening_findings.md: {mstr}")
    out.append("")


# ═══════════════════════════════════════════════════════════
# Task 3: P/H/Q parity vs Z₅ difference
# ═══════════════════════════════════════════════════════════

def task3(out):
    out.append("## Task 3: P/H/Q Parity vs Z₅ Difference")
    out.append("")
    
    parity_funcs = [('P', P_parity), ('H', H_parity), ('Q', Q_parity)]
    
    for pname, pfunc in parity_funcs:
        out.append(f"### {pname}-parity of lower trigram vs d")
        out.append("")
        
        table = defaultdict(lambda: Counter())
        for h in range(64):
            d = hex_d(h)
            pval = pfunc(hex_lower(h))
            table[d][pval] += 1
        
        out.append(f"| d | Relation | {pname}=0 | {pname}=1 | Total | {pname}=0 frac |")
        out.append("|---|----------|------|------|-------|-----------|")
        for d in range(5):
            t = table[d]
            total = t[0] + t[1]
            frac = t[0] / total if total > 0 else 0
            out.append(f"| {d} | {RELATION_NAMES[d]} | {t[0]} | {t[1]} | {total} | {frac:.4f} |")
        out.append("")
    
    # Restate P-parity theorem in Z₅ language
    out.append("### The P-parity theorem in Z₅ language")
    out.append("")
    out.append("**Note:** The tables above show P/H/Q-parity of the **lower trigram alone**,")
    out.append("which is approximately uniform. The meaningful quantity is P-parity of the")
    out.append("**XOR mask** (= P(lower) ⊕ P(upper)), which measures whether lower and upper")
    out.append("trigrams have the SAME P-parity. This is computed below.")
    out.append("")
    
    # Can we express this algebraically?
    out.append("### Algebraic relationship")
    out.append("")
    out.append("Is there a function g: Z₅ → Z₂ such that P-parity ≈ g(d)?")
    out.append("")
    
    # The P-parity of a hexagram depends on the LOWER trigram only
    # But d depends on both lower and upper
    # However, P-parity of the XOR mask (lower XOR upper) also matters
    # P(lower XOR upper) = P(lower) XOR P(upper)
    
    # Actually: P-parity of the difference relates to the mask parity
    # Let's check: for each d, what's the distribution of P(mask)?
    out.append("**P-parity of XOR mask vs d:**")
    out.append("")
    
    mask_parity_table = defaultdict(lambda: Counter())
    for h in range(64):
        d = hex_d(h)
        mask = hex_lower(h) ^ hex_upper(h)
        mp = P_parity(mask)
        mask_parity_table[d][mp] += 1
    
    out.append(f"| d | Relation | P(mask)=0 | P(mask)=1 | P(mask)=0 frac |")
    out.append("|---|----------|-----------|-----------|----------------|")
    for d in range(5):
        t = mask_parity_table[d]
        total = t[0] + t[1]
        frac = t[0] / total if total > 0 else 0
        out.append(f"| {d} | {RELATION_NAMES[d]} | {t[0]} | {t[1]} | {frac:.4f} |")
    out.append("")
    
    out.append("**Key insight:** P(mask) = P(lower) ⊕ P(upper), so P(mask)=0 means")
    out.append("lower and upper have the SAME P-parity. The 100% for 同 means")
    out.append("same-element trigrams always have the same P-parity — this is the")
    out.append("P-coset alignment theorem from synthesis-1.md.")
    out.append("")
    
    # The deeper connection: P(mask) relates to the 五行 relation because
    # the exclusive masks for each relation have specific P-parity:
    # 同: id(000)→P=0, 生: OM(011)→P=0, 克: M(010)→P=1, MI(110)→P=1
    out.append("**Connection to exclusive masks:**")
    out.append("")
    out.append("Each 五行 relation has exclusive XOR masks with fixed P-parity:")
    out.append("- 同 exclusive mask: id(000) → P(mask)=0")
    out.append("- 生 exclusive mask: OM(011) → P(mask)=0")  
    out.append("- 克 exclusive masks: M(010), MI(110) → P(mask)=1")
    out.append("")
    out.append("Non-exclusive masks dilute the relationship, which is why")
    out.append("同 is 100% P-even but 克 is only 92% P-odd (one exception).")
    out.append("")


# ═══════════════════════════════════════════════════════════
# Task 4: 先天/後天 orderings and Z₅
# ═══════════════════════════════════════════════════════════

def task4(out):
    out.append("## Task 4: 先天/後天 Orderings and Z₅ Relations")
    out.append("")
    
    for name, order in [("先天 (Fu Xi)", XIANTIAN_ORDER), ("後天 (King Wen)", HOUTIAN_ORDER)]:
        out.append(f"### {name} circular ordering")
        out.append("")
        
        # List trigrams in order with elements
        out.append("| Position | Trigram | Element (Z₅) |")
        out.append("|----------|--------|-------------|")
        for i, t in enumerate(order):
            out.append(f"| {i} | {TRIGRAM_NAMES[t]} ({t:03b}) | {ELEMENT_NAMES[f(t)]} ({f(t)}) |")
        out.append("")
        
        # Adjacent pairs and Z₅ differences
        out.append("| Step | From → To | d (fwd) | Relation | d (rev) | Relation |")
        out.append("|------|-----------|---------|----------|---------|----------|")
        d_fwd_counts = Counter()
        d_rev_counts = Counter()
        for i in range(8):
            a = order[i]
            b = order[(i + 1) % 8]
            d_fwd = (f(b) - f(a)) % 5
            d_rev = (f(a) - f(b)) % 5
            d_fwd_counts[d_fwd] += 1
            d_rev_counts[d_rev] += 1
            out.append(f"| {i}→{(i+1)%8} | {TRIGRAM_NAMES[a]}→{TRIGRAM_NAMES[b]} | "
                       f"{d_fwd} | {RELATION_NAMES[d_fwd]} | {d_rev} | {RELATION_NAMES[d_rev]} |")
        out.append("")
        
        out.append(f"Z₅ step multiset (forward): {dict(sorted(d_fwd_counts.items()))}")
        out.append("")
    
    # Compare multisets
    out.append("### Comparison of Z₅ step multisets")
    out.append("")
    
    xt_steps, ht_steps = Counter(), Counter()
    for i in range(8):
        xt_steps[(f(XIANTIAN_ORDER[(i+1)%8]) - f(XIANTIAN_ORDER[i])) % 5] += 1
        ht_steps[(f(HOUTIAN_ORDER[(i+1)%8]) - f(HOUTIAN_ORDER[i])) % 5] += 1
    
    out.append("| d | 先天 count | 後天 count |")
    out.append("|---|-----------|-----------|")
    for d in range(5):
        out.append(f"| {d} ({RELATION_NAMES[d]}) | {xt_steps[d]} | {ht_steps[d]} |")
    out.append("")
    
    same = xt_steps == ht_steps
    out.append(f"**Same multiset?** {'Yes' if same else 'No'}")
    out.append("")
    
    # 8×8 Z₅ matrix for 先天 hexagram arrangement
    out.append("### 先天 hexagram arrangement: Z₅ difference matrix")
    out.append("")
    out.append("Lower trigram = row (先天 order), Upper = column (先天 order).")
    out.append("Entry = d = f(upper) - f(lower) mod 5.")
    out.append("")
    
    header = "| |"
    for up in XIANTIAN_ORDER:
        header += f" {TRIGRAM_NAMES[up]} |"
    out.append(header)
    out.append("|" + "---|" * 9)
    
    for lo in XIANTIAN_ORDER:
        row = f"| **{TRIGRAM_NAMES[lo]}** |"
        for up in XIANTIAN_ORDER:
            d = (f(up) - f(lo)) % 5
            row += f" {d} |"
        out.append(row)
    out.append("")
    
    # Check diagonal patterns
    out.append("**Diagonal (同) entries:** main diagonal is always 0 (同). ✓")
    out.append("")
    
    # Anti-diagonal: in 先天, position i pairs with position 7-i (complements)
    out.append("**Anti-diagonal (complement pairs):**")
    for i in range(4):
        a = XIANTIAN_ORDER[i]
        b = XIANTIAN_ORDER[7-i]
        d = (f(b) - f(a)) % 5
        out.append(f"  {TRIGRAM_NAMES[a]}×{TRIGRAM_NAMES[b]}: d={d} ({RELATION_NAMES[d]})")
    out.append("")
    
    out.append("**Structural insight:** The 8×8 matrix is the 5×5 Z₅ Cayley subtraction table")
    out.append("expanded by fiber multiplicities. Same-element trigrams produce identical rows/columns:")
    out.append("- 乾 and 兌 (Metal): identical rows")
    out.append("- 巽 and 震 (Wood): identical rows")
    out.append("- 艮 and 坤 (Earth): identical rows")
    out.append("The collapsed 5×5 table is simply d_{ab} = b − a mod 5 — the Z₅ group operation.")
    out.append("")
    
    # 後天 step pattern insight
    out.append("### 後天 step pattern — 被克 dominance")
    out.append("")
    out.append("The 後天 arrangement has 4/8 steps with d=3 (被克 = reverse-克 = stride-3 on Z₅).")
    out.append("The 2 同-steps join same-element pairs (震/巽=Wood, 乾/兌=Metal).")
    out.append("The remaining 2 steps are d=1 (生) and d=2 (克).")
    out.append("The 先天 arrangement distributes steps more evenly across all five Z₅ values.")
    out.append("This asymmetry is a Z₅ signature of the 先天→後天 transition.")
    out.append("")


# ═══════════════════════════════════════════════════════════
# Task 5: Complement, reversal, KW pairing and Z₅
# ═══════════════════════════════════════════════════════════

def task5(out):
    out.append("## Task 5: Complement, Reversal, and Z₅")
    out.append("")
    
    # Complement: ~h flips all bits
    out.append("### Complement: d(~h) vs d(h)")
    out.append("")
    out.append("**Theorem.** d(~h) = −d(h) mod 5.")
    out.append("")
    out.append("*Proof.* ~h = (~lower, ~upper). By complement-respecting property,")
    out.append("f(~x) = −f(x) mod 5. So d(~h) = f(~upper) − f(~lower) = ")
    out.append("(−f(upper)) − (−f(lower)) = −(f(upper) − f(lower)) = −d(h). ∎")
    out.append("")
    
    # Verify
    complement_check = all(hex_d(hex_complement(h)) == (-hex_d(h)) % 5 for h in range(64))
    out.append(f"**Computational verification:** {'✓ ALL 64 match' if complement_check else '✗ FAIL'}")
    out.append("")
    
    out.append("**Consequence:** Complement maps 五行 relations as:")
    out.append("- 同 (d=0) → 同 (d=0): same relation preserved")
    out.append("- 生 (d=1) → 被生 (d=4): generation reverses")
    out.append("- 克 (d=2) → 被克 (d=3): conquest reverses")
    out.append("- 被克 (d=3) → 克 (d=2): conquest reverses")
    out.append("- 被生 (d=4) → 生 (d=1): generation reverses")
    out.append("")
    
    # Reversal: reverse line order
    out.append("### Reversal: d(h̄) vs d(h)")
    out.append("")
    out.append("**Claim.** d(h̄) = −d(h) mod 5 (same as complement).")
    out.append("")
    out.append("*Proof.* h̄ reverses L₁...L₆ → L₆...L₁. The lower trigram of h̄ is")
    out.append("the upper trigram of h (reversed), and vice versa. So")
    out.append("d(h̄) = f(lower(h)) − f(upper(h)) = −d(h). ∎")
    out.append("")
    
    reversal_check = all(hex_d(hex_reversal(h)) == (-hex_d(h)) % 5 for h in range(64))
    out.append(f"**Computational verification:** {'✓ ALL 64 match' if reversal_check else '✗ FAIL'}")
    out.append("")
    
    # Wait — does reversal actually swap lower and upper?
    # h = lower | (upper << 3), 6 bits = L₁L₂L₃L₄L₅L₆
    # h̄ = L₆L₅L₄L₃L₂L₁
    # lower(h̄) = L₆L₅L₄ (bits 0,1,2 of reversed)
    # upper(h̄) = L₃L₂L₁ (bits 3,4,5 of reversed)
    # But upper(h) = L₄L₅L₆ and lower(h) = L₁L₂L₃
    # So lower(h̄) = REVERSE of upper(h), upper(h̄) = REVERSE of lower(h)
    # f(reverse(x)) ≠ f(x) in general!
    # Let me re-verify more carefully
    
    out.append("**Wait — correction needed.** Reversal doesn't simply swap lower and upper.")
    out.append("It reverses the LINE order, so lower(h̄) = reverse(upper(h)) and")
    out.append("upper(h̄) = reverse(lower(h)). Since f is NOT reverse-invariant in general,")
    out.append("d(h̄) ≠ −d(h) in general.")
    out.append("")
    
    # Recheck properly
    reversal_neg_count = 0
    reversal_data = []
    for h in range(64):
        hr = hex_reversal(h)
        d_h = hex_d(h)
        d_hr = hex_d(hr)
        if d_hr == (-d_h) % 5:
            reversal_neg_count += 1
        reversal_data.append((h, d_h, d_hr, d_hr == (-d_h) % 5))
    
    out.append(f"**Proper verification:** d(h̄) = −d(h) in {reversal_neg_count}/64 cases")
    out.append("")
    
    if reversal_neg_count < 64:
        # Show counterexamples
        out.append("**Counterexamples (d(h̄) ≠ −d(h)):**")
        out.append("")
        out.append("| h | lower×upper | d(h) | h̄ | lower×upper | d(h̄) | −d(h) |")
        out.append("|---|------------|------|-----|------------|-------|-------|")
        count = 0
        for h, d_h, d_hr, match in reversal_data:
            if not match:
                lo, up = hex_lower(h), hex_upper(h)
                hr = hex_reversal(h)
                lo_r, up_r = hex_lower(hr), hex_upper(hr)
                out.append(f"| {h:06b} | {TRIGRAM_NAMES[lo]}×{TRIGRAM_NAMES[up]} | "
                           f"{d_h} | {hr:06b} | {TRIGRAM_NAMES[lo_r]}×{TRIGRAM_NAMES[up_r]} | "
                           f"{d_hr} | {(-d_h)%5} |")
                count += 1
                if count >= 10:
                    out.append("| ... | ... | ... | ... | ... | ... | ... |")
                    break
        out.append("")
    
    # What about reverse-complement (錯綜)?
    out.append("### Reverse-complement (錯綜): d(~h̄) vs d(h)")
    out.append("")
    
    rc_data = Counter()
    for h in range(64):
        hr = hex_reversal(h)
        hrc = hex_complement(hr)
        d_h = hex_d(h)
        d_hrc = hex_d(hrc)
        rc_data[(d_h, d_hrc)] += 1
    
    # Check: is d preserved?
    preserved = sum(v for (d1, d2), v in rc_data.items() if d1 == d2)
    out.append(f"d(~h̄) = d(h) in {preserved}/64 cases")
    out.append("")
    
    # KW pairing
    out.append("### King Wen pairing and Z₅")
    out.append("")
    out.append("KW pairs hexagrams by reversal (or complement for palindromes).")
    out.append("For each KW pair (h, h'), check d(h) vs d(h'):")
    out.append("")
    
    # Build KW pairs
    kw_pairs = []
    seen = set()
    for h in range(64):
        if h in seen:
            continue
        hr = hex_reversal(h)
        if hr == h:
            # Palindrome: pair with complement
            partner = hex_complement(h)
        else:
            partner = hr
        kw_pairs.append((h, partner))
        seen.add(h)
        seen.add(partner)
    
    # Analyze d relationship in KW pairs
    kw_d_rel = Counter()
    for h, hp in kw_pairs:
        d_h = hex_d(h)
        d_hp = hex_d(hp)
        rel = (d_hp - (-d_h)) % 5  # deviation from d' = -d
        kw_d_rel[((d_h + d_hp) % 5)] += 1
    
    neg_pairs = sum(1 for h, hp in kw_pairs if hex_d(hp) == (-hex_d(h)) % 5)
    
    out.append(f"**KW pairs where d(partner) = −d(h):** {neg_pairs}/{len(kw_pairs)}")
    out.append("")
    
    # For non-palindromes (paired by reversal), we already know d(h̄) situation
    pal_pairs = [(h, hp) for h, hp in kw_pairs if hex_reversal(h) == h]
    non_pal = [(h, hp) for h, hp in kw_pairs if hex_reversal(h) != h]
    
    out.append(f"  Non-palindrome pairs (reversal): {len(non_pal)}")
    non_pal_neg = sum(1 for h, hp in non_pal if hex_d(hp) == (-hex_d(h)) % 5)
    out.append(f"    d(h̄) = −d(h): {non_pal_neg}/{len(non_pal)}")
    
    out.append(f"  Palindrome pairs (complement): {len(pal_pairs)}")
    pal_neg = sum(1 for h, hp in pal_pairs if hex_d(hp) == (-hex_d(h)) % 5)
    out.append(f"    d(~h) = −d(h): {pal_neg}/{len(pal_pairs)} (should be 100%)")
    out.append("")
    
    # Detailed analysis for reversal pairs
    out.append("### Reversal and the 五行 map")
    out.append("")
    out.append("For a trigram x = b₂b₁b₀, its reversal is x̃ = b₀b₁b₂.")
    out.append("The 五行 map of reversed trigrams:")
    out.append("")
    out.append("| x | x̃ | f(x) | f(x̃) | f(x̃)−f(x) mod 5 |")
    out.append("|---|---|------|------|-----------------|")
    for x in range(8):
        bits = [(x >> i) & 1 for i in range(3)]
        xr = bits[2] | (bits[1] << 1) | (bits[0] << 2)
        diff = (f(xr) - f(x)) % 5
        out.append(f"| {TRIGRAM_NAMES[x]}({x:03b}) | {TRIGRAM_NAMES[xr]}({xr:03b}) | "
                   f"{f(x)}({ELEMENT_NAMES[f(x)]}) | {f(xr)}({ELEMENT_NAMES[f(xr)]}) | {diff} |")
    out.append("")
    
    # Count palindromic trigrams (where reversal = self)
    palindromes = [x for x in range(8) if x == (((x>>2)&1) | (((x>>1)&1)<<1) | ((x&1)<<2))]
    out.append(f"**Palindromic trigrams** (x = x̃): {[TRIGRAM_NAMES[x] for x in palindromes]}")
    seen2 = set()
    np_pairs = []
    for x in range(8):
        bits = [(x >> i) & 1 for i in range(3)]
        xr = bits[2] | (bits[1] << 1) | (bits[0] << 2)
        if x != xr and x not in seen2:
            np_pairs.append((x, xr))
            seen2.add(x); seen2.add(xr)
    out.append(f"**Non-palindromic pairs:** {[(TRIGRAM_NAMES[a], TRIGRAM_NAMES[b]) for a, b in np_pairs]}")
    out.append("")
    
    # Key finding: reversal acts on Z₅ as a SPECIFIC permutation, not just negation
    out.append("**Reversal permutation on Z₅:**")
    rev_perm = {}
    for x in range(8):
        bits = [(x >> i) & 1 for i in range(3)]
        xr = bits[2] | (bits[1] << 1) | (bits[0] << 2)
        rev_perm[f(x)] = f(xr)
    # This isn't well-defined if f isn't injective — check
    rev_perm_multi = defaultdict(set)
    for x in range(8):
        bits = [(x >> i) & 1 for i in range(3)]
        xr = bits[2] | (bits[1] << 1) | (bits[0] << 2)
        rev_perm_multi[f(x)].add(f(xr))
    out.append(f"  f(x) → f(x̃) images: {dict((ELEMENT_NAMES[k], {ELEMENT_NAMES[v] for v in vs}) for k, vs in rev_perm_multi.items())}")
    out.append("")
    
    # Check: is reversal-on-五行 a well-defined permutation?
    well_defined = all(len(vs) == 1 for vs in rev_perm_multi.values())
    out.append(f"  **Well-defined permutation on Z₅?** {'Yes' if well_defined else 'No — reversal mixes elements'}")
    out.append("")
    
    if not well_defined:
        out.append("  This means trigram reversal does NOT induce a function on Z₅.")
        out.append("  For doubleton fibers, reversal may send the two trigrams to")
        out.append("  DIFFERENT elements. This is why d(h̄) ≠ −d(h) in general.")
        out.append("")
        
        # Show which fibers are split
        out.append("  **Fiber-splitting by reversal:**")
        for elem in range(5):
            fiber = [x for x in range(8) if f(x) == elem]
            rev_images = []
            for x in fiber:
                bits = [(x >> i) & 1 for i in range(3)]
                xr = bits[2] | (bits[1] << 1) | (bits[0] << 2)
                rev_images.append(f(xr))
            split = len(set(rev_images)) > 1
            out.append(f"    {ELEMENT_NAMES[elem]}: {[TRIGRAM_NAMES[x] for x in fiber]} "
                       f"→ {[ELEMENT_NAMES[v] for v in rev_images]} "
                       f"{'(SPLIT!)' if split else '(preserved)'}")
        out.append("")


# ═══════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════

def main():
    out = []
    out.append("# Hexagram 五行 Relation Algebra: Complete Results")
    out.append("")
    out.append("All analysis uses the complement-respecting 五行 surjection with Wood=0 in Z₅")
    out.append("(生-cycle numbering: Wood=0, Fire=1, Earth=2, Metal=3, Water=4).")
    out.append("d = f(upper) − f(lower) mod 5 determines the 五行 relation.")
    out.append("")
    out.append("---")
    out.append("")
    
    task1(out)
    out.append("---")
    out.append("")
    task2(out)
    out.append("---")
    out.append("")
    task3(out)
    out.append("---")
    out.append("")
    task4(out)
    out.append("---")
    out.append("")
    task5(out)
    
    # Final synthesis
    out.append("---")
    out.append("")
    out.append("## Synthesis: What the Z₅ Language Reveals")
    out.append("")
    out.append("### 1. The 五行 relation d is genuinely non-linear")
    out.append("d depends on both the lower trigram and the XOR mask (orbit).")
    out.append("Only mask=000 gives constant d=0. The non-linearity of the 五行 map")
    out.append("prevents d from being an orbit-only quantity.")
    out.append("")
    out.append("### 2. The 互 transition is NOT Z₅-linear but concentrates onto {0,2,3}")
    out.append("No constant c makes d(互(h)) = c·d(h) mod 5. The transition")
    out.append("matrix has negation symmetry T[d][d'] = T[−d][−d'] (from complement")
    out.append("equivariance) but is otherwise non-algebraic on Z₅.")
    out.append("However, 互 strongly concentrates the output: nuclear d lands in")
    out.append("{0,2,3} = {同,克,被克} with probability 56/64 = 87.5%, while")
    out.append("{1,4} = {生,被生} receive only 8/64 = 12.5%. This is the 克 amplification")
    out.append("(1.538×) restated in Z₅ language: 互 maps the relation space toward the")
    out.append("克/被克 axis (stride-2 on Z₅) and away from the 生/被生 axis (stride-1).")
    out.append("")
    out.append("### 3. P-parity is the Z₅ shadow of the F₂ structure")
    out.append("The P-parity theorem (同=100% P-even, 克=92% P-odd) is")
    out.append("the nearest thing to a Z₅→Z₂ homomorphism: d mod 2 approximately")
    out.append("determines P(mask). The exclusive masks explain the exact distribution.")
    out.append("")
    out.append("### 4. Complement negates d; reversal does NOT")
    out.append("Complement is a clean Z₅ operation (d → −d) because f(~x) = -f(x).")
    out.append("Reversal splits doubleton fibers: 震(Wood)↔艮(Earth) and 兌(Metal)↔巽(Wood)")
    out.append("swap elements under reversal. Only palindromic trigrams (坤,坎,離,乾) and")
    out.append("singletons (坎,離) are preserved. This means reversal does NOT induce a")
    out.append("function on Z₅, and d(h̄) = −d(h) holds in only 24/64 cases.")
    out.append("This is the precise algebraic statement of the synthesis-1 result that")
    out.append("complement descends to Z₅ but reversal does not.")
    out.append("")
    out.append("### 5. The KW pairing lives at the reversal/complement boundary")
    out.append("KW pairs non-palindromes by reversal (NOT Z₅-clean) and palindromes")
    out.append("by complement (Z₅-clean). The 4 palindrome pairs have d → −d exactly.")
    out.append("The 28 reversal pairs break this: d(h̄) ≠ −d(h) in general,")
    out.append("because the 五行 map is not reversal-invariant.")
    out.append("")
    
    path = "/home/quasar/nous/memories/iching/unification/hexagram_wuxing_results.md"
    with open(path, 'w') as fout:
        fout.write('\n'.join(out))
    print(f"Results written to {path}")
    print(f"Lines: {len(out)}")


if __name__ == '__main__':
    main()
