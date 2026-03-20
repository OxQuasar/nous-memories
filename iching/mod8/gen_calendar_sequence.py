"""
Generate the complete 梅花 calendar cycle: 8 day-residues × 12 hours = 96 readings.

Formula:
  upper_pos = (Y+M+D) mod 8,       0→8
  lower_pos = (Y+M+D+H) mod 8,     0→8
  moving_line = (Y+M+D+H) mod 6,   0→6

先天 ordering: 1=乾,2=兌,3=離,4=震,5=巽,6=坎,7=艮,8=坤
"""
import json

# 先天 position → (name, binary, element, element_z5)
XIANTIAN = {
    1: ("乾", "111", "金", 3),
    2: ("兌", "011", "金", 3),
    3: ("離", "101", "火", 1),
    4: ("震", "001", "木", 0),
    5: ("巽", "110", "木", 0),
    6: ("坎", "010", "水", 4),
    7: ("艮", "100", "土", 2),
    8: ("坤", "000", "土", 2),
}

# Z₅ relation: d = (用_z5 - 体_z5) mod 5
RELATION_NAMES = {
    0: "比和",
    1: "体生用",
    2: "体克用",
    3: "用克体",
    4: "用生体",
}

UNDIRECTED = {
    0: "比和",
    1: "生",
    2: "克",
    3: "克",
    4: "生",
}

FAVORABLE = {
    0: True,   # 比和
    1: False,  # 体生用 (drain)
    2: True,   # 体克用 (overcome)
    3: False,  # 用克体 (overwhelmed)
    4: True,   # 用生体 (nourished)
}

def mod_nonzero(n, m):
    """mod with 0 → m (梅花 convention)"""
    r = n % m
    return m if r == 0 else r

sequence = []

for day_residue in range(8):  # D mod 8 = 0..7
    upper_pos = mod_nonzero(day_residue, 8)  # 0→8
    up = XIANTIAN[upper_pos]
    
    for hour in range(1, 13):  # H = 1..12
        S = day_residue + hour
        lower_pos = mod_nonzero(S, 8)
        moving_line = mod_nonzero(S, 6)
        lo = XIANTIAN[lower_pos]
        
        # 体/用 assignment: moving line in lower (1-3) → upper=体; in upper (4-6) → lower=体
        if moving_line <= 3:
            ti_name, ti_elem, ti_z5 = up[0], up[2], up[3]
            yong_name, yong_elem, yong_z5 = lo[0], lo[2], lo[3]
            ti_pos = "upper"
        else:
            ti_name, ti_elem, ti_z5 = lo[0], lo[2], lo[3]
            yong_name, yong_elem, yong_z5 = up[0], up[2], up[3]
            ti_pos = "lower"
        
        d = (yong_z5 - ti_z5) % 5
        
        # Q₃ properties
        up_bits = [int(b) for b in up[1]]
        lo_bits = [int(b) for b in lo[1]]
        xor_bits = [a ^ b for a, b in zip(up_bits, lo_bits)]
        hamming = sum(xor_bits)
        is_q3_edge = hamming == 1
        if is_q3_edge:
            string_idx = xor_bits.index(1)
            # String is "top-mid-bot" = [b₂, b₁, b₀]. Convert to Convention A bit index.
            bit_index = 2 - string_idx
            bit_layer = f"bit₀" if bit_index == 0 else f"bit₁" if bit_index == 1 else f"bit₂"
        else:
            bit_layer = None
        
        entry = {
            "day_residue": day_residue,
            "hour": hour,
            "shift": hour % 8 if hour % 8 != 0 else 8,
            "upper": {
                "position": upper_pos,
                "name": up[0],
                "binary": up[1],
                "element": up[2],
            },
            "lower": {
                "position": lower_pos,
                "name": lo[0],
                "binary": lo[1],
                "element": lo[2],
            },
            "moving_line": moving_line,
            "ti": {
                "name": ti_name,
                "element": ti_elem,
                "position": ti_pos,
            },
            "yong": {
                "name": yong_name,
                "element": yong_elem,
            },
            "relation": {
                "directed": RELATION_NAMES[d],
                "undirected": UNDIRECTED[d],
                "favorable": FAVORABLE[d],
                "z5_distance": d if d <= 2 else 5 - d,
            },
            "q3": {
                "hamming_distance": hamming,
                "is_edge": is_q3_edge,
                "xor_mask": "".join(str(b) for b in xor_bits),
                "bit_layer": bit_layer,
            },
        }
        sequence.append(entry)

# Summary statistics
total = len(sequence)
favorable_count = sum(1 for e in sequence if e["relation"]["favorable"])
type_counts = {}
directed_counts = {}
for e in sequence:
    t = e["relation"]["undirected"]
    type_counts[t] = type_counts.get(t, 0) + 1
    d = e["relation"]["directed"]
    directed_counts[d] = directed_counts.get(d, 0) + 1

q3_edge_count = sum(1 for e in sequence if e["q3"]["is_edge"])
q3_edge_ke = sum(1 for e in sequence if e["q3"]["is_edge"] and e["relation"]["undirected"] == "克")

output = {
    "description": "Complete 梅花 calendar cycle: 8 day-residues × 12 hours = 96 readings",
    "formula": {
        "upper": "(Y+M+D) mod 8, 0→8",
        "lower": "(Y+M+D+H) mod 8, 0→8",
        "moving_line": "(Y+M+D+H) mod 6, 0→6",
    },
    "bit_convention": "A: b₀=bottom(bit2 in string), b₂=top(bit0 in string). Binary strings written top-mid-bot.",
    "xiantian_map": {str(k): {"name": v[0], "binary": v[1], "element": v[2]} for k, v in XIANTIAN.items()},
    "summary": {
        "total_readings": total,
        "favorable": favorable_count,
        "unfavorable": total - favorable_count,
        "favorable_pct": round(favorable_count / total * 100, 2),
        "undirected_counts": type_counts,
        "directed_counts": directed_counts,
        "q3_edges": q3_edge_count,
        "q3_edge_ke_count": q3_edge_ke,
    },
    "sequence": sequence,
}

with open("/home/quasar/nous/memories/iching/mod8/mh-calendar-sequence.json", "w") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Generated {total} readings")
print(f"Favorable: {favorable_count}/{total} ({favorable_count/total*100:.1f}%)")
print(f"Undirected: {type_counts}")
print(f"Directed: {directed_counts}")
print(f"Q₃ edges: {q3_edge_count}, of which 克: {q3_edge_ke}")

# Print the path for day_residue=0 as a quick check
print("\n=== Day residue 0 (upper=坤), 12 hours ===")
for e in sequence[:12]:
    r = e["relation"]
    q = e["q3"]
    print(f"  H={e['hour']:2d}  {e['upper']['name']}({e['upper']['element']}) / {e['lower']['name']}({e['lower']['element']})  "
          f"line={e['moving_line']}  体={e['ti']['position']}  "
          f"{r['directed']:4s}  {'✓' if r['favorable'] else '✗'}  "
          f"H={q['hamming_distance']} {'Q₃' if q['is_edge'] else '  '} {q['xor_mask']}")
