"""S8: 大象 Bridge Test — does 大象 operate in imagistic, elemental, or both registers?"""

import json
import numpy as np
from pathlib import Path
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ATLAS_PATH = ROOT.parent / "atlas" / "atlas.json"

# Trigram → element mapping (from atlas)
TRIGRAM_ELEMENT = {
    "Qian": "Metal", "Kun": "Earth", "Zhen": "Wood", "Xun": "Wood",
    "Kan": "Water", "Li": "Fire", "Gen": "Earth", "Dui": "Metal",
}

# Image character → trigram name
IMAGE_TRIGRAM = {
    "天": "Qian", "地": "Kun", "雷": "Zhen", "風": "Xun",
    "水": "Kan", "火": "Li", "山": "Gen", "澤": "Dui",
}

# Secondary images (from S4 mismatches)
SECONDARY_IMAGE = {
    "雲": "Kan",   # clouds = water
    "泉": "Kan",   # spring = water
    "電": "Li",    # lightning = fire
    "木": "Xun",   # wood = wind/wood
}

# 五行 vocabulary to search for
WUXING_VOCAB = ["五行", "相生", "相克", "金", "木", "水", "火", "土", "生", "克"]


def parse_trigram_name(full_name: str) -> str:
    return full_name.split()[0]


def main():
    with open(DATA / "daxiang_relations.json") as f:
        daxiang = json.load(f)
    with open(ATLAS_PATH) as f:
        atlas = json.load(f)

    kw_to_hexval = {v["kw_number"]: int(k) for k, v in atlas.items()}

    # ── Test 1: relation_type × surface_relation ──
    print("=" * 60)
    print("Test 1: Relation type × Surface relation")
    print("=" * 60)

    rel_types = sorted(set(d["relation_type"] for d in daxiang))
    surf_rels = sorted(set(atlas[str(d["hex_val"])]["surface_relation"] for d in daxiang))

    ct = np.zeros((len(rel_types), len(surf_rels)), dtype=int)
    for d in daxiang:
        sr = atlas[str(d["hex_val"])]["surface_relation"]
        rt = d["relation_type"]
        ct[rel_types.index(rt), surf_rels.index(sr)] += 1

    print(f"\n  {'':12s} " + " ".join(f"{sr:>8s}" for sr in surf_rels))
    for i, rt in enumerate(rel_types):
        row = " ".join(f"{ct[i,j]:8d}" for j in range(len(surf_rels)))
        print(f"  {rt:12s} {row}")

    chi2, p, dof, expected = stats.chi2_contingency(ct)
    print(f"\n  χ²={chi2:.2f}, dof={dof}, p={p:.4f}")

    # ── Test 2: 五行 vocabulary in 大象 texts ──
    print(f"\n{'=' * 60}")
    print("Test 2: 五行 vocabulary in 大象 texts")
    print("=" * 60)

    wuxing_hits = {}
    for term in WUXING_VOCAB:
        count = 0
        examples = []
        for d in daxiang:
            n = d["text"].count(term)
            if n > 0:
                count += n
                examples.append(f"{d['name']}: {d['text'][:30]}")
        if count > 0:
            wuxing_hits[term] = {"count": count, "examples": examples[:3]}

    if wuxing_hits:
        for term, info in wuxing_hits.items():
            print(f"  {term}: {info['count']} occurrences")
            for ex in info["examples"]:
                print(f"    {ex}")
    else:
        print("  No 五行 vocabulary found in any 大象 text.")

    # Note: 金木水火 will match image characters too — filter those out
    # Only count if they appear in the moral/action portion
    print("\n  Filtering: checking if hits are in trigram-image vs moral portions...")
    filtered_hits = {}
    for d in daxiang:
        text = d["text"]
        moral = d.get("moral_action", "")
        for term in ["金", "木", "水", "火", "土"]:
            if term in moral:
                filtered_hits.setdefault(term, []).append(f"{d['name']}: {moral[:30]}")

    if filtered_hits:
        for term, examples in filtered_hits.items():
            print(f"  {term} in moral portion: {len(examples)} occurrences")
    else:
        print("  No elemental vocabulary in moral/action portions.")

    # ── Test 3: Image-derived element vs actual element ──
    print(f"\n{'=' * 60}")
    print("Test 3: Image element prediction accuracy")
    print("=" * 60)

    all_images = {**IMAGE_TRIGRAM, **SECONDARY_IMAGE}
    image_element = {img: TRIGRAM_ELEMENT[trig] for img, trig in all_images.items()}

    correct_upper = 0
    correct_lower = 0
    total_upper = 0
    total_lower = 0

    for d in daxiang:
        h = atlas[str(d["hex_val"])]
        upper = parse_trigram_name(h["upper_trigram"]["name"])
        lower = parse_trigram_name(h["lower_trigram"]["name"])
        upper_el = TRIGRAM_ELEMENT[upper]
        lower_el = TRIGRAM_ELEMENT[lower]

        # Try to infer elements from images found in text
        found_images = []
        for img in all_images:
            if img in d["text"]:
                found_images.append(img)

        if len(found_images) >= 2:
            # First image usually = upper trigram in 大象, second = lower
            # But 大象 format is typically "上下" or image descriptions
            inferred_elements = [image_element[img] for img in found_images]
            # Check if any inferred element matches upper
            if upper_el in inferred_elements:
                correct_upper += 1
            total_upper += 1
            if lower_el in inferred_elements:
                correct_lower += 1
            total_lower += 1
        elif len(found_images) == 1:
            inferred_el = image_element[found_images[0]]
            if inferred_el == upper_el or inferred_el == lower_el:
                correct_upper += 1
            total_upper += 1

    print(f"  Element recovery (upper): {correct_upper}/{total_upper}")
    print(f"  Element recovery (lower): {correct_lower}/{total_lower}")

    # Cross-tab: image-derived element × actual element
    print("\n  Cross-tab: found image element → actual trigram element")
    elem_crosstab = {}
    for d in daxiang:
        h = atlas[str(d["hex_val"])]
        upper = parse_trigram_name(h["upper_trigram"]["name"])
        lower = parse_trigram_name(h["lower_trigram"]["name"])

        for img in all_images:
            if img in d["text"]:
                inferred = image_element[img]
                actual_upper = TRIGRAM_ELEMENT[upper]
                actual_lower = TRIGRAM_ELEMENT[lower]
                # Match to closest trigram
                for actual in [actual_upper, actual_lower]:
                    key = (inferred, actual)
                    elem_crosstab[key] = elem_crosstab.get(key, 0) + 1

    elements = sorted(set(TRIGRAM_ELEMENT.values()))
    print(f"\n  {'Inferred→':12s} " + " ".join(f"{e:>8s}" for e in elements))
    for inf_el in elements:
        row = []
        for act_el in elements:
            row.append(elem_crosstab.get((inf_el, act_el), 0))
        print(f"  {inf_el:12s} " + " ".join(f"{v:8d}" for v in row))

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print("Summary")
    print("=" * 60)
    has_wuxing = bool(filtered_hits)
    print(f"  大象 uses 五行 vocabulary in moral portions: {has_wuxing}")
    print(f"  大象 trigram images match actual trigrams: "
          f"{sum(1 for d in daxiang if d['trigrams_match_actual'])}/64 (with primary images)")
    extended_match = sum(1 for d in daxiang
                        if d["trigrams_match_actual"] or
                        any(si in d["text"] for si in SECONDARY_IMAGE))
    print(f"  Extended match (including secondary images): ~{extended_match}/64")
    print(f"  Relation type × surface relation: χ²={chi2:.2f}, p={p:.4f}")
    register = "imagistic" if not has_wuxing else "both"
    print(f"  → 大象 operates in: {register} register")

    output = {
        "relation_surface_chi2": {"chi2": float(chi2), "p": float(p), "dof": int(dof)},
        "wuxing_vocabulary": wuxing_hits if wuxing_hits else "none",
        "wuxing_in_moral": {k: len(v) for k, v in filtered_hits.items()} if filtered_hits else "none",
        "element_recovery": {
            "upper": {"correct": correct_upper, "total": total_upper},
            "lower": {"correct": correct_lower, "total": total_lower},
        },
        "register": register,
        "relation_type_crosstab": ct.tolist(),
        "relation_types": rel_types,
        "surface_relations": surf_rels,
    }

    with open(DATA / "daxiang_bridge.json", "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\nSaved to {DATA / 'daxiang_bridge.json'}")


if __name__ == "__main__":
    main()
