# TCM Study Plan

## Goal

Understand how Chinese medicine applies 五行 theory to clinical practice. Specifically:
1. How the 八纲辨证 (Eight Principle Differentiation) diagnostic system works
2. How 五行 is used alongside or within the 八纲 framework
3. Whether the tradition explicitly maps the three diagnostic axes to trigram lines
4. How 五行 生/克 cycles are used in diagnosis, treatment selection, and prognosis
5. What the mapping from clinical situations to the algebraic structure actually is

## Why TCM

The investigation established that the Z₅ grammar is typological, not dynamical, and requires three axes of similar kind. TCM's 八纲 has:
- Three binary axes: 寒/热 (cold/hot), 虚/实 (deficiency/excess), 表/里 (exterior/interior)
- All are clinical binary assessments of the same patient
- Measured by similar methods (pulse, tongue, symptom observation)
- Operating on similar timescales (disease progression)
- Native to the same intellectual tradition as the I Ching
- 五行 is already used in TCM — the mapping is predetermined, not invented

The D4 market test showed that when axes are physically asymmetric (trend ≠ vol ≠ liquidity), the grammar fails. TCM may have better axis symmetry. But we need to study the system first before testing anything.

Reference: 
- iching/domains/findings.md - Findings on the application of I Ching grammar.


## Phase 1: Understand the 八纲辨证 System

### Questions

**T1:** What exactly are the 八纲 (Eight Principles)? How are they defined clinically? What symptoms/signs determine each pole?

**T2:** Are the three axes truly independent in practice, or are there known correlations? (e.g., is 表 typically 实 and 里 typically 虚? Is 寒 correlated with 虚?)

**T3:** How do practitioners combine the three axes into a diagnosis? Is it literally a 3-bit binary label, or is it more graded/nuanced?

**T4:** What is the relationship between 八纲 diagnosis and 五行/脏腑 (organ) diagnosis? Are they parallel systems, nested systems, or sequential stages of the same process?

**T5:** Is there classical literature that explicitly connects the 八纲 axes to I Ching trigram lines?

## Phase 2: Understand 五行 in Clinical Practice

### Questions

**T6:** How does TCM assign 五行 to organs (脏腑)?
- 木 = 肝/胆 (liver/gallbladder)
- 火 = 心/小肠 (heart/small intestine)
- 土 = 脾/胃 (spleen/stomach)
- 金 = 肺/大肠 (lungs/large intestine)
- 水 = 肾/膀胱 (kidneys/bladder)

These are standard. But HOW are they used diagnostically? Does the 五行 assignment change the diagnosis, or only the treatment strategy?

**T7:** How are 生/克 cycles used clinically?
- 生 (generation): mother-child organ relationships. 木生火 = liver nourishes heart. Treatment: tonify the mother to help the child.
- 克 (control): control relationships. 木克土 = liver controls spleen. Pathology: liver excess over-controls spleen (木亢克土).

What determines whether a 克 relationship is normal (healthy control) vs pathological (over-control)?

**T8:** What is 五行生克制化 — the full system of generation, control, and their regulation? How does TCM distinguish normal 克 (necessary restraint) from pathological 克 (overcoming)?

**T9:** Does TCM use forbidden-pattern constraints analogous to GMS? Is there a clinical rule that says certain sequences of pathological transitions are impossible or never observed?

**T10:** Does TCM recognize a "valve" — a directional constraint where 克→生 transitions must pass through an intermediate state?

## Phase 3: Map the Structure

### Questions

**T11:** Under the traditional organ-element assignment, what is the Z₅ typing of the 八纲 × 脏腑 diagnostic space? Can we write down the explicit Q₃ vertex → element mapping for clinical states?

**T12:** Is the 八纲→trigram mapping unique, or are there multiple classical sources with conflicting assignments?

**T13:** Which line (b₀, b₁, b₂) maps to which diagnostic axis? The algebra predicts one axis is pure-克 (all transitions destructive), one is pure non-克 (all transitions benign), one is mixed. Does the clinical system have an axis that matches the pure-克 role?

**T14:** The axis-type alignment theorem (D3-R4) predicts: the pure-克 axis is the one carrying the doublet element pairs. In the trigram system, b₁ (middle/man) is pure-克. If 八纲 maps to trigrams, which diagnostic axis sits at b₁?

## Phase 4: Assess Testability

### Questions

**T15:** What clinical data exists? Case studies with sequential diagnoses showing how a patient moves through the 八纲 space over time? Natural history studies (untreated disease progression)?

**T16:** The practitioner bias problem: if TCM practitioners use 五行 to guide treatment, and treatment changes disease progression, then the data reflects the grammar's influence, not natural disease dynamics. Is there a way around this? Pre-treatment assessments? Untreated case series? Historical records from before 五行 was used in medicine?

