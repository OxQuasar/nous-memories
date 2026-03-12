========================================================================
  FIVE-ORBIT DECOMPOSITION AT (3,5)
========================================================================

  Domain: F₂³ (8 elements)
  Target: Z₅
  Complement pairs: [(0, 7), (1, 6), (2, 5), (3, 4)]
  Negation pairs in Z₅: {1,4}, {2,3}

  Total surjections: 240
  Fiber shapes:
    [2, 2, 2, 1, 1]: 192 surjections
    [4, 1, 1, 1, 1]: 48 surjections

  |Stab(111)| = 24
  |Aut(Z₅)| = 4
  |G| = |Stab × Aut| = 96

  Number of orbits: 5
  Orbit sizes: [96, 48, 48, 24, 24]
  Total: 240 (should be 240)

  ====================================================================
  ORBIT DETAILS
  ====================================================================

  ─── Orbit 0 (★ I CHING ORBIT) ───
    Size: 96
    Fiber shape: [2, 2, 2, 1, 1]
    Type distribution: (2, 0, 2, 1)
    Action free: yes
    |Stabilizer|: 1
    ★ Contains the I Ching surjection
    IC map: [2, 0, 4, 3, 2, 1, 0, 3]
      000 (坤) → 2 (Earth)
      001 (震) → 0 (Wood)
      010 (坎) → 4 (Water)
      011 (兌) → 3 (Metal)
      100 (艮) → 2 (Earth)
      101 (離) → 1 (Fire)
      110 (巽) → 0 (Wood)
      111 (乾) → 3 (Metal)
    Representative: [1, 0, 1, 2, 3, 4, 0, 4]
      000 → 1,  ~000=111 → 4  (sum mod 5 = 0)
      001 → 0,  ~001=110 → 0  (sum mod 5 = 0)
      010 → 1,  ~010=101 → 4  (sum mod 5 = 0)
      011 → 2,  ~011=100 → 3  (sum mod 5 = 0)
      100 → 3,  ~100=011 → 2  (sum mod 5 = 0)
      101 → 4,  ~101=010 → 1  (sum mod 5 = 0)
      110 → 0,  ~110=001 → 0  (sum mod 5 = 0)
      111 → 4,  ~111=000 → 1  (sum mod 5 = 0)
    Complement constraint verified: True
    Type distributions in orbit: {(2, 0, 2, 1): 16, (2, 0, 1, 2): 16, (2, 2, 0, 1): 16, (2, 2, 1, 0): 16, (2, 1, 0, 2): 16, (2, 1, 2, 0): 16}
    Frame (000) values in orbit: {1: 24, 2: 24, 3: 24, 4: 24}

  ─── Orbit 1 ───
    Size: 48
    Fiber shape: [2, 2, 2, 1, 1]
    Type distribution: (0, 2, 2, 1)
    Action free: no
    |Stabilizer|: 2
    Representative: [0, 1, 1, 2, 3, 4, 4, 0]
      000 → 0,  ~000=111 → 0  (sum mod 5 = 0)
      001 → 1,  ~001=110 → 4  (sum mod 5 = 0)
      010 → 1,  ~010=101 → 4  (sum mod 5 = 0)
      011 → 2,  ~011=100 → 3  (sum mod 5 = 0)
      100 → 3,  ~100=011 → 2  (sum mod 5 = 0)
      101 → 4,  ~101=010 → 1  (sum mod 5 = 0)
      110 → 4,  ~110=001 → 1  (sum mod 5 = 0)
      111 → 0,  ~111=000 → 0  (sum mod 5 = 0)
    Complement constraint verified: True
    Type distributions in orbit: {(0, 2, 2, 1): 16, (0, 2, 1, 2): 16, (0, 1, 2, 2): 16}
    Frame (000) values in orbit: {0: 48}

  ─── Orbit 2 ───
    Size: 48
    Fiber shape: [2, 2, 2, 1, 1]
    Type distribution: (1, 0, 2, 2)
    Action free: no
    |Stabilizer|: 2
    Representative: [1, 0, 2, 2, 3, 3, 0, 4]
      000 → 1,  ~000=111 → 4  (sum mod 5 = 0)
      001 → 0,  ~001=110 → 0  (sum mod 5 = 0)
      010 → 2,  ~010=101 → 3  (sum mod 5 = 0)
      011 → 2,  ~011=100 → 3  (sum mod 5 = 0)
      100 → 3,  ~100=011 → 2  (sum mod 5 = 0)
      101 → 3,  ~101=010 → 2  (sum mod 5 = 0)
      110 → 0,  ~110=001 → 0  (sum mod 5 = 0)
      111 → 4,  ~111=000 → 1  (sum mod 5 = 0)
    Complement constraint verified: True
    Type distributions in orbit: {(1, 0, 2, 2): 16, (1, 2, 0, 2): 16, (1, 2, 2, 0): 16}
    Frame (000) values in orbit: {1: 12, 2: 12, 3: 12, 4: 12}

  ─── Orbit 3 ───
    Size: 24
    Fiber shape: [4, 1, 1, 1, 1]
    Type distribution: (0, 0, 1, 1)
    Action free: no
    |Stabilizer|: 4
    Representative: [0, 0, 1, 2, 3, 4, 0, 0]
      000 → 0,  ~000=111 → 0  (sum mod 5 = 0)
      001 → 0,  ~001=110 → 0  (sum mod 5 = 0)
      010 → 1,  ~010=101 → 4  (sum mod 5 = 0)
      011 → 2,  ~011=100 → 3  (sum mod 5 = 0)
      100 → 3,  ~100=011 → 2  (sum mod 5 = 0)
      101 → 4,  ~101=010 → 1  (sum mod 5 = 0)
      110 → 0,  ~110=001 → 0  (sum mod 5 = 0)
      111 → 0,  ~111=000 → 0  (sum mod 5 = 0)
    Complement constraint verified: True
    Type distributions in orbit: {(0, 0, 1, 1): 8, (0, 1, 0, 1): 8, (0, 1, 1, 0): 8}
    Frame (000) values in orbit: {0: 24}

  ─── Orbit 4 ───
    Size: 24
    Fiber shape: [4, 1, 1, 1, 1]
    Type distribution: (1, 0, 0, 1)
    Action free: no
    |Stabilizer|: 4
    Representative: [1, 0, 0, 2, 3, 0, 0, 4]
      000 → 1,  ~000=111 → 4  (sum mod 5 = 0)
      001 → 0,  ~001=110 → 0  (sum mod 5 = 0)
      010 → 0,  ~010=101 → 0  (sum mod 5 = 0)
      011 → 2,  ~011=100 → 3  (sum mod 5 = 0)
      100 → 3,  ~100=011 → 2  (sum mod 5 = 0)
      101 → 0,  ~101=010 → 0  (sum mod 5 = 0)
      110 → 0,  ~110=001 → 0  (sum mod 5 = 0)
      111 → 4,  ~111=000 → 1  (sum mod 5 = 0)
    Complement constraint verified: True
    Type distributions in orbit: {(1, 0, 0, 1): 8, (1, 0, 1, 0): 8, (1, 1, 0, 0): 8}
    Frame (000) values in orbit: {1: 6, 2: 6, 3: 6, 4: 6}

  ====================================================================
  SUMMARY TABLE
  ====================================================================

  Orbit  Size           Shape       Type Dist  Free |Stab|  IC
  -------------------------------------------------------
      0    96 [2, 2, 2, 1, 1]    (2, 0, 2, 1)   yes      1   ★
      1    48 [2, 2, 2, 1, 1]    (0, 2, 2, 1)    no      2    
      2    48 [2, 2, 2, 1, 1]    (1, 0, 2, 2)    no      2    
      3    24 [4, 1, 1, 1, 1]    (0, 0, 1, 1)    no      4    
      4    24 [4, 1, 1, 1, 1]    (1, 0, 0, 1)    no      4    
  -------------------------------------------------------
  Total   240

  KEY FINDING:
  The I Ching orbit is the UNIQUE orbit where the action is
  REGULAR (free + transitive): orbit size = |G| = 96.
  No other orbit has size 96.

  Largest orbits: [0] (size 96)
  Orbits have different sizes: [24, 48, 96]
