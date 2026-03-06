# Unified Transition Table — 31 Inter-Pair Bridges

Each row joins algebraic profile (basin, 互, kernel, distances) with semantic
profile (Xugua logic, confidence, directionality) and corridor profile.

## Column Key

| Column | Meaning |
|--------|---------|
| T# | Transition number (1–31) |
| Bridge | Exit hex (#) → Entry hex (#) |
| d | Hex Hamming distance |
| lo/up | Lower/upper trigram Hamming distance |
| Basin | Exit basin → Entry basin (Kun/Qian/KanLi) |
| ×? | Basin-crossing (Y/N) |
| 互d | 互 Hamming distance |
| Kern | Mirror kernel (id/O/M/I/OM/OI/MI/OMI) |
| H? | H-kernel member (Y/N) |
| Pres | Preserving bridge: which trigram preserved, or — |
| Logic | Xugua logic type |
| Conf | Xugua confidence (Direct/Implied) |
| Dir | Directionality (→ unidirectional / ⇀ weakly directional) |
| Lvl | Level (PP pair-to-pair / HH hex-to-hex) |
| Corridor | Corridor relationship |
| Regime | Corridor-rich or corridor-free |
| RB | Basin run boundary (Y/N) |

## Main Table

| T# | Bridge | d | lo | up | Basin | ×? | 互d | Kern | H? | Pres | Logic | Conf | Dir | Lvl | Corridor | Reg | RB |
|:--:|--------|:-:|:--:|:--:|-------|:--:|:---:|:----:|:--:|------|-------|------|:---:|:---:|----------|:---:|:--:|
| 1 | Kun(#2)→Zhun(#3) | 2 | 1 | 1 | Kun→Kun | N | 1 | OM | N | — | Causal | Direct | → | PP | LOCAL_EXIT | rich | N |
| 2 | Meng(#4)→Xu(#5) | 4 | 2 | 2 | Kun→Kan | **Y** | 3 | MI | **Y** | — | Causal | Direct | → | HH | RE_ENTRY | rich | **Y** |
| 3 | Song(#6)→Shi(#7) | 3 | 0 | 3 | Kan→Kun | **Y** | 3 | OMI | **Y** | Lo:Water | Causal | Direct | ⇀ | HH | LOCAL_EXIT+INIT_ENTRY | rich | **Y** |
| 4 | Bi(#8)→Xiao Chu(#9) | 4 | 3 | 1 | Kun→Kan | **Y** | 3 | MI | **Y** | — | Causal | Implied | ⇀ | HH | LOCAL_EXIT+RE_ENTRY | rich | **Y** |
| 5 | Lu(#10)→Tai(#11) | 4 | 1 | 3 | Kan→Kan | N | 5 | OM | N | — | Causal | Direct | → | HH | TERM_EXIT+RE_ENTRY | rich | N |
| 6 | Pi(#12)→Tong Ren(#13) | 2 | 2 | 0 | Kan→Qia | **Y** | 2 | OI | N | Up:Heaven | **Cyclical** | Direct | ⇀ | HH | LOCAL_EXIT | rich | **Y** |
| 7 | Da You(#14)→Qian(#15) | 4 | 2 | 2 | Qia→Kan | **Y** | 3 | MI | **Y** | — | **Contrastive** | Direct | → | HH | RE_ENTRY | rich | **Y** |
| 8 | Yu(#16)→Sui(#17) | 2 | 1 | 1 | Kan→Kan | N | 1 | OM | N | — | Causal | Implied | ⇀ | HH | LOCAL_EXIT+INIT_ENTRY | rich | N |
| 9 | Gu(#18)→Lin(#19) | 3 | 2 | 1 | Kan→Kun | **Y** | 2 | I | N | — | Causal | Direct | → | HH | LOCAL_EXIT+RE_ENTRY | rich | **Y** |
| 10 | Guan(#20)→Shi He(#21) | 3 | 1 | 2 | Kun→Kan | **Y** | 3 | OMI | **Y** | — | Causal | Implied | ⇀ | HH | TERM_EXIT+RE_ENTRY | rich | **Y** |
| 11 | Bi(#22)→Bo(#23) | 2 | 2 | 0 | Kan→Kun | **Y** | 2 | OI | N | Up:Mtn | **Cyclical** | Direct | → | HH | TERM_EXIT | rich | **Y** |
| 12 | Fu(#24)→Wu Wang(#25) | 3 | 0 | 3 | Kun→Kan | **Y** | 3 | OMI | **Y** | Lo:Thndr | Causal | Direct | → | HH | BETWEEN | rich | **Y** |
| 13 | Da Chu(#26)→Yi(#27) | 2 | 2 | 0 | Kan→Kun | **Y** | 3 | MI | **Y** | Up:Mtn | Causal | Direct | → | HH | INIT_ENTRY | rich | **Y** |
| 14 | Da Guo(#28)→Kan(#29) | 2 | 1 | 1 | Qia→Kun | **Y** | 4 | id | **Y** | — | **Cyclical** | Implied | ⇀ | HH | LOCAL_EXIT | rich | **Y** |
| 15 | Li(#30)→Xian(#31) | 3 | 1 | 2 | Qia→Qia | N | 1 | M | N | — | **Temporal** | Direct | → | PP | RE_ENTRY | rich | N |
| 16 | Heng(#32)→Dun(#33) | 3 | 1 | 2 | Qia→Qia | N | 2 | O | **Y** | — | **Cyclical** | Implied | ⇀ | HH | TERM_EXIT | rich | N |
| 17 | Da Zhuang(#34)→Jin(#35) | 4 | 3 | 1 | Qia→Kan | **Y** | 3 | MI | **Y** | — | **Cyclical** | Implied | ⇀ | HH | NONE | free | **Y** |
| 18 | Ming Yi(#36)→Jia Ren(#37) | 2 | 0 | 2 | Kan→Kan | N | 1 | OM | N | Lo:Fire | Causal | Direct | → | HH | NONE | free | N |
| 19 | Kui(#38)→Jian(#39) | 6 | 3 | 3 | Kan→Kan | N | 6 | id | **Y** | — | Causal | Direct | → | HH | NONE | free | N |
| 20 | Xie(#40)→Sun(#41) | 3 | 1 | 2 | Kan→Kun | **Y** | 2 | I | N | — | Causal | Direct | → | HH | NONE | free | **Y** |
| 21 | Yi(#42)→Guai(#43) | 4 | 2 | 2 | Kun→Qia | **Y** | 5 | OM | N | — | **Cyclical** | Direct | → | HH | NONE | free | **Y** |
| 22 | Gou(#44)→Cui(#45) | 3 | 2 | 1 | Qia→Kan | **Y** | 3 | OMI | **Y** | — | Causal | Direct | ⇀ | HH | NONE | free | **Y** |
| 23 | Sheng(#46)→Kun(#47) | 3 | 1 | 2 | Kan→Kan | N | 5 | M | N | — | **Cyclical** | Direct | → | HH | NONE | free | N |
| 24 | Jing(#48)→Ge(#49) | 3 | 2 | 1 | Kan→Qia | **Y** | 3 | OMI | **Y** | — | Causal | Direct | → | HH | NONE | free | **Y** |
| 25 | Ding(#50)→Zhen(#51) | 4 | 3 | 1 | Qia→Kan | **Y** | 3 | MI | **Y** | — | **Analogical** | Direct | ⇀ | HH | NONE | free | **Y** |
| 26 | Gen(#52)→Jian(#53) | 1 | 0 | 1 | Kan→Kan | N | 1 | M | N | Lo:Mtn | **Cyclical** | Implied | ⇀ | HH | INIT_ENTRY | rich | N |
| 27 | Gui Mei(#54)→Feng(#55) | 2 | 2 | 0 | Kan→Qia | **Y** | 3 | MI | **Y** | Up:Thndr | Causal | Direct | → | HH | LOCAL_EXIT | rich | **Y** |
| 28 | Lu(#56)→Xun(#57) | 3 | 1 | 2 | Qia→Kan | **Y** | 4 | I | N | — | Causal | Direct | → | HH | RE_ENTRY | rich | **Y** |
| 29 | Dui(#58)→Huan(#59) | 3 | 1 | 2 | Kan→Kun | **Y** | 2 | I | N | — | Causal | Direct | → | HH | TERM_EXIT | rich | **Y** |
| 30 | Jie(#60)→Zhong Fu(#61) | 1 | 0 | 1 | Kun→Kun | N | 0 | O | **Y** | Lo:Lake | Causal | Direct | → | HH | NONE | free | N |
| 31 | Xiao Guo(#62)→Ji Ji(#63) | 3 | 1 | 2 | Qia→Kan | **Y** | 3 | OMI | **Y** | — | Causal | Implied | ⇀ | HH | NONE | free | **Y** |

## Cross-Tabulations

### Basin-crossing × Logic type

| | Causal | Cyclical | Contrastive | Temporal | Analogical | Total |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **False** | 6 | 3 | 0 | 1 | 0 | 10 |
| **True** | 14 | 5 | 1 | 0 | 1 | 21 |
| **Total** | **20** | **8** | **1** | **1** | **1** | **31** |

### Basin-crossing × Confidence

| | Direct | Implied | Total |
|---|:---:|:---:|:---:|
| **False** | 7 | 3 | 10 |
| **True** | 16 | 5 | 21 |
| **Total** | **23** | **8** | **31** |

### Basin-crossing × Regime

| | free | rich | Total |
|---|:---:|:---:|:---:|
| **False** | 4 | 6 | 10 |
| **True** | 7 | 14 | 21 |
| **Total** | **11** | **20** | **31** |

### H-kernel × Logic type

| | Causal | Cyclical | Contrastive | Temporal | Analogical | Total |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **False** | 8 | 5 | 0 | 1 | 0 | 14 |
| **True** | 12 | 3 | 1 | 0 | 1 | 17 |
| **Total** | **20** | **8** | **1** | **1** | **1** | **31** |

### H-kernel × Confidence

| | Direct | Implied | Total |
|---|:---:|:---:|:---:|
| **False** | 12 | 2 | 14 |
| **True** | 11 | 6 | 17 |
| **Total** | **23** | **8** | **31** |

### Corridor category × Basin-crossing

| | False | True | Total |
|---|:---:|:---:|:---:|
| **EXIT** | 2 | 5 | 7 |
| **ENTRY** | 2 | 4 | 6 |
| **CROSS** | 2 | 4 | 6 |
| **BETWEEN** | 0 | 1 | 1 |
| **NONE** | 4 | 7 | 11 |
| **Total** | **10** | **21** | **31** |

### 互 distance distribution by regime

| Regime | d=0 | d=1 | d=2 | d=3 | d=4 | d=5 | d=6 | Mean | n |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:----:|:-:|
| rich | 0 | 4 | 5 | 8 | 2 | 1 | 0 | 2.55 | 20 |
| free | 1 | 1 | 1 | 5 | 0 | 2 | 1 | 3.09 | 11 |