**T17:** Sample size requirements: the D4 market test needed ~30-40 P₄ transitions for GMS detection. How many clinical case transitions would we need? Are there datasets of this size?

## Sources

### In-house — available for direct reading

**梅花易數** `texts/meihuajingshu/`
- vol2 has a medical domain (illness section). Extract the 體用 rules for medical diagnosis.
- The 五行 organ assignment is already documented across the investigation.

**黃帝內經** `texts/huangdineijing/`
- Foundational TCM text (~300 BCE). Public domain, from Chinese Wikisource.
- 素問 (Suwen / Basic Questions): 24 volumes → `suwen_01.txt` – `suwen_24.txt`
- 靈樞 (Lingshu / Spiritual Pivot): 12 volumes → `lingshu_01.txt` – `lingshu_12.txt`
- Traditional Chinese, each file readable in a single call.
- Key chapters for this investigation:
  - suwen_02 (卷2): 陰陽應象大論 ch.5 — yin/yang + 五行 correspondences (T1, T6)
  - suwen_03 (卷3): 六節藏象論 ch.9, 五藏生成 ch.10 — organ-element theory (T6)
  - suwen_07 (卷7): 藏氣法時論 ch.22, 宣明五氣 ch.23 — organ qi + seasonal 五行 regulation (T7, T8)
  - suwen_08 (卷8): 通評虛實論 ch.28 — 虚/实 assessment (T1, T2)
  - suwen_09 (卷9): 熱論 ch.31 — heat/cold disease theory (T1)
  - suwen_19 (卷19): 天元紀大論 ch.66, 五運行大論 ch.67 — 五行 dynamics, 運氣 theory (T7, T8)
  - suwen_20 (卷20): 五常政大論 ch.70 — 五行 regulation, 生克制化 (T8, T9)
  - lingshu_05 (卷5): 五邪 ch.20 — five pathogenic influences (T9)
  - lingshu_07 (卷7): 病傳 ch.42 — disease transmission patterns (T9, T10)
  - lingshu_11 (卷11): 九宮八風 ch.77 — nine palaces / eight winds (T5, trigram connection)

**傷寒論** `texts/shanghanlun/shang-han-lun.md`
- Zhang Zhongjing (~200 CE). Single file, 2867 lines, simplified Chinese.
- 22 篇 (chapters), 宋本 (Song dynasty edition). 397 clauses, 112 prescriptions.
- Systematic 六经辨证 (Six Channel Differentiation) — related to but distinct from 八纲.
- Key sections:
  - 辨太阳病 ch.5-7 — exterior/表 disease patterns (T1)
  - 辨阳明病 ch.8, 辨太阴病 ch.10 — interior/里 disease patterns (T1)
  - 辨少阴病 ch.11 — cold/寒 + deficiency/虚 patterns (T2, axis correlations)
  - 辨厥阴病 ch.12 — hot-cold mixed patterns (T2)

### External (to be researched)
- Modern: TCM diagnostic textbooks that formalize the 八纲 system
- Clinical: case study databases, if they exist in structured format

## Execution Order

1. **Extract the medical domain rules from 梅花易數** — in-house, no sourcing needed. What does the 體用 system say about illness? (Connects to 8c findings.)
2. **Research 八纲辨证** — understand the system from TCM sources. Establish whether the three axes are genuinely binary and independent in clinical practice.
3. **Research 五行 clinical application** — how 生/克 is actually used in diagnosis and treatment. Whether forbidden patterns exist in the tradition.
4. **Map the structure** — determine whether the 八纲→trigram mapping exists in classical sources, or must be constructed.
5. **Assess testability** — identify available data, bias risks, sample size requirements.

## What Would Change Our Understanding

- **Classical mapping exists and matches the algebra:** The 八纲 axes were traditionally assigned to specific trigram lines, and the assignment produces the algebraic axis-type hierarchy. This would mean the I Ching and TCM share the same Q₃ × Z₅ structure by design, not coincidence.
- **Classical mapping exists but doesn't match:** The tradition assigned the axes differently from what the algebra would predict. The systems are related but the mapping is conventional, not structural.
- **No classical mapping:** The 八纲 and the I Ching developed independently within the Chinese tradition. The three binary axes are parallel but not connected. Any mapping must be constructed, introducing researcher degrees of freedom.
- **Axes aren't genuinely binary/independent:** The 八纲 is more nuanced than Q₃ — degrees of cold/hot, correlations between axes. The Q₃ framework is too coarse for clinical reality. This would apply to all Q₃ domain tests, not just TCM.
