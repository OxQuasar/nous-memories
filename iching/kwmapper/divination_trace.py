"""
Trace a complete divination (本→互→变) through S₄/Z₂³ spaces.
Track what happens at each stage in both trigram spaces.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/memories/iching/kwmapper')

from common import *
from cycle_algebra import (
    hamming3, fmt3, fmt6, bit,
    tiyong_relation, tiyong_trigrams,
)

def trace_divination(hex_val, moving_line, hex_name=""):
    """Full divination trace through algebraic spaces."""
    
    ben = hex_val
    hu = hugua(ben)
    bian = ben ^ (1 << (moving_line - 1))  # flip the moving line (1-indexed)
    
    print(f"\n{'═' * 70}")
    print(f"  DIVINATION: {hex_name} #{KW_NUMBERS[KW_HEX.index(ben)] if ben in KW_HEX else '?'}, "
          f"line {moving_line} moving")
    print(f"{'═' * 70}")
    
    for label, h in [("Ben (manifest)", ben), ("Hu (hidden)", hu), ("Bian (transform)", bian)]:
        lo = lower_trigram(h)
        up = upper_trigram(h)
        lo_name = TRIGRAM_NAMES[lo]
        up_name = TRIGRAM_NAMES[up]
        lo_elem = TRIGRAM_ELEMENT[lo]
        up_elem = TRIGRAM_ELEMENT[up]
        
        inner = (h >> 1) & 0xF
        basin = get_basin(h)
        h1, h2, h3, h4 = bit(h,1), bit(h,2), bit(h,3), bit(h,4)
        
        hu_h = hugua(h)
        hu_lo = lower_trigram(hu_h)
        hu_up = upper_trigram(hu_h)
        
        print(f"\n  {label}: {fmt6(h)}")
        print(f"    Outer:  {lo_name} ({lo_elem}) / {up_name} ({up_elem})")
        print(f"    Inner:  ({h1},{h2},{h3},{h4}) = {format(inner, '04b')}  Basin: {BASIN_NAME[basin]}")
        print(f"    Hu:     {TRIGRAM_NAMES[hu_lo]} ({TRIGRAM_ELEMENT[hu_lo]}) / "
              f"{TRIGRAM_NAMES[hu_up]} ({TRIGRAM_ELEMENT[hu_up]})")
    
    # ── Transitions ──────────────────────────────────────────────────────
    
    print(f"\n  {'─' * 60}")
    print(f"  TRANSITIONS IN S₄ / Z₂³")
    print(f"  {'─' * 60}")
    
    transitions = [
        ("Ben → Hu", ben, hu),
        ("Ben → Bian", ben, bian),
        ("Hu → Bian", hu, bian),
    ]
    
    for label, h1, h2 in transitions:
        xor = h1 ^ h2
        kernel = mirror_kernel(xor)
        kname = KERNEL_NAMES[kernel]
        in_H = kernel in H_KERNELS
        I_comp = kernel[2]
        
        lo1, up1 = lower_trigram(h1), upper_trigram(h1)
        lo2, up2 = lower_trigram(h2), upper_trigram(h2)
        
        # Five-phase on outer trigrams
        lo_rel = trig_phase(lo1, lo2)
        up_rel = trig_phase(up1, up2)
        lo_pc = phase_class(lo_rel)
        up_pc = phase_class(up_rel)
        
        # Five-phase on 互 trigrams
        hu1, hu2 = hugua(h1), hugua(h2)
        hu_lo1, hu_up1 = lower_trigram(hu1), upper_trigram(hu1)
        hu_lo2, hu_up2 = lower_trigram(hu2), upper_trigram(hu2)
        
        hu_lo_rel = trig_phase(hu_lo1, hu_lo2)
        hu_up_rel = trig_phase(hu_up1, hu_up2)
        hu_lo_pc = phase_class(hu_lo_rel)
        hu_up_pc = phase_class(hu_up_rel)
        
        # Basin transition
        b1 = get_basin(h1)
        b2 = get_basin(h2)
        
        # Inner bit change
        inner1 = (h1 >> 1) & 0xF
        inner2 = (h2 >> 1) & 0xF
        outer1 = (h1 & 1) | (((h1 >> 5) & 1) << 1)
        outer2 = (h2 & 1) | (((h2 >> 5) & 1) << 1)
        
        print(f"\n  {label}:")
        print(f"    XOR: {fmt6(xor)}  Kernel: {kname}  H: {'yes' if in_H else 'NO'}  I: {I_comp}")
        print(f"    Basin: {BASIN_NAME[b1]} → {BASIN_NAME[b2]}  "
              f"{'(preserved)' if b1 == b2 else '** CROSSING **'}")
        print(f"    Inner: {format(inner1,'04b')} → {format(inner2,'04b')}  "
              f"Outer: {format(outer1,'02b')} → {format(outer2,'02b')}")
        
        print(f"    Outer trigrams:")
        print(f"      Lower: {TRIGRAM_NAMES[lo1]}({TRIGRAM_ELEMENT[lo1]}) → "
              f"{TRIGRAM_NAMES[lo2]}({TRIGRAM_ELEMENT[lo2]})  {lo_rel} [{lo_pc}]")
        print(f"      Upper: {TRIGRAM_NAMES[up1]}({TRIGRAM_ELEMENT[up1]}) → "
              f"{TRIGRAM_NAMES[up2]}({TRIGRAM_ELEMENT[up2]})  {up_rel} [{up_pc}]")
        
        print(f"    Hu trigrams:")
        print(f"      Lower: {TRIGRAM_NAMES[hu_lo1]}({TRIGRAM_ELEMENT[hu_lo1]}) → "
              f"{TRIGRAM_NAMES[hu_lo2]}({TRIGRAM_ELEMENT[hu_lo2]})  {hu_lo_rel} [{hu_lo_pc}]")
        print(f"      Upper: {TRIGRAM_NAMES[hu_up1]}({TRIGRAM_ELEMENT[hu_up1]}) → "
              f"{TRIGRAM_NAMES[hu_up2]}({TRIGRAM_ELEMENT[hu_up2]})  {hu_up_rel} [{hu_up_pc}]")
    
    # ── Ti/Yong reading ──────────────────────────────────────────────────
    
    print(f"\n  {'─' * 60}")
    print(f"  TI/YONG READING (line {moving_line})")
    print(f"  {'─' * 60}")
    
    ti_trig, yong_trig = tiyong_trigrams(ben, moving_line)
    ti_elem = TRIGRAM_ELEMENT[ti_trig]
    yong_elem = TRIGRAM_ELEMENT[yong_trig]
    relation = tiyong_relation(ben, moving_line)
    
    which_ti = "upper" if moving_line <= 3 else "lower"
    which_yong = "lower" if moving_line <= 3 else "upper"
    
    print(f"    Line {moving_line} in {'lower' if moving_line <= 3 else 'upper'} trigram")
    print(f"    Ti (body):  {which_ti} = {TRIGRAM_NAMES[ti_trig]} ({ti_elem})")
    print(f"    Yong (use): {which_yong} = {TRIGRAM_NAMES[yong_trig]} ({yong_elem})")
    print(f"    Relation: {relation}")
    
    # ── Interpretation ───────────────────────────────────────────────────
    
    print(f"\n  {'─' * 60}")
    print(f"  ALGEBRAIC INTERPRETATION")
    print(f"  {'─' * 60}")
    
    # Ben → Hu
    ben_hu_kernel = mirror_kernel(ben ^ hu)
    print(f"\n    Ben→Hu: kernel={KERNEL_NAMES[ben_hu_kernel]} (I=0 always, O/M free)")
    print(f"      I=0 forced: XOR bits 2,3 identical → interface never breaks.")
    print(f"      Basin preserved: {BASIN_NAME[get_basin(ben)]} → {BASIN_NAME[get_basin(hu)]}")
    
    # Ben → Bian  
    ben_bian_kernel = mirror_kernel(ben ^ bian)
    ben_bian_I = ben_bian_kernel[2]
    print(f"\n    Ben→Bian: kernel={KERNEL_NAMES[ben_bian_kernel]}  I={ben_bian_I}")
    if ben_bian_I == 0:
        print(f"      I=0: interface preserved. Basin stays {BASIN_NAME[get_basin(ben)]}.")
        print(f"      The transformation is harmonious — sheng/bi territory.")
    else:
        print(f"      I=1: interface broken. Basin may cross.")
        b_ben = get_basin(ben)
        b_bian = get_basin(bian)
        if b_ben != b_bian:
            print(f"      Basin CROSSES: {BASIN_NAME[b_ben]} → {BASIN_NAME[b_bian]}")
            print(f"      The transformation enters destructive territory (ke).")
        else:
            print(f"      Basin preserved despite I=1 (interface bits swapped but stayed mixed).")

# ══════════════════════════════════════════════════════════════════════════════
# EXAMPLES
# ══════════════════════════════════════════════════════════════════════════════

# Example 1: Tai (Peace) #11, line 5 moving
# Tai = Qian below, Kun above
tai = 0b000111  # bits: 1,1,1,0,0,0
trace_divination(tai, 5, "Tai (Peace)")

# Example 2: Kan (Water) #29, line 3 moving  
# Kan = Kan below, Kan above
kan = 0b010010
trace_divination(kan, 3, "Kan (Danger)")

# Example 3: Ji Ji (Completion) #63, line 2 moving
# Ji Ji = Li below, Kan above = 101 010
jiji = 0b010101
trace_divination(jiji, 2, "Ji Ji (Completion)")

# Example 4: A basin-crossing case — Qian #1, line 3 moving
# Qian = 111111, flip bit 2 → 111011
qian = 0b111111
trace_divination(qian, 3, "Qian (Creative)")

print(f"\n{'═' * 70}")
print("DONE")
print(f"{'═' * 70}")
