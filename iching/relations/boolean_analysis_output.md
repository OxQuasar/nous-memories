========================================================================
  THE IC SURJECTION AS A BOOLEAN FUNCTION
========================================================================

  ====================================================================
  1. ALGEBRAIC NORMAL FORM (ANF) OVER Z₅
  ====================================================================

  f = [2, 0, 4, 3, 2, 1, 0, 3]
  f(x₂x₁x₀) = Σ_S a_S · m_S(x) mod 5

  ANF coefficients:
    a_{1} = 2
    a_{x₀} = 3
    a_{x₁} = 2
    a_{x₀x₁} = 1
    a_{x₀x₂} = 1
    a_{x₁x₂} = 1
    a_{x₀x₁x₂} = 3

  Full polynomial:
  f = 2 + 3x₀ + 2x₁ + x₀x₁ + x₀x₂ + x₁x₂ + 3x₀x₁x₂ (mod 5)
  Verification: ✓

  Algebraic degree: 3
  Nonzero coefficients: 7/8

  ====================================================================
  2. COMPLEMENT CONSTRAINT IN ANF FORM
  ====================================================================

  f(x⊕111) = -f(x) mod 5 implies:
  For each T: Σ_{S⊇T} a_S ≡ -a_T mod 5
  i.e., 2·a_T + Σ_{S⊋T} a_S ≡ 0 mod 5

  T=      1 (|T|=0,even):         2·2+1=0 ≡ 0? ✓  [2a_T+Σsup=0]
  T=     x₀ (|T|=1, odd):          Σsup=0 ≡ 0? ✓  [Σsup=0]
  T=     x₁ (|T|=1, odd):          Σsup=0 ≡ 0? ✓  [Σsup=0]
  T=   x₀x₁ (|T|=2,even):         2·1+3=0 ≡ 0? ✓  [2a_T+Σsup=0]
  T=     x₂ (|T|=1, odd):          Σsup=0 ≡ 0? ✓  [Σsup=0]
  T=   x₀x₂ (|T|=2,even):         2·1+3=0 ≡ 0? ✓  [2a_T+Σsup=0]
  T=   x₁x₂ (|T|=2,even):         2·1+3=0 ≡ 0? ✓  [2a_T+Σsup=0]
  T= x₀x₁x₂ (|T|=3, odd):          Σsup=0 ≡ 0? ✓  [Σsup=0]

  General constraints for ANY complement-respecting surjection:

  Even |T|: 2a_T + Σ_{S⊋T} a_S = 0 mod 5 → a_T = 3·(-Σ_{S⊋T} a_S) mod 5
  Odd |T|:  Σ_{S⊋T} a_S = 0 mod 5

  Degree 3 (|T|=3, odd): No supersets → 0 = 0. Always true. a₇ is FREE.
  Degree 2 (|T|=2, even): 2a_{ij} + a_{ijk} = 0 → a_{ij} = 2·a₇
  Degree 1 (|T|=1, odd): Σ_{S⊋T} a_S = a_{ij}+a_{ik}+a_{ijk} = 2a₇+2a₇+a₇ = 5a₇ = 0 ✓
    → Degree-1 coefficients a₁, a₂, a₄ are UNCONSTRAINED (always satisfied)
  Degree 0 (|T|=0, even): 2a₀ + (a₁+a₂+a₄) + 3·(2a₇) + a₇ = 0
    → 2a₀ + (a₁+a₂+a₄) + 7a₇ = 0 → a₀ = 3·(-(a₁+a₂+a₄) - 2a₇) mod 5

  FREE PARAMETERS: a₁, a₂, a₄, a₇ (4 free, each ∈ Z₅)
  DETERMINED: a₀ from above, a₃=a₅=a₆ = 2a₇
  Total complement-respecting functions: 5⁴ = 625 (of which 240 surjective)

  a_{x₀x₁} = 1, 2·a_{x₀x₁x₂} = 1: ✓
  a_{x₀x₂} = 1, 2·a_{x₀x₁x₂} = 1: ✓
  a_{x₁x₂} = 1, 2·a_{x₀x₁x₂} = 1: ✓

  ====================================================================
  3. INDICATOR FUNCTIONS AND WALSH SPECTRA
  ====================================================================

  g_0(x) = [f(x) = 0] (Wood)
    Support: 2 (['001', '110'])
    Algebraic degree: 2
    ANF: x₀ ⊕ x₀x₁ ⊕ x₀x₂ ⊕ x₁x₂
    Walsh: {ĝ(000)=4, ĝ(001)=0, ĝ(010)=0, ĝ(011)=4, ĝ(100)=0, ĝ(101)=4, ĝ(110)=-4, ĝ(111)=0}
    Nonlinearity: 2.0

  g_1(x) = [f(x) = 1] (Fire)
    Support: 1 (['101'])
    Algebraic degree: 3
    ANF: x₀x₂ ⊕ x₀x₁x₂
    Walsh: {ĝ(000)=6, ĝ(001)=2, ĝ(010)=-2, ĝ(011)=2, ĝ(100)=2, ĝ(101)=-2, ĝ(110)=2, ĝ(111)=-2}
    Nonlinearity: 1.0

  g_2(x) = [f(x) = 2] (Earth)
    Support: 2 (['000', '100'])
    Algebraic degree: 2
    ANF: 1 ⊕ x₀ ⊕ x₁ ⊕ x₀x₁
    Walsh: {ĝ(000)=4, ĝ(001)=-4, ĝ(010)=-4, ĝ(011)=-4, ĝ(100)=0, ĝ(101)=0, ĝ(110)=0, ĝ(111)=0}
    Nonlinearity: 2.0

  g_3(x) = [f(x) = 3] (Metal)
    Support: 2 (['011', '111'])
    Algebraic degree: 2
    ANF: x₀x₁
    Walsh: {ĝ(000)=4, ĝ(001)=4, ĝ(010)=4, ĝ(011)=-4, ĝ(100)=0, ĝ(101)=0, ĝ(110)=0, ĝ(111)=0}
    Nonlinearity: 2.0

  g_4(x) = [f(x) = 4] (Water)
    Support: 1 (['010'])
    Algebraic degree: 3
    ANF: x₁ ⊕ x₀x₁ ⊕ x₁x₂ ⊕ x₀x₁x₂
    Walsh: {ĝ(000)=6, ĝ(001)=-2, ĝ(010)=2, ĝ(011)=2, ĝ(100)=-2, ĝ(101)=-2, ĝ(110)=2, ĝ(111)=2}
    Nonlinearity: 1.0

  ====================================================================
  4. ANF COMPARISON ACROSS ALL 5 ORBITS
  ====================================================================

  Orbit  Size                         f                ANF coeffs Deg #NZ
  -------------------------------------------------------------------
      0    96  [1, 0, 1, 2, 3, 4, 0, 4]  [1, 4, 0, 2, 2, 2, 2, 1]   3   7 ★
      1    48  [0, 1, 1, 2, 3, 4, 4, 0]  [0, 1, 1, 0, 3, 0, 0, 0]   1   3
      2    48  [1, 0, 2, 2, 3, 3, 0, 4]  [1, 4, 1, 1, 2, 1, 1, 3]   3   8
      3    24  [0, 0, 1, 2, 3, 4, 0, 0]  [0, 0, 1, 1, 3, 1, 1, 3]   3   6
      4    24  [1, 0, 0, 2, 3, 0, 0, 4]  [1, 4, 4, 3, 2, 3, 3, 4]   3   8

  ANF structure orbit-invariance check:
    Orbit 0: deg ({1, 3}), #NZ ({8, 4, 7}), 5 coeff patterns ★
    Orbit 1: deg ({1, 3}), #NZ ({3, 7}), 2 coeff patterns
    Orbit 2: deg ({1, 3}), #NZ ({8, 4}), 2 coeff patterns
    Orbit 3: deg ✓, #NZ ✓, 3 coeff patterns
    Orbit 4: deg ✓, #NZ ✓, 1 coeff patterns

  UNIVERSAL ANF PROPERTIES (all 240 surjections):

  Full complement constraint (parity-correct): ✓
  a_{ij} = 2·a_{012} mod 5: ✓
  a₀ = 3·(-(a₁+a₂+a₄) - 2a₇): ✓
  a_{x₀} distribution: {0: 24, 1: 54, 2: 54, 3: 54, 4: 54}
  a_{x₁} distribution: {0: 24, 1: 54, 2: 54, 3: 54, 4: 54}
  a_{x₂} distribution: {0: 24, 1: 54, 2: 54, 3: 54, 4: 54}

  Distinct ANF coefficient vectors: 240
  Distribution by a₇: {0: 48, 1: 48, 2: 48, 3: 48, 4: 48}

  Total complement-respecting functions: 625 (= 5⁴ = 625)
  Of which surjective: 240 (should = 240)
  ====================================================================
  SUMMARY
  ====================================================================

  1. PARAMETRIZATION: Complement-respecting functions F₂³ → Z₅
     are parametrized by 4 free coefficients (a₁, a₂, a₄, a₇) ∈ Z₅⁴.
     Total: 5⁴ = 625 functions. Of these, 240 are surjective.

  2. UNIVERSAL RELATION: a_{x₀x₁} = a_{x₀x₂} = a_{x₁x₂} = 2·a₇ mod 5
     All degree-2 coefficients are locked to the cubic coefficient.
     a₀ is determined by a₁ + a₂ + a₄ + 2a₇.

  3. DEGREE-1 COEFFICIENTS (a₁, a₂, a₄) break the S₃ symmetry of
     the Boolean cube. They are the 'orientation' parameters that
     distinguish surjections within the same orbit.

  4. a₇ (the cubic coefficient) determines the 'type' of the
     surjection modulo orientation. Distribution: 48 surjections/value.
     a₇ = 0 forces all degree-2 coefficients to 0 (degree ≤ 1).

  5. IC SURJECTION:
     f = 2 + 3x₀ + 2x₁ + x₀x₁ + x₀x₂ + x₁x₂ + 3x₀x₁x₂ (mod 5)
     (a₁,a₂,a₄,a₇) = (3,2,0,3)
