# V₄-Compatible Pairings + Palace Torus Trajectories

## Task 1: V₄-Compatible Pairings

V₄ orbits: 8 of size 2, 12 of size 4
Size-2 orbits: pairing forced (1 way each)
Size-4 orbits: 3 splittings each (one per involution)

### Size-4 orbit splittings

  Orbit 1: ['#24 Fu', '#43 Guai', '#23 Bo', '#44 Gou']
    comp: {#24 Fu,#44 Gou} + {#43 Guai,#23 Bo}
    rev: {#24 Fu,#23 Bo} + {#43 Guai,#44 Gou}
    c∘r: {#24 Fu,#43 Guai} + {#23 Bo,#44 Gou}
  Orbit 2: ['#7 Shi', '#8 Bi', '#14 Da You', '#13 Tong Ren']
    comp: {#7 Shi,#13 Tong Ren} + {#8 Bi,#14 Da You}
    rev: {#7 Shi,#8 Bi} + {#14 Da You,#13 Tong Ren}
    c∘r: {#7 Shi,#14 Da You} + {#8 Bi,#13 Tong Ren}
  Orbit 3: ['#19 Lin', '#34 Da Zhuang', '#20 Guan', '#33 Dun']
    comp: {#19 Lin,#33 Dun} + {#34 Da Zhuang,#20 Guan}
    rev: {#19 Lin,#20 Guan} + {#34 Da Zhuang,#33 Dun}
    c∘r: {#19 Lin,#34 Da Zhuang} + {#20 Guan,#33 Dun}
  Orbit 4: ['#15 Qian', '#16 Yu', '#9 Xiao Chu', '#10 Lu']
    comp: {#15 Qian,#10 Lu} + {#16 Yu,#9 Xiao Chu}
    rev: {#15 Qian,#16 Yu} + {#9 Xiao Chu,#10 Lu}
    c∘r: {#15 Qian,#9 Xiao Chu} + {#16 Yu,#10 Lu}
  Orbit 5: ['#36 Ming Yi', '#5 Xu', '#35 Jin', '#6 Song']
    comp: {#36 Ming Yi,#6 Song} + {#5 Xu,#35 Jin}
    rev: {#36 Ming Yi,#35 Jin} + {#5 Xu,#6 Song}
    c∘r: {#36 Ming Yi,#5 Xu} + {#35 Jin,#6 Song}
  Orbit 6: ['#46 Sheng', '#45 Cui', '#26 Da Chu', '#25 Wu Wang']
    comp: {#46 Sheng,#25 Wu Wang} + {#45 Cui,#26 Da Chu}
    rev: {#46 Sheng,#45 Cui} + {#26 Da Chu,#25 Wu Wang}
    c∘r: {#46 Sheng,#26 Da Chu} + {#45 Cui,#25 Wu Wang}
  Orbit 7: ['#51 Zhen', '#58 Dui', '#52 Gen', '#57 Xun']
    comp: {#51 Zhen,#57 Xun} + {#58 Dui,#52 Gen}
    rev: {#51 Zhen,#52 Gen} + {#58 Dui,#57 Xun}
    c∘r: {#51 Zhen,#58 Dui} + {#52 Gen,#57 Xun}
  Orbit 8: ['#40 Xie', '#39 Jian', '#38 Kui', '#37 Jia Ren']
    comp: {#40 Xie,#37 Jia Ren} + {#39 Jian,#38 Kui}
    rev: {#40 Xie,#39 Jian} + {#38 Kui,#37 Jia Ren}
    c∘r: {#40 Xie,#38 Kui} + {#39 Jian,#37 Jia Ren}
  Orbit 9: ['#55 Feng', '#60 Jie', '#56 Lu', '#59 Huan']
    comp: {#55 Feng,#59 Huan} + {#60 Jie,#56 Lu}
    rev: {#55 Feng,#56 Lu} + {#60 Jie,#59 Huan}
    c∘r: {#55 Feng,#60 Jie} + {#56 Lu,#59 Huan}
  Orbit 10: ['#32 Heng', '#31 Xian', '#41 Sun', '#42 Yi']
    comp: {#32 Heng,#42 Yi} + {#31 Xian,#41 Sun}
    rev: {#32 Heng,#31 Xian} + {#41 Sun,#42 Yi}
    c∘r: {#32 Heng,#41 Sun} + {#31 Xian,#42 Yi}
  Orbit 11: ['#3 Zhun', '#49 Ge', '#4 Meng', '#50 Ding']
    comp: {#3 Zhun,#50 Ding} + {#49 Ge,#4 Meng}
    rev: {#3 Zhun,#4 Meng} + {#49 Ge,#50 Ding}
    c∘r: {#3 Zhun,#49 Ge} + {#4 Meng,#50 Ding}
  Orbit 12: ['#48 Jing', '#47 Kun', '#22 Bi', '#21 Shi He']
    comp: {#48 Jing,#21 Shi He} + {#47 Kun,#22 Bi}
    rev: {#48 Jing,#47 Kun} + {#22 Bi,#21 Shi He}
    c∘r: {#48 Jing,#22 Bi} + {#47 Kun,#21 Shi He}

### Independence verification

V₄ acts on each orbit independently (orbits are V₄-invariant sets).
A pairing is V₄-compatible iff within each orbit, the splitting
comes from one of the 3 involutions. No cross-orbit constraints.

  Random mixed-involution pairings tested: 1000
  V₄-compatible: 1000/1000

### Total V₄-compatible pairings: 3^12 = 531,441

### KW pairing involution choices

  Orbit 1: KW uses rev
  Orbit 2: KW uses rev
  Orbit 3: KW uses rev
  Orbit 4: KW uses rev
  Orbit 5: KW uses rev
  Orbit 6: KW uses rev
  Orbit 7: KW uses rev
  Orbit 8: KW uses rev
  Orbit 9: KW uses rev
  Orbit 10: KW uses rev
  Orbit 11: KW uses rev
  Orbit 12: KW uses rev

  KW involution distribution: {'rev': 12}
  KW uses reversal for ALL 12 size-4 orbits: True

## Task 2: Palace Walks on Z₅×Z₅ Torus

### Element-pair trajectories

  坤宮 (Earth):
    Trajectory: ['Ea→Ea', 'Wo→Ea', 'Me→Ea', 'Me→Ea', 'Me→Wo', 'Me→Me', 'Me→Wa', 'Ea→Wa']
    Z₅×Z₅ cells visited: 7/8 (revisits: 1)
    Distinct relations: 4/5
    Relations: ['比和', '体克', '生体', '生体', '体克', '比和', '体生', '体克']
    Z₅ step distances (lo,up): [(3, 0), (3, 0), (0, 0), (0, 3), (0, 3), (0, 1), (4, 0)]

  震宮 (Wood):
    Trajectory: ['Wo→Wo', 'Ea→Wo', 'Wa→Wo', 'Wo→Wo', 'Wo→Ea', 'Wo→Wa', 'Wo→Me', 'Wo→Me']
    Z₅×Z₅ cells visited: 6/8 (revisits: 2)
    Distinct relations: 5/5
    Relations: ['比和', '克体', '体生', '比和', '体克', '生体', '克体', '克体']
    Z₅ step distances (lo,up): [(2, 0), (2, 0), (1, 0), (0, 2), (0, 2), (0, 4), (0, 0)]

  坎宮 (Water):
    Trajectory: ['Wa→Wa', 'Me→Wa', 'Wo→Wa', 'Fi→Wa', 'Fi→Me', 'Fi→Wo', 'Fi→Ea', 'Wa→Ea']
    Z₅×Z₅ cells visited: 8/8 (revisits: 0)
    Distinct relations: 5/5
    Relations: ['比和', '体生', '生体', '克体', '体克', '生体', '体生', '克体']
    Z₅ step distances (lo,up): [(4, 0), (2, 0), (1, 0), (0, 4), (0, 2), (0, 2), (3, 0)]

  兌宮 (Metal):
    Trajectory: ['Me→Me', 'Wa→Me', 'Ea→Me', 'Ea→Me', 'Ea→Wa', 'Ea→Ea', 'Ea→Wo', 'Me→Wo']
    Z₅×Z₅ cells visited: 7/8 (revisits: 1)
    Distinct relations: 5/5
    Relations: ['比和', '生体', '体生', '体生', '体克', '比和', '克体', '体克']
    Z₅ step distances (lo,up): [(1, 0), (3, 0), (0, 0), (0, 1), (0, 3), (0, 3), (1, 0)]

  艮宮 (Earth):
    Trajectory: ['Ea→Ea', 'Fi→Ea', 'Me→Ea', 'Me→Ea', 'Me→Fi', 'Me→Me', 'Me→Wo', 'Ea→Wo']
    Z₅×Z₅ cells visited: 7/8 (revisits: 1)
    Distinct relations: 5/5
    Relations: ['比和', '体生', '生体', '生体', '克体', '比和', '体克', '克体']
    Z₅ step distances (lo,up): [(4, 0), (2, 0), (0, 0), (0, 4), (0, 2), (0, 2), (4, 0)]

  離宮 (Fire):
    Trajectory: ['Fi→Fi', 'Ea→Fi', 'Wo→Fi', 'Wa→Fi', 'Wa→Ea', 'Wa→Wo', 'Wa→Me', 'Fi→Me']
    Z₅×Z₅ cells visited: 8/8 (revisits: 0)
    Distinct relations: 5/5
    Relations: ['比和', '生体', '体生', '体克', '克体', '体生', '生体', '体克']
    Z₅ step distances (lo,up): [(1, 0), (3, 0), (4, 0), (0, 1), (0, 3), (0, 3), (2, 0)]

  巽宮 (Wood):
    Trajectory: ['Wo→Wo', 'Me→Wo', 'Fi→Wo', 'Wo→Wo', 'Wo→Me', 'Wo→Fi', 'Wo→Ea', 'Wo→Ea']
    Z₅×Z₅ cells visited: 6/8 (revisits: 2)
    Distinct relations: 5/5
    Relations: ['比和', '体克', '生体', '比和', '克体', '体生', '体克', '体克']
    Z₅ step distances (lo,up): [(3, 0), (3, 0), (4, 0), (0, 3), (0, 3), (0, 1), (0, 0)]

  乾宮 (Metal):
    Trajectory: ['Me→Me', 'Wo→Me', 'Ea→Me', 'Ea→Me', 'Ea→Wo', 'Ea→Ea', 'Ea→Fi', 'Me→Fi']
    Z₅×Z₅ cells visited: 7/8 (revisits: 1)
    Distinct relations: 4/5
    Relations: ['比和', '克体', '体生', '体生', '克体', '比和', '生体', '克体']
    Z₅ step distances (lo,up): [(2, 0), (2, 0), (0, 0), (0, 2), (0, 2), (0, 4), (1, 0)]

### Torus coverage

  Total Z₅×Z₅ cells visited across all palaces: 25/25

  Cell occupancy distribution:
    1 visit(s): 4 cells
    2 visit(s): 12 cells
    4 visit(s): 9 cells

### Coverage by basin-trajectory class

  3-basin Kun-type (坤,坎): 14 Z₅×Z₅ cells
  3-basin Qian-type (離,乾): 14 Z₅×Z₅ cells
  2-basin KanLi+Qian (震,兌): 12 Z₅×Z₅ cells
  2-basin KanLi+Kun (艮,巽): 12 Z₅×Z₅ cells

### Complement-paired palace trajectories

  坤↔乾: comp(traj₁) == traj₂ at 8/8 ranks
  坎↔離: comp(traj₁) == traj₂ at 8/8 ranks
  震↔巽: comp(traj₁) == traj₂ at 8/8 ranks
  兌↔艮: comp(traj₁) == traj₂ at 8/8 ranks

## Task 3: Selecting the KW Pairing

  KW pairing == pure reversal pairing: True

### Constraint A: Total Hamming distance

  complement: total Hamming = 192, avg = 6.00
  reversal (KW): total Hamming = 120, avg = 3.75
  comp∘rev: total Hamming = 120, avg = 3.75

  Hamming distance distribution per pair:
    complement: {6: 32}
    reversal (KW): {2: 12, 4: 12, 6: 8}
    comp∘rev: {2: 12, 4: 12, 6: 8}

### Hamming distance across all 3^12 pairings

  Range: [96, 192]
  Distribution:
    H=96:      1 pairings
    H=100:     12 pairings
    H=104:     78 pairings
    H=108:    352 pairings
    H=112:   1221 pairings
    H=116:   3432 pairings
    H=120:   8074 pairings ← KW ← c∘r
    H=124:  16236 pairings
    H=128:  28314 pairings
    H=132:  43252 pairings
    H=136:  58278 pairings
    H=140:  69576 pairings
    H=144:  73789 pairings
    H=148:  69576 pairings
    H=152:  58278 pairings
    H=156:  43252 pairings
    H=160:  28314 pairings
    H=164:  16236 pairings
    H=168:   8074 pairings
    H=172:   3432 pairings
    H=176:   1221 pairings
    H=180:    352 pairings
    H=184:     78 pairings
    H=188:     12 pairings
    H=192:      1 pairings ← comp

  KW Hamming total: 120
  Rank among all 3^12: 7/25 distinct values
  KW is NOT minimum Hamming

### Constraint B: Same-basin pairs

  complement: 16/32 same-basin pairs
  reversal (KW): 28/32 same-basin pairs
  comp∘rev: 16/32 same-basin pairs

### Constraint C: Per-orbit minimum-Hamming involution

  Orbit 1 (#24 Fu...): [('rev', 4), ('c∘r', 8), ('comp', 12)], min=['rev']
  Orbit 2 (#7 Shi...): [('rev', 4), ('c∘r', 8), ('comp', 12)], min=['rev']
  Orbit 3 (#19 Lin...): [('c∘r', 4), ('rev', 8), ('comp', 12)], min=['c∘r']
  Orbit 4 (#15 Qian...): [('rev', 4), ('c∘r', 8), ('comp', 12)], min=['rev']
  Orbit 5 (#36 Ming Yi...): [('c∘r', 4), ('rev', 8), ('comp', 12)], min=['c∘r']
  Orbit 6 (#46 Sheng...): [('c∘r', 4), ('rev', 8), ('comp', 12)], min=['c∘r']
  Orbit 7 (#51 Zhen...): [('c∘r', 4), ('rev', 8), ('comp', 12)], min=['c∘r']
  Orbit 8 (#40 Xie...): [('c∘r', 4), ('rev', 8), ('comp', 12)], min=['c∘r']
  Orbit 9 (#55 Feng...): [('rev', 4), ('c∘r', 8), ('comp', 12)], min=['rev']
  Orbit 10 (#32 Heng...): [('rev', 4), ('c∘r', 8), ('comp', 12)], min=['rev']
  Orbit 11 (#3 Zhun...): [('c∘r', 4), ('rev', 8), ('comp', 12)], min=['c∘r']
  Orbit 12 (#48 Jing...): [('rev', 4), ('c∘r', 8), ('comp', 12)], min=['rev']

  Reversal is minimum-Hamming in 6/12 orbits

### Constraint D: Relation inversion in pairs

  complement:
    Inverse relations: 32/32
    Same relation: 0/32
    Other: 0/32
  reversal (KW):
    Inverse relations: 14/32
    Same relation: 4/32
    Other: 14/32
  comp∘rev:
    Inverse relations: 14/32
    Same relation: 4/32
    Other: 14/32

### Constraint E: Same-palace pairs

  complement: 0/32 same-palace pairs
  reversal (KW): 0/32 same-palace pairs
  comp∘rev: 8/32 same-palace pairs

### Minimum-Hamming pairings

  Minimum total Hamming: 96
  Number of pairings achieving minimum: 1
  One minimum-Hamming choice: (1, 1, 2, 1, 2, 2, 2, 2, 1, 1, 2, 1)
  Involution choices: ['rev', 'rev', 'c∘r', 'rev', 'c∘r', 'c∘r', 'c∘r', 'c∘r', 'rev', 'rev', 'c∘r', 'rev']

  Maximum total Hamming: 192
  Achieved by: 1 pairings
  One max choice: ['comp', 'comp', 'comp', 'comp', 'comp', 'comp', 'comp', 'comp', 'comp', 'comp', 'comp', 'comp']

## Summary

### V₄-compatible pairings
  Total: 3^12 = 531,441
  Choices are independent across orbits (verified by 1000 random tests)
  KW pairing uses reversal for ALL 12 size-4 orbits

### What selects KW?
  A. Hamming distance: KW total = 120
     NOT minimum (min = 96, max = 192)
  B. Same-basin pairs: KW=28, comp=16, c∘r=16
  C. Reversal is minimum-Hamming in 6/12 orbits
  D. Relation inversion: complement perfectly inverts (by algebra), reversal does not

### Palace torus
  All palaces cover 25/25 Z₅×Z₅ cells
  Complement-paired palaces have comp-related trajectories
