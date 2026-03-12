#!/usr/bin/env python3
"""
05_semantic: §V Text extraction — structured data from sy-divination.md.

Writes:
  mh_domains.json — 18 application domain bindings
  mh_channels.json — 十應 channels + inversion + 向背
  mh_timing.json — timing formula
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def build_domains():
    """18 application domains from vol 2, extracted from sy-divination.md."""
    domains = [
        {
            "number": 1,
            "domain": "天時 (Weather)",
            "ti_meaning": None,
            "yong_meaning": "all trigrams vote as committee",
            "special_rules": "No 體/用 split. Multiple trigrams of one type amplify "
                             "(重坎=heavy rain). Trigrams suppress by 克. "
                             "Read entire hexagram as weather panel.",
            "weather_exception": True,
            "uses_tiyong": False,
        },
        {
            "number": 2,
            "domain": "人事 (Human affairs)",
            "ti_meaning": "self",
            "yong_meaning": "situation/event",
            "special_rules": "Standard 生克",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 3,
            "domain": "家宅 (Household)",
            "ti_meaning": "self/family",
            "yong_meaning": "the house/dwelling",
            "special_rules": "Standard. Pure-yang/pure-yin structural override "
                             "(西林寺: all 比和 but 群陰剥陽 = structural contradiction).",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 4,
            "domain": "婚姻 (Marriage)",
            "ti_meaning": "one's own family",
            "yong_meaning": "other family",
            "special_rules": "Trigram 象 gives appearance of spouse. "
                             "生体=favorable match, 克体=unfavorable.",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 5,
            "domain": "生產 (Childbirth)",
            "ti_meaning": "mother",
            "yong_meaning": "child",
            "special_rules": "陽爻多=boy, 陰爻多=girl. "
                             "生体=safe delivery, 克体=difficulty.",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 6,
            "domain": "飲食 (Food/drink)",
            "ti_meaning": "self/diner",
            "yong_meaning": "the meal",
            "special_rules": "坎=wine/liquid, 兑=food. "
                             "Trigram images determine cuisine type.",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 7,
            "domain": "求財 (Wealth)",
            "ti_meaning": "self",
            "yong_meaning": "money/assets",
            "special_rules": "生体 date = gain; 克体 date = loss. "
                             "Timing uses seasonal element for gain/loss dates.",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 8,
            "domain": "失物 (Lost objects)",
            "ti_meaning": "self/searcher",
            "yong_meaning": "lost object",
            "special_rules": "変卦 trigram = search direction. "
                             "乾→NW/high, 坤→SW/fields, 坎→water, 离→S/kitchen, etc.",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 9,
            "domain": "疾病 (Illness)",
            "ti_meaning": "patient",
            "yong_meaning": "disease",
            "special_rules": "Three sub-systems: "
                             "(1) Spirit diagnosis: 克体 trigram → ghost/deity class, "
                             "(2) Pharmacology: 生体 trigram → medicine type "
                             "(离→hot, 坎→cold, 艮→warming, 乾兑→cooling), "
                             "(3) 乾坤 walkthrough: same hex, all 6 lines → opposite outcomes.",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 10,
            "domain": "訴訟 (Litigation)",
            "ti_meaning": "self",
            "yong_meaning": "opponent",
            "special_rules": "Standard 生克. 体克用=win, 克体=lose.",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 11,
            "domain": "墳墓 (Graves)",
            "ti_meaning": "self/descendants",
            "yong_meaning": "burial site",
            "special_rules": "Standard 生克. Trigram images give site features.",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 12,
            "domain": "出行 (Travel)",
            "ti_meaning": "self/traveler",
            "yong_meaning": "journey/destination",
            "special_rules": "Not extracted — requires original vol 2 text",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 13,
            "domain": "求官 (Officials)",
            "ti_meaning": "self/candidate",
            "yong_meaning": "the position",
            "special_rules": "Not extracted — requires original vol 2 text",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 14,
            "domain": "求人 (Seeking people)",
            "ti_meaning": "self/seeker",
            "yong_meaning": "the person sought",
            "special_rules": "Not extracted — requires original vol 2 text",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 15,
            "domain": "交易 (Transactions)",
            "ti_meaning": "self/trader",
            "yong_meaning": "the deal",
            "special_rules": "Not extracted — requires original vol 2 text",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 16,
            "domain": "求謀 (Letters/news)",
            "ti_meaning": "self/inquirer",
            "yong_meaning": "the information",
            "special_rules": "Not extracted — requires original vol 2 text",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 17,
            "domain": "田獵 (Fishing/hunting)",
            "ti_meaning": "self/hunter",
            "yong_meaning": "the quarry",
            "special_rules": "Not extracted — requires original vol 2 text",
            "weather_exception": False,
            "uses_tiyong": True,
        },
        {
            "number": 18,
            "domain": "雜占 (Miscellaneous)",
            "ti_meaning": "self/subject",
            "yong_meaning": "the matter",
            "special_rules": "Not extracted — requires original vol 2 text",
            "weather_exception": False,
            "uses_tiyong": True,
        },
    ]
    return domains


def build_channels():
    """十應 channels + inversion principle + 向背."""
    return {
        "channels": [
            {"number": 1, "name": "正应", "source": "本卦",
             "element_derivation": "algebraic",
             "description": "體/用 五行 relation of the original hexagram"},
            {"number": 2, "name": "互应", "source": "互卦",
             "element_derivation": "algebraic",
             "description": "Nuclear trigrams evaluated against 體"},
            {"number": 3, "name": "变应", "source": "变卦",
             "element_derivation": "algebraic",
             "description": "Changed hexagram's 用-side trigram vs 體"},
            {"number": 4, "name": "日应", "source": "日辰",
             "element_derivation": "calendrical",
             "description": "Day's earthly branch element vs 體"},
            {"number": 5, "name": "刻应", "source": "刻 (casting instant)",
             "element_derivation": "perceptual (三要)",
             "description": "Omens at the exact moment of casting"},
            {"number": 6, "name": "外应", "source": "外物",
             "element_derivation": "perceptual (三要)",
             "description": "Objects or people appearing at casting"},
            {"number": 7, "name": "天时应", "source": "天時",
             "element_derivation": "perceptual (三要)",
             "description": "Current weather conditions"},
            {"number": 8, "name": "地理应", "source": "地理",
             "element_derivation": "perceptual (三要)",
             "description": "Physical environment at casting location"},
            {"number": 9, "name": "人事应", "source": "人事",
             "element_derivation": "perceptual (三要)",
             "description": "Human activities nearby at casting"},
            {"number": 10, "name": "方应", "source": "方位",
             "element_derivation": "perceptual (三要)",
             "description": "Querent's directional position relative to caster"},
        ],
        "channel_classification": {
            "algebraic": [1, 2, 3],
            "calendrical": [4],
            "perceptual": [5, 6, 7, 8, 9, 10],
            "note": "Channels 1-3 computed from hexagram. Channel 4 from calendar. "
                    "Channels 5-10 from 三要 perception. "
                    "The hexagram provides 3/10 channels; the remaining 7 require observation."
        },
        "inversion_rule": {
            "principle": "Hexagram 生克 overrides perceptual omen sign",
            "source_quote": "必须以易卦为主，克应次之",
            "example": "Gold = auspicious in 三要, but if 体 is Wood, "
                       "Metal 克 Wood = harmful. Coffin = death in 三要, "
                       "but if 体 is Fire, Wood 生 Fire = recovery.",
            "priority_order": ["hexagram 体/用 生克", "external 克應 omens",
                               "observer state", "Yi line text (後天 only)"]
        },
        "xiangbei": {
            "approaching": "favorable sign arriving → good fortune coming; "
                           "harmful sign arriving → disaster approaching",
            "departing": "favorable sign leaving → good fortune spent; "
                         "harmful sign leaving → disaster past",
            "mechanism": "Adds temporal arrow (approaching/receding) to every "
                         "用 input. Direction modifies the temporal dimension "
                         "of the reading, not the valence."
        },
        "boundaries": {
            "extractable": [
                "channel → element mapping (algebraic channels fully formalized)",
                "inversion priority (hexagram > omens)",
                "向背 sign modifier (directional arrow)",
                "静占 graceful degradation (drop channels 5-10 when no input)"
            ],
            "context_only": [
                "三要 framework (perceptual theory — 虚灵 cultivation, not algorithm)",
                "真生真克 intensity gradient (strength of 生克 by seasonal context)",
                "心易 anti-literalism (trigram→referent is many-to-many, context-selected)"
            ]
        }
    }


def build_timing():
    """Timing formula (克應之期) from vol 2-3."""
    return {
        "formula": "timing = base_number × observer_modifier, unit by event type",
        "arc_position_map": {
            "本生体": {
                "label": "immediate (即成)",
                "meaning": "Favorable force present at surface → fast resolution"
            },
            "互生体": {
                "label": "gradual (渐成)",
                "meaning": "Favorable force in nuclear layer → middling resolution"
            },
            "變生体": {
                "label": "slow (稍迟)",
                "meaning": "Favorable force only in outcome → delayed resolution"
            }
        },
        "observer_state_map": {
            "walking (行)": {"modifier": 0.5, "meaning": "fast response → halve the number"},
            "standing (立)": {"modifier": 1.0, "meaning": "moderate → use number as-is"},
            "sitting (坐)": {"modifier": 2.0, "meaning": "slow response → double the number"},
        },
        "base_number": "全卦之数 — total number from the casting arithmetic",
        "unit_selection": {
            "ephemeral": "days",
            "medium": "months",
            "durable": "years",
            "note": "Practitioner judgment. No algorithm for unit selection."
        },
        "two_channel_note": {
            "xiantian": "先天: uses arc layer only (止以卦論，不甚用易之爻辭). "
                        "Timing from 卦气 (trigram-associated stems/branches).",
            "houtian": "後天: uses arc + 爻辭 text layer. "
                       "Timing from total number + observer state."
        }
    }


def build_two_channel_architecture():
    """Two-channel architecture documentation."""
    return {
        "text_channel": {
            "source": "爻辭 (line texts)",
            "encodes": "present state (snapshot of the situation at 本卦)",
            "correlates_with": "ben_relation",
            "used_in": "後天 only",
            "vol2_ref": "后天则用爻辞",
            "evidence": "吉 correlates with 生体-at-本 (44.4%), "
                        "凶 correlates with 比和-at-本 (20.2%) and 克体-at-本. "
                        "Neither tracks arc trajectory."
        },
        "arc_channel": {
            "source": "體/用 五行 生克 across 本→互→變",
            "encodes": "trajectory (how situation develops through layers)",
            "used_in": "先天 and 後天",
            "vol2_ref": "止以卦论，不甚用《易》之爻辞 (先天)",
            "evidence": "arc_type captures temporal development — "
                        "rescued/betrayed/improving/deteriorating arc types."
        },
        "resolution": {
            "agreement": "When channels agree: high confidence (both textual and "
                         "algebraic evidence point same direction)",
            "disagreement": "When channels disagree: 详审卦辞，及克用体应之类...要在圆机，不可执 "
                            "(examine carefully, remain flexible, don't be rigid)",
            "priority": "Arc channel (生克) is primary; text channel is supporting. "
                        "先天 explicitly drops text channel entirely."
        }
    }


def main():
    # Write domains
    domains = build_domains()
    with open(HERE / "mh_domains.json", "w") as f:
        json.dump({"domains": domains, "total": len(domains),
                   "weather_exception_count": 1,
                   "extracted_from_text": 11,
                   "requires_vol2": 7}, f, ensure_ascii=False, indent=2)
    print(f"Written mh_domains.json ({len(domains)} domains)")

    # Write channels
    channels = build_channels()
    with open(HERE / "mh_channels.json", "w") as f:
        json.dump(channels, f, ensure_ascii=False, indent=2)
    print(f"Written mh_channels.json ({len(channels['channels'])} channels)")

    # Write timing
    timing = build_timing()
    with open(HERE / "mh_timing.json", "w") as f:
        json.dump(timing, f, ensure_ascii=False, indent=2)
    print(f"Written mh_timing.json")

    # Write two-channel architecture
    arch = build_two_channel_architecture()
    with open(HERE / "mh_two_channel.json", "w") as f:
        json.dump(arch, f, ensure_ascii=False, indent=2)
    print(f"Written mh_two_channel.json")

    # Summary
    print(f"\n=== §V SEMANTIC EXTRACTION SUMMARY ===")
    print(f"Domains: {len(domains)} total, {11} extracted from sy-divination.md, {7} require vol 2")
    print(f"Weather exception: domain 1 (天時) — no 體/用, committee-based")
    print(f"Channels: 10 (3 algebraic, 1 calendrical, 6 perceptual)")
    print(f"Timing: base_number × observer_modifier, unit by practitioner judgment")
    print(f"Two-channel architecture: text (爻辭, 本-snapshot) + arc (生克, trajectory)")
    print(f"  先天 = arc only; 後天 = arc + text")
    print(f"  Text channel tracks present state, not outcome")
    print(f"  Arc channel tracks development through 本→互→變")


if __name__ == "__main__":
    main()
