"""S4: Commentary Regex Extraction — structural parsing of 大象, 彖傳, 小象."""

import json
import re
import numpy as np
import requests
from pathlib import Path
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEXTS = Path(__file__).resolve().parent.parent.parent.parent / "texts" / "iching"
ATLAS = ROOT.parent / "atlas" / "atlas.json"

# Trigram name (from atlas) → image character
TRIGRAM_IMAGE = {
    "Qian": "天", "Kun": "地", "Zhen": "雷", "Xun": "風",
    "Kan": "水", "Li": "火", "Gen": "山", "Dui": "澤",
}
IMAGE_TO_TRIGRAM = {v: k for k, v in TRIGRAM_IMAGE.items()}

# 彖傳 target vocabulary
TUAN_VOCAB = {
    "剛柔": ["剛", "柔"],
    "position": ["得位", "失位", "不當位", "當位", "不正", "位", "中", "正"],
    "correspondence": ["不應", "應"],
    "movement": ["乘", "承", "往", "來", "進", "退"],
    "line_ref": ["初", "二", "三", "四", "五"],
}

# 小象 target vocabulary (ordered longest-first for overlap)
XIAOXIANG_VOCAB = [
    "不當位", "失位", "得位",
    "位", "中", "正", "當", "應",
    "上", "下", "剛", "柔",
    "志", "道", "義", "時",
]


def load_atlas():
    with open(ATLAS) as f:
        atlas = json.load(f)
    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}
    return atlas, kw_to_hexval


def parse_trigram_name(full_name: str) -> str:
    """'Qian ☰' → 'Qian'"""
    return full_name.split()[0]


# ─── III.1: 大象 ─────────────────────────────────────────────

def parse_daxiang(atlas, kw_to_hexval):
    with open(TEXTS / "xiangzhuan.json") as f:
        xiang = json.load(f)["entries"]

    trigram_images = set(TRIGRAM_IMAGE.values())
    spatial_words = {"上", "下", "中", "在"}

    results = []
    for entry in xiang:
        hv = kw_to_hexval[entry["number"]]
        text = entry["daxiang"]
        atlas_hex = atlas[str(hv)]

        # Extract trigram images present in text
        found_images = [img for img in trigram_images if img in text]

        # Extract spatial words
        found_spatial = [w for w in spatial_words if w in text]

        # Actual trigrams from atlas
        upper = parse_trigram_name(atlas_hex["upper_trigram"]["name"])
        lower = parse_trigram_name(atlas_hex["lower_trigram"]["name"])
        expected_images = {TRIGRAM_IMAGE.get(upper), TRIGRAM_IMAGE.get(lower)}

        # Check match
        trigrams_match = set(found_images) == expected_images

        # Classify relation type based on verb patterns
        # Extract the 君子以... / 先王以... / 后以... portion (moral action)
        moral_match = re.search(r'[君子先王后大人]以(.+)', text)
        moral_action = moral_match.group(1) if moral_match else ""

        # Relation type heuristic
        if any(w in text for w in ["在", "上", "下"]):
            relation_type = "spatial"
        elif any(w in text for w in ["行", "動", "流", "雷"]):
            relation_type = "dynamic"
        else:
            relation_type = "functional"

        results.append({
            "hex_val": hv,
            "kw_number": entry["number"],
            "name": entry["name"],
            "text": text,
            "trigram_images": found_images,
            "expected_images": list(expected_images),
            "trigrams_match_actual": trigrams_match,
            "spatial_words": found_spatial,
            "relation_type": relation_type,
            "moral_action": moral_action,
        })

    return results


# ─── III.2: 彖傳 ─────────────────────────────────────────────

def parse_tuanzhuan(kw_to_hexval):
    with open(TEXTS / "tuan.json") as f:
        tuan = json.load(f)["entries"]

    results = []
    freq_table = {}  # term → {hex_val: count}

    for entry in tuan:
        hv = kw_to_hexval[entry["number"]]
        text = entry["text"]
        terms_found = []

        for category, vocab in TUAN_VOCAB.items():
            # Sort by length descending for overlap handling
            for term in sorted(vocab, key=len, reverse=True):
                # Find all occurrences with context
                for m in re.finditer(re.escape(term), text):
                    start = max(0, m.start() - 5)
                    end = min(len(text), m.end() + 5)
                    context = text[start:end]
                    terms_found.append({
                        "term": term,
                        "category": category,
                        "context": context,
                        "position": m.start(),
                    })

                count = text.count(term)
                if count > 0:
                    freq_table.setdefault(term, {})[hv] = count

        results.append({
            "hex_val": hv,
            "kw_number": entry["number"],
            "name": entry["name"],
            "text": text,
            "terms": terms_found,
        })

    # Build frequency table as term × hexagram
    all_terms = sorted(freq_table.keys())
    freq_summary = {}
    for term in all_terms:
        total = sum(freq_table[term].values())
        n_hex = len(freq_table[term])
        freq_summary[term] = {"total": total, "n_hexagrams": n_hex}

    return results, freq_summary


# ─── III.3: 小象 ─────────────────────────────────────────────

def parse_xiaoxiang(kw_to_hexval):
    with open(TEXTS / "xiangzhuan.json") as f:
        xiang = json.load(f)["entries"]

    lines_data = []
    feature_matrix = []

    for entry in xiang:
        hv = kw_to_hexval[entry["number"]]
        xiaoxiang_list = entry["xiaoxiang"]

        # Take only first 6 (skip 用九/用六 extras)
        for j in range(min(6, len(xiaoxiang_list))):
            text = xiaoxiang_list[j]
            features = {}
            remaining = text

            # Extract target vocabulary (longest-first)
            for term in XIAOXIANG_VOCAB:
                count = remaining.count(term)
                features[term] = count
                if count > 0:
                    remaining = remaining.replace(term, "□" * len(term))

            binary = [1 if features[t] > 0 else 0 for t in XIAOXIANG_VOCAB]
            feature_matrix.append(binary)

            lines_data.append({
                "hex_val": hv,
                "kw_number": entry["number"],
                "name": entry["name"],
                "line": j,
                "text": text,
                "features": features,
            })

    feature_matrix = np.array(feature_matrix)

    # Positional bias: χ² test per feature
    positions = np.array([ld["line"] for ld in lines_data])
    pos_bias = {}
    for j, term in enumerate(XIAOXIANG_VOCAB):
        counts = np.zeros(6)
        for pos in range(6):
            counts[pos] = feature_matrix[positions == pos, j].sum()
        total = counts.sum()
        if total < 5:
            continue
        expected = np.full(6, total / 6)
        chi2, p = stats.chisquare(counts, expected)
        pos_bias[term] = {
            "counts_by_position": counts.tolist(),
            "total": int(total),
            "chi2": float(chi2),
            "p_value": float(p),
        }

    return lines_data, feature_matrix.tolist(), pos_bias


def main():
    atlas, kw_to_hexval = load_atlas()

    # ─── 大象 ───
    print("=" * 60)
    print("III.1: 大象 parsing")
    daxiang = parse_daxiang(atlas, kw_to_hexval)
    match_count = sum(1 for d in daxiang if d["trigrams_match_actual"])
    print(f"  {len(daxiang)} entries, {match_count}/{len(daxiang)} trigram images match actual")

    type_counts = {}
    for d in daxiang:
        type_counts[d["relation_type"]] = type_counts.get(d["relation_type"], 0) + 1
    print(f"  Relation types: {type_counts}")

    # Sample mismatches
    mismatches = [d for d in daxiang if not d["trigrams_match_actual"]]
    if mismatches:
        print(f"  Mismatches ({len(mismatches)}):")
        for m in mismatches[:5]:
            print(f"    {m['name']}: found={m['trigram_images']}, expected={m['expected_images']}, text={m['text'][:40]}")

    with open(DATA / "daxiang_relations.json", "w") as f:
        json.dump(daxiang, f, ensure_ascii=False, indent=2)

    # ─── 彖傳 ───
    print(f"\n{'='*60}")
    print("III.2: 彖傳 parsing")
    tuanzhuan, freq_summary = parse_tuanzhuan(kw_to_hexval)
    print(f"  {len(tuanzhuan)} entries")
    print(f"  Term frequencies:")
    for term, info in sorted(freq_summary.items(), key=lambda x: -x[1]["total"]):
        print(f"    {term}: {info['total']} total in {info['n_hexagrams']} hexagrams")

    with open(DATA / "tuanzhuan_structure.json", "w") as f:
        json.dump({"entries": tuanzhuan, "frequency_summary": freq_summary}, f, ensure_ascii=False, indent=2)

    # ─── 小象 ───
    print(f"\n{'='*60}")
    print("III.3: 小象 parsing")
    xiaoxiang_data, feat_matrix, pos_bias = parse_xiaoxiang(kw_to_hexval)
    print(f"  {len(xiaoxiang_data)} entries, {len(XIAOXIANG_VOCAB)} features")
    print(f"  Positional bias (p < 0.05):")
    for term, info in pos_bias.items():
        if info["p_value"] < 0.05:
            print(f"    {term}: χ²={info['chi2']:.1f} p={info['p_value']:.4f} counts={info['counts_by_position']}")

    with open(DATA / "xiaoxiang_vocab.json", "w") as f:
        json.dump({
            "entries": xiaoxiang_data,
            "feature_names": XIAOXIANG_VOCAB,
            "feature_matrix": feat_matrix,
            "positional_bias": pos_bias,
        }, f, ensure_ascii=False, indent=2)

    print(f"\nSaved: daxiang_relations.json, tuanzhuan_structure.json, xiaoxiang_vocab.json")


if __name__ == "__main__":
    main()
