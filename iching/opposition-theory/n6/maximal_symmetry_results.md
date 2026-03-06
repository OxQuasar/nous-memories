======================================================================
MAXIMAL SYMMETRY GROUP OF THE KW PAIRING IN B₆
======================================================================

  B₆ = hyperoctahedral group on 6 bits
  |B₆| = 2⁶ × 6! = 46080
  Each element: permute bit positions + selectively flip bits

## Known Z₂² Symmetries
  identity: perm=(0, 1, 2, 3, 4, 5), flip=000000, preserves KW: True
  complement: perm=(0, 1, 2, 3, 4, 5), flip=111111, preserves KW: True
  reversal: perm=(5, 4, 3, 2, 1, 0), flip=000000, preserves KW: True
  comp∘rev: perm=(5, 4, 3, 2, 1, 0), flip=111111, preserves KW: True

## Enumerating Stabilizer
  Checking all 46,080 elements of B₆...
  Found 384 elements preserving KW (1.6s)

## Stabilizer Elements

  Pure permutations (no flips): 48
    id  order=1  perm=(0, 1, 2, 3, 4, 5)
    (3 4)  order=2  perm=(0, 1, 3, 2, 4, 5)
    (2 3)(4 5)  order=2  perm=(0, 2, 1, 4, 3, 5)
    (2 3 5 4)  order=4  perm=(0, 2, 4, 1, 3, 5)
    (2 4 5 3)  order=4  perm=(0, 3, 1, 4, 2, 5)
    (2 4)(3 5)  order=2  perm=(0, 3, 4, 1, 2, 5)
    (2 5)  order=2  perm=(0, 4, 2, 3, 1, 5)
    (2 5)(3 4)  order=2  perm=(0, 4, 3, 2, 1, 5)
    (1 2)(5 6)  order=2  perm=(1, 0, 2, 3, 5, 4)
    (1 2)(3 4)(5 6)  order=2  perm=(1, 0, 3, 2, 5, 4)
    (1 2 3)(4 6 5)  order=3  perm=(1, 2, 0, 5, 3, 4)
    (1 2 3 6 5 4)  order=6  perm=(1, 2, 5, 0, 3, 4)
    (1 2 4 6 5 3)  order=6  perm=(1, 3, 0, 5, 2, 4)
    (1 2 4)(3 6 5)  order=3  perm=(1, 3, 5, 0, 2, 4)
    (1 2 6 5)  order=4  perm=(1, 5, 2, 3, 0, 4)
    (1 2 6 5)(3 4)  order=4  perm=(1, 5, 3, 2, 0, 4)
    (1 3 2)(4 5 6)  order=3  perm=(2, 0, 1, 4, 5, 3)
    (1 3 5 6 4 2)  order=6  perm=(2, 0, 4, 1, 5, 3)
    (1 3)(4 6)  order=2  perm=(2, 1, 0, 5, 4, 3)
    (1 3 6 4)  order=4  perm=(2, 1, 5, 0, 4, 3)
    (1 3)(2 5)(4 6)  order=2  perm=(2, 4, 0, 5, 1, 3)
    (1 3 6 4)(2 5)  order=4  perm=(2, 4, 5, 0, 1, 3)
    (1 3 2 6 4 5)  order=6  perm=(2, 5, 1, 4, 0, 3)
    (1 3 5)(2 6 4)  order=3  perm=(2, 5, 4, 1, 0, 3)
    (1 4 5 6 3 2)  order=6  perm=(3, 0, 1, 4, 5, 2)
    (1 4 2)(3 5 6)  order=3  perm=(3, 0, 4, 1, 5, 2)
    (1 4 6 3)  order=4  perm=(3, 1, 0, 5, 4, 2)
    (1 4)(3 6)  order=2  perm=(3, 1, 5, 0, 4, 2)
    (1 4 6 3)(2 5)  order=4  perm=(3, 4, 0, 5, 1, 2)
    (1 4)(2 5)(3 6)  order=2  perm=(3, 4, 5, 0, 1, 2)
    (1 4 5)(2 6 3)  order=3  perm=(3, 5, 1, 4, 0, 2)
    (1 4 2 6 3 5)  order=6  perm=(3, 5, 4, 1, 0, 2)
    (1 5 6 2)  order=4  perm=(4, 0, 2, 3, 5, 1)
    (1 5 6 2)(3 4)  order=4  perm=(4, 0, 3, 2, 5, 1)
    (1 5 4 6 2 3)  order=6  perm=(4, 2, 0, 5, 3, 1)
    (1 5 4)(2 3 6)  order=3  perm=(4, 2, 5, 0, 3, 1)
    (1 5 3)(2 4 6)  order=3  perm=(4, 3, 0, 5, 2, 1)
    (1 5 3 6 2 4)  order=6  perm=(4, 3, 5, 0, 2, 1)
    (1 5)(2 6)  order=2  perm=(4, 5, 2, 3, 0, 1)
    (1 5)(2 6)(3 4)  order=2  perm=(4, 5, 3, 2, 0, 1)
    (1 6)  order=2  perm=(5, 1, 2, 3, 4, 0)
    (1 6)(3 4)  order=2  perm=(5, 1, 3, 2, 4, 0)
    (1 6)(2 3)(4 5)  order=2  perm=(5, 2, 1, 4, 3, 0)
    (1 6)(2 3 5 4)  order=4  perm=(5, 2, 4, 1, 3, 0)
    (1 6)(2 4 5 3)  order=4  perm=(5, 3, 1, 4, 2, 0)
    (1 6)(2 4)(3 5)  order=2  perm=(5, 3, 4, 1, 2, 0)
    (1 6)(2 5)  order=2  perm=(5, 4, 2, 3, 1, 0)
    (1 6)(2 5)(3 4)  order=2  perm=(5, 4, 3, 2, 1, 0)

  Pure flips (no permutation): 8
    id  order=1  flip=000000
    flip{3,4}  order=2  flip=001100
    flip{2,5}  order=2  flip=010010
    flip{2,3,4,5}  order=2  flip=011110
    flip{1,6}  order=2  flip=100001
    flip{1,3,4,6}  order=2  flip=101101
    flip{1,2,5,6}  order=2  flip=110011
    flip{1,2,3,4,5,6}  order=2  flip=111111

  Mixed (permutation + flip): 329
    (3 4) ∘ flip{3,4}  order=2
    (3 4) ∘ flip{2,5}  order=2
    (3 4) ∘ flip{2,3,4,5}  order=2
    (3 4) ∘ flip{1,6}  order=2
    (3 4) ∘ flip{1,3,4,6}  order=2
    (3 4) ∘ flip{1,2,5,6}  order=2
    (3 4) ∘ flip{1,2,3,4,5,6}  order=2
    (2 3)(4 5) ∘ flip{3,4}  order=4
    (2 3)(4 5) ∘ flip{2,5}  order=4
    (2 3)(4 5) ∘ flip{2,3,4,5}  order=2
    (2 3)(4 5) ∘ flip{1,6}  order=2
    (2 3)(4 5) ∘ flip{1,3,4,6}  order=4
    (2 3)(4 5) ∘ flip{1,2,5,6}  order=4
    (2 3)(4 5) ∘ flip{1,2,3,4,5,6}  order=2
    (2 3 5 4) ∘ flip{3,4}  order=4
    (2 3 5 4) ∘ flip{2,5}  order=4
    (2 3 5 4) ∘ flip{2,3,4,5}  order=4
    (2 3 5 4) ∘ flip{1,6}  order=4
    (2 3 5 4) ∘ flip{1,3,4,6}  order=4
    (2 3 5 4) ∘ flip{1,2,5,6}  order=4
    (2 3 5 4) ∘ flip{1,2,3,4,5,6}  order=4
    (2 4 5 3) ∘ flip{3,4}  order=4
    (2 4 5 3) ∘ flip{2,5}  order=4
    (2 4 5 3) ∘ flip{2,3,4,5}  order=4
    (2 4 5 3) ∘ flip{1,6}  order=4
    (2 4 5 3) ∘ flip{1,3,4,6}  order=4
    (2 4 5 3) ∘ flip{1,2,5,6}  order=4
    (2 4 5 3) ∘ flip{1,2,3,4,5,6}  order=4
    (2 4)(3 5) ∘ flip{3,4}  order=4
    (2 4)(3 5) ∘ flip{2,5}  order=4
    (2 4)(3 5) ∘ flip{2,3,4,5}  order=2
    (2 4)(3 5) ∘ flip{1,6}  order=2
    (2 4)(3 5) ∘ flip{1,3,4,6}  order=4
    (2 4)(3 5) ∘ flip{1,2,5,6}  order=4
    (2 4)(3 5) ∘ flip{1,2,3,4,5,6}  order=2
    (2 5) ∘ flip{3,4}  order=2
    (2 5) ∘ flip{2,5}  order=2
    (2 5) ∘ flip{2,3,4,5}  order=2
    (2 5) ∘ flip{1,6}  order=2
    (2 5) ∘ flip{1,3,4,6}  order=2
    (2 5) ∘ flip{1,2,5,6}  order=2
    (2 5) ∘ flip{1,2,3,4,5,6}  order=2
    (2 5)(3 4) ∘ flip{3,4}  order=2
    (2 5)(3 4) ∘ flip{2,5}  order=2
    (2 5)(3 4) ∘ flip{2,3,4,5}  order=2
    (2 5)(3 4) ∘ flip{1,6}  order=2
    (2 5)(3 4) ∘ flip{1,3,4,6}  order=2
    (2 5)(3 4) ∘ flip{1,2,5,6}  order=2
    (2 5)(3 4) ∘ flip{1,2,3,4,5,6}  order=2
    (1 2)(5 6) ∘ flip{3,4}  order=2
    (1 2)(5 6) ∘ flip{2,5}  order=4
    (1 2)(5 6) ∘ flip{2,3,4,5}  order=4
    (1 2)(5 6) ∘ flip{1,6}  order=4
    (1 2)(5 6) ∘ flip{1,3,4,6}  order=4
    (1 2)(5 6) ∘ flip{1,2,5,6}  order=2
    (1 2)(5 6) ∘ flip{1,2,3,4,5,6}  order=2
    (1 2)(3 4)(5 6) ∘ flip{3,4}  order=2
    (1 2)(3 4)(5 6) ∘ flip{2,5}  order=4
    (1 2)(3 4)(5 6) ∘ flip{2,3,4,5}  order=4
    (1 2)(3 4)(5 6) ∘ flip{1,6}  order=4
    (1 2)(3 4)(5 6) ∘ flip{1,3,4,6}  order=4
    (1 2)(3 4)(5 6) ∘ flip{1,2,5,6}  order=2
    (1 2)(3 4)(5 6) ∘ flip{1,2,3,4,5,6}  order=2
    (1 2 3)(4 6 5) ∘ flip{3,4}  order=6
    (1 2 3)(4 6 5) ∘ flip{2,5}  order=6
    (1 2 3)(4 6 5) ∘ flip{2,3,4,5}  order=3
    (1 2 3)(4 6 5) ∘ flip{1,6}  order=6
    (1 2 3)(4 6 5) ∘ flip{1,3,4,6}  order=3
    (1 2 3)(4 6 5) ∘ flip{1,2,5,6}  order=3
    (1 2 3)(4 6 5) ∘ flip{1,2,3,4,5,6}  order=6
    (1 2 3 6 5 4) ∘ flip{3,4}  order=6
    (1 2 3 6 5 4) ∘ flip{2,5}  order=6
    (1 2 3 6 5 4) ∘ flip{2,3,4,5}  order=6
    (1 2 3 6 5 4) ∘ flip{1,6}  order=6
    (1 2 3 6 5 4) ∘ flip{1,3,4,6}  order=6
    (1 2 3 6 5 4) ∘ flip{1,2,5,6}  order=6
    (1 2 3 6 5 4) ∘ flip{1,2,3,4,5,6}  order=6
    (1 2 4 6 5 3) ∘ flip{3,4}  order=6
    (1 2 4 6 5 3) ∘ flip{2,5}  order=6
    (1 2 4 6 5 3) ∘ flip{2,3,4,5}  order=6
    (1 2 4 6 5 3) ∘ flip{1,6}  order=6
    (1 2 4 6 5 3) ∘ flip{1,3,4,6}  order=6
    (1 2 4 6 5 3) ∘ flip{1,2,5,6}  order=6
    (1 2 4 6 5 3) ∘ flip{1,2,3,4,5,6}  order=6
    (1 2 4)(3 6 5) ∘ flip{3,4}  order=6
    (1 2 4)(3 6 5) ∘ flip{2,5}  order=6
    (1 2 4)(3 6 5) ∘ flip{2,3,4,5}  order=3
    (1 2 4)(3 6 5) ∘ flip{1,6}  order=6
    (1 2 4)(3 6 5) ∘ flip{1,3,4,6}  order=3
    (1 2 4)(3 6 5) ∘ flip{1,2,5,6}  order=3
    (1 2 4)(3 6 5) ∘ flip{1,2,3,4,5,6}  order=6
    (1 2 6 5) ∘ flip{3,4}  order=4
    (1 2 6 5) ∘ flip{2,5}  order=4
    (1 2 6 5) ∘ flip{2,3,4,5}  order=4
    (1 2 6 5) ∘ flip{1,6}  order=4
    (1 2 6 5) ∘ flip{1,3,4,6}  order=4
    (1 2 6 5) ∘ flip{1,2,5,6}  order=4
    (1 2 6 5) ∘ flip{1,2,3,4,5,6}  order=4
    (1 2 6 5)(3 4) ∘ flip{3,4}  order=4
    (1 2 6 5)(3 4) ∘ flip{2,5}  order=4
    (1 2 6 5)(3 4) ∘ flip{2,3,4,5}  order=4
    (1 2 6 5)(3 4) ∘ flip{1,6}  order=4
    (1 2 6 5)(3 4) ∘ flip{1,3,4,6}  order=4
    (1 2 6 5)(3 4) ∘ flip{1,2,5,6}  order=4
    (1 2 6 5)(3 4) ∘ flip{1,2,3,4,5,6}  order=4
    (1 3 2)(4 5 6) ∘ flip{3,4}  order=6
    (1 3 2)(4 5 6) ∘ flip{2,5}  order=6
    (1 3 2)(4 5 6) ∘ flip{2,3,4,5}  order=3
    (1 3 2)(4 5 6) ∘ flip{1,6}  order=6
    (1 3 2)(4 5 6) ∘ flip{1,3,4,6}  order=3
    (1 3 2)(4 5 6) ∘ flip{1,2,5,6}  order=3
    (1 3 2)(4 5 6) ∘ flip{1,2,3,4,5,6}  order=6
    (1 3 5 6 4 2) ∘ flip{3,4}  order=6
    (1 3 5 6 4 2) ∘ flip{2,5}  order=6
    (1 3 5 6 4 2) ∘ flip{2,3,4,5}  order=6
    (1 3 5 6 4 2) ∘ flip{1,6}  order=6
    (1 3 5 6 4 2) ∘ flip{1,3,4,6}  order=6
    (1 3 5 6 4 2) ∘ flip{1,2,5,6}  order=6
    (1 3 5 6 4 2) ∘ flip{1,2,3,4,5,6}  order=6
    (1 3)(4 6) ∘ flip{3,4}  order=4
    (1 3)(4 6) ∘ flip{2,5}  order=2
    (1 3)(4 6) ∘ flip{2,3,4,5}  order=4
    (1 3)(4 6) ∘ flip{1,6}  order=4
    (1 3)(4 6) ∘ flip{1,3,4,6}  order=2
    (1 3)(4 6) ∘ flip{1,2,5,6}  order=4
    (1 3)(4 6) ∘ flip{1,2,3,4,5,6}  order=2
    (1 3 6 4) ∘ flip{3,4}  order=4
    (1 3 6 4) ∘ flip{2,5}  order=4
    (1 3 6 4) ∘ flip{2,3,4,5}  order=4
    (1 3 6 4) ∘ flip{1,6}  order=4
    (1 3 6 4) ∘ flip{1,3,4,6}  order=4
    (1 3 6 4) ∘ flip{1,2,5,6}  order=4
    (1 3 6 4) ∘ flip{1,2,3,4,5,6}  order=4
    (1 3)(2 5)(4 6) ∘ flip{3,4}  order=4
    (1 3)(2 5)(4 6) ∘ flip{2,5}  order=2
    (1 3)(2 5)(4 6) ∘ flip{2,3,4,5}  order=4
    (1 3)(2 5)(4 6) ∘ flip{1,6}  order=4
    (1 3)(2 5)(4 6) ∘ flip{1,3,4,6}  order=2
    (1 3)(2 5)(4 6) ∘ flip{1,2,5,6}  order=4
    (1 3)(2 5)(4 6) ∘ flip{1,2,3,4,5,6}  order=2
    (1 3 6 4)(2 5) ∘ flip{3,4}  order=4
    (1 3 6 4)(2 5) ∘ flip{2,5}  order=4
    (1 3 6 4)(2 5) ∘ flip{2,3,4,5}  order=4
    (1 3 6 4)(2 5) ∘ flip{1,6}  order=4
    (1 3 6 4)(2 5) ∘ flip{1,3,4,6}  order=4
    (1 3 6 4)(2 5) ∘ flip{1,2,5,6}  order=4
    (1 3 6 4)(2 5) ∘ flip{1,2,3,4,5,6}  order=4
    (1 3 2 6 4 5) ∘ flip{3,4}  order=6
    (1 3 2 6 4 5) ∘ flip{2,5}  order=6
    (1 3 2 6 4 5) ∘ flip{2,3,4,5}  order=6
    (1 3 2 6 4 5) ∘ flip{1,6}  order=6
    (1 3 2 6 4 5) ∘ flip{1,3,4,6}  order=6
    (1 3 2 6 4 5) ∘ flip{1,2,5,6}  order=6
    (1 3 2 6 4 5) ∘ flip{1,2,3,4,5,6}  order=6
    (1 3 5)(2 6 4) ∘ flip{3,4}  order=6
    (1 3 5)(2 6 4) ∘ flip{2,5}  order=6
    (1 3 5)(2 6 4) ∘ flip{2,3,4,5}  order=3
    (1 3 5)(2 6 4) ∘ flip{1,6}  order=6
    (1 3 5)(2 6 4) ∘ flip{1,3,4,6}  order=3
    (1 3 5)(2 6 4) ∘ flip{1,2,5,6}  order=3
    (1 3 5)(2 6 4) ∘ flip{1,2,3,4,5,6}  order=6
    (1 4 5 6 3 2) ∘ flip{3,4}  order=6
    (1 4 5 6 3 2) ∘ flip{2,5}  order=6
    (1 4 5 6 3 2) ∘ flip{2,3,4,5}  order=6
    (1 4 5 6 3 2) ∘ flip{1,6}  order=6
    (1 4 5 6 3 2) ∘ flip{1,3,4,6}  order=6
    (1 4 5 6 3 2) ∘ flip{1,2,5,6}  order=6
    (1 4 5 6 3 2) ∘ flip{1,2,3,4,5,6}  order=6
    (1 4 2)(3 5 6) ∘ flip{3,4}  order=6
    (1 4 2)(3 5 6) ∘ flip{2,5}  order=6
    (1 4 2)(3 5 6) ∘ flip{2,3,4,5}  order=3
    (1 4 2)(3 5 6) ∘ flip{1,6}  order=6
    (1 4 2)(3 5 6) ∘ flip{1,3,4,6}  order=3
    (1 4 2)(3 5 6) ∘ flip{1,2,5,6}  order=3
    (1 4 2)(3 5 6) ∘ flip{1,2,3,4,5,6}  order=6
    (1 4 6 3) ∘ flip{3,4}  order=4
    (1 4 6 3) ∘ flip{2,5}  order=4
    (1 4 6 3) ∘ flip{2,3,4,5}  order=4
    (1 4 6 3) ∘ flip{1,6}  order=4
    (1 4 6 3) ∘ flip{1,3,4,6}  order=4
    (1 4 6 3) ∘ flip{1,2,5,6}  order=4
    (1 4 6 3) ∘ flip{1,2,3,4,5,6}  order=4
    (1 4)(3 6) ∘ flip{3,4}  order=4
    (1 4)(3 6) ∘ flip{2,5}  order=2
    (1 4)(3 6) ∘ flip{2,3,4,5}  order=4
    (1 4)(3 6) ∘ flip{1,6}  order=4
    (1 4)(3 6) ∘ flip{1,3,4,6}  order=2
    (1 4)(3 6) ∘ flip{1,2,5,6}  order=4
    (1 4)(3 6) ∘ flip{1,2,3,4,5,6}  order=2
    (1 4 6 3)(2 5) ∘ flip{3,4}  order=4
    (1 4 6 3)(2 5) ∘ flip{2,5}  order=4
    (1 4 6 3)(2 5) ∘ flip{2,3,4,5}  order=4
    (1 4 6 3)(2 5) ∘ flip{1,6}  order=4
    (1 4 6 3)(2 5) ∘ flip{1,3,4,6}  order=4
    (1 4 6 3)(2 5) ∘ flip{1,2,5,6}  order=4
    (1 4 6 3)(2 5) ∘ flip{1,2,3,4,5,6}  order=4
    (1 4)(2 5)(3 6) ∘ flip{3,4}  order=4
    (1 4)(2 5)(3 6) ∘ flip{2,5}  order=2
    (1 4)(2 5)(3 6) ∘ flip{2,3,4,5}  order=4
    (1 4)(2 5)(3 6) ∘ flip{1,6}  order=4
    (1 4)(2 5)(3 6) ∘ flip{1,3,4,6}  order=2
    (1 4)(2 5)(3 6) ∘ flip{1,2,5,6}  order=4
    (1 4)(2 5)(3 6) ∘ flip{1,2,3,4,5,6}  order=2
    (1 4 5)(2 6 3) ∘ flip{3,4}  order=6
    (1 4 5)(2 6 3) ∘ flip{2,5}  order=6
    (1 4 5)(2 6 3) ∘ flip{2,3,4,5}  order=3
    (1 4 5)(2 6 3) ∘ flip{1,6}  order=6
    (1 4 5)(2 6 3) ∘ flip{1,3,4,6}  order=3
    (1 4 5)(2 6 3) ∘ flip{1,2,5,6}  order=3
    (1 4 5)(2 6 3) ∘ flip{1,2,3,4,5,6}  order=6
    (1 4 2 6 3 5) ∘ flip{3,4}  order=6
    (1 4 2 6 3 5) ∘ flip{2,5}  order=6
    (1 4 2 6 3 5) ∘ flip{2,3,4,5}  order=6
    (1 4 2 6 3 5) ∘ flip{1,6}  order=6
    (1 4 2 6 3 5) ∘ flip{1,3,4,6}  order=6
    (1 4 2 6 3 5) ∘ flip{1,2,5,6}  order=6
    (1 4 2 6 3 5) ∘ flip{1,2,3,4,5,6}  order=6
    (1 5 6 2) ∘ flip{3,4}  order=4
    (1 5 6 2) ∘ flip{2,5}  order=4
    (1 5 6 2) ∘ flip{2,3,4,5}  order=4
    (1 5 6 2) ∘ flip{1,6}  order=4
    (1 5 6 2) ∘ flip{1,3,4,6}  order=4
    (1 5 6 2) ∘ flip{1,2,5,6}  order=4
    (1 5 6 2) ∘ flip{1,2,3,4,5,6}  order=4
    (1 5 6 2)(3 4) ∘ flip{3,4}  order=4
    (1 5 6 2)(3 4) ∘ flip{2,5}  order=4
    (1 5 6 2)(3 4) ∘ flip{2,3,4,5}  order=4
    (1 5 6 2)(3 4) ∘ flip{1,6}  order=4
    (1 5 6 2)(3 4) ∘ flip{1,3,4,6}  order=4
    (1 5 6 2)(3 4) ∘ flip{1,2,5,6}  order=4
    (1 5 6 2)(3 4) ∘ flip{1,2,3,4,5,6}  order=4
    (1 5 4 6 2 3) ∘ flip{3,4}  order=6
    (1 5 4 6 2 3) ∘ flip{2,5}  order=6
    (1 5 4 6 2 3) ∘ flip{2,3,4,5}  order=6
    (1 5 4 6 2 3) ∘ flip{1,6}  order=6
    (1 5 4 6 2 3) ∘ flip{1,3,4,6}  order=6
    (1 5 4 6 2 3) ∘ flip{1,2,5,6}  order=6
    (1 5 4 6 2 3) ∘ flip{1,2,3,4,5,6}  order=6
    (1 5 4)(2 3 6) ∘ flip{3,4}  order=6
    (1 5 4)(2 3 6) ∘ flip{2,5}  order=6
    (1 5 4)(2 3 6) ∘ flip{2,3,4,5}  order=3
    (1 5 4)(2 3 6) ∘ flip{1,6}  order=6
    (1 5 4)(2 3 6) ∘ flip{1,3,4,6}  order=3
    (1 5 4)(2 3 6) ∘ flip{1,2,5,6}  order=3
    (1 5 4)(2 3 6) ∘ flip{1,2,3,4,5,6}  order=6
    (1 5 3)(2 4 6) ∘ flip{3,4}  order=6
    (1 5 3)(2 4 6) ∘ flip{2,5}  order=6
    (1 5 3)(2 4 6) ∘ flip{2,3,4,5}  order=3
    (1 5 3)(2 4 6) ∘ flip{1,6}  order=6
    (1 5 3)(2 4 6) ∘ flip{1,3,4,6}  order=3
    (1 5 3)(2 4 6) ∘ flip{1,2,5,6}  order=3
    (1 5 3)(2 4 6) ∘ flip{1,2,3,4,5,6}  order=6
    (1 5 3 6 2 4) ∘ flip{3,4}  order=6
    (1 5 3 6 2 4) ∘ flip{2,5}  order=6
    (1 5 3 6 2 4) ∘ flip{2,3,4,5}  order=6
    (1 5 3 6 2 4) ∘ flip{1,6}  order=6
    (1 5 3 6 2 4) ∘ flip{1,3,4,6}  order=6
    (1 5 3 6 2 4) ∘ flip{1,2,5,6}  order=6
    (1 5 3 6 2 4) ∘ flip{1,2,3,4,5,6}  order=6
    (1 5)(2 6) ∘ flip{3,4}  order=2
    (1 5)(2 6) ∘ flip{2,5}  order=4
    (1 5)(2 6) ∘ flip{2,3,4,5}  order=4
    (1 5)(2 6) ∘ flip{1,6}  order=4
    (1 5)(2 6) ∘ flip{1,3,4,6}  order=4
    (1 5)(2 6) ∘ flip{1,2,5,6}  order=2
    (1 5)(2 6) ∘ flip{1,2,3,4,5,6}  order=2
    (1 5)(2 6)(3 4) ∘ flip{3,4}  order=2
    (1 5)(2 6)(3 4) ∘ flip{2,5}  order=4
    (1 5)(2 6)(3 4) ∘ flip{2,3,4,5}  order=4
    (1 5)(2 6)(3 4) ∘ flip{1,6}  order=4
    (1 5)(2 6)(3 4) ∘ flip{1,3,4,6}  order=4
    (1 5)(2 6)(3 4) ∘ flip{1,2,5,6}  order=2
    (1 5)(2 6)(3 4) ∘ flip{1,2,3,4,5,6}  order=2
    (1 6) ∘ flip{3,4}  order=2
    (1 6) ∘ flip{2,5}  order=2
    (1 6) ∘ flip{2,3,4,5}  order=2
    (1 6) ∘ flip{1,6}  order=2
    (1 6) ∘ flip{1,3,4,6}  order=2
    (1 6) ∘ flip{1,2,5,6}  order=2
    (1 6) ∘ flip{1,2,3,4,5,6}  order=2
    (1 6)(3 4) ∘ flip{3,4}  order=2
    (1 6)(3 4) ∘ flip{2,5}  order=2
    (1 6)(3 4) ∘ flip{2,3,4,5}  order=2
    (1 6)(3 4) ∘ flip{1,6}  order=2
    (1 6)(3 4) ∘ flip{1,3,4,6}  order=2
    (1 6)(3 4) ∘ flip{1,2,5,6}  order=2
    (1 6)(3 4) ∘ flip{1,2,3,4,5,6}  order=2
    (1 6)(2 3)(4 5) ∘ flip{3,4}  order=4
    (1 6)(2 3)(4 5) ∘ flip{2,5}  order=4
    (1 6)(2 3)(4 5) ∘ flip{2,3,4,5}  order=2
    (1 6)(2 3)(4 5) ∘ flip{1,6}  order=2
    (1 6)(2 3)(4 5) ∘ flip{1,3,4,6}  order=4
    (1 6)(2 3)(4 5) ∘ flip{1,2,5,6}  order=4
    (1 6)(2 3)(4 5) ∘ flip{1,2,3,4,5,6}  order=2
    (1 6)(2 3 5 4) ∘ flip{3,4}  order=4
    (1 6)(2 3 5 4) ∘ flip{2,5}  order=4
    (1 6)(2 3 5 4) ∘ flip{2,3,4,5}  order=4
    (1 6)(2 3 5 4) ∘ flip{1,6}  order=4
    (1 6)(2 3 5 4) ∘ flip{1,3,4,6}  order=4
    (1 6)(2 3 5 4) ∘ flip{1,2,5,6}  order=4
    (1 6)(2 3 5 4) ∘ flip{1,2,3,4,5,6}  order=4
    (1 6)(2 4 5 3) ∘ flip{3,4}  order=4
    (1 6)(2 4 5 3) ∘ flip{2,5}  order=4
    (1 6)(2 4 5 3) ∘ flip{2,3,4,5}  order=4
    (1 6)(2 4 5 3) ∘ flip{1,6}  order=4
    (1 6)(2 4 5 3) ∘ flip{1,3,4,6}  order=4
    (1 6)(2 4 5 3) ∘ flip{1,2,5,6}  order=4
    (1 6)(2 4 5 3) ∘ flip{1,2,3,4,5,6}  order=4
    (1 6)(2 4)(3 5) ∘ flip{3,4}  order=4
    (1 6)(2 4)(3 5) ∘ flip{2,5}  order=4
    (1 6)(2 4)(3 5) ∘ flip{2,3,4,5}  order=2
    (1 6)(2 4)(3 5) ∘ flip{1,6}  order=2
    (1 6)(2 4)(3 5) ∘ flip{1,3,4,6}  order=4
    (1 6)(2 4)(3 5) ∘ flip{1,2,5,6}  order=4
    (1 6)(2 4)(3 5) ∘ flip{1,2,3,4,5,6}  order=2
    (1 6)(2 5) ∘ flip{3,4}  order=2
    (1 6)(2 5) ∘ flip{2,5}  order=2
    (1 6)(2 5) ∘ flip{2,3,4,5}  order=2
    (1 6)(2 5) ∘ flip{1,6}  order=2
    (1 6)(2 5) ∘ flip{1,3,4,6}  order=2
    (1 6)(2 5) ∘ flip{1,2,5,6}  order=2
    (1 6)(2 5) ∘ flip{1,2,3,4,5,6}  order=2
    (1 6)(2 5)(3 4) ∘ flip{3,4}  order=2
    (1 6)(2 5)(3 4) ∘ flip{2,5}  order=2
    (1 6)(2 5)(3 4) ∘ flip{2,3,4,5}  order=2
    (1 6)(2 5)(3 4) ∘ flip{1,6}  order=2
    (1 6)(2 5)(3 4) ∘ flip{1,3,4,6}  order=2
    (1 6)(2 5)(3 4) ∘ flip{1,2,5,6}  order=2
    (1 6)(2 5)(3 4) ∘ flip{1,2,3,4,5,6}  order=2

## Group Structure

  |Stab_B₆(KW)| = 384
  |Z₂²| = 4
  Z₂² is a PROPER subgroup of Stab_B₆(KW).
  Index [Stab : Z₂²] = 96

  Element orders: {1: 1, 2: 111, 3: 32, 4: 144, 6: 96}
  Abelian: False

  Looking for generators...
  Generators (6):
    flip{3,4}  order=2
    flip{2,5}  order=2
    flip{1,6}  order=2
    (3 4)  order=2
    (2 3)(4 5)  order=2
    (1 2)(5 6)  order=2
  Generated group size: 384 (expected 384)

## Analysis of Extra Symmetries

  Elements beyond Z₂² (380):
    flip{3,4}: 000000→001100, 000001→001101, 000010→001110, 000011→001111
    flip{2,5}: 000000→010010, 000001→010011, 000010→010000, 000011→010001
    flip{2,3,4,5}: 000000→011110, 000001→011111, 000010→011100, 000011→011101
    flip{1,6}: 000000→100001, 000001→100000, 000010→100011, 000011→100010
    flip{1,3,4,6}: 000000→101101, 000001→101100, 000010→101111, 000011→101110
    flip{1,2,5,6}: 000000→110011, 000001→110010, 000010→110001, 000011→110000
    (3 4): 000000→000000, 000001→000001, 000010→000010, 000011→000011
    (3 4) ∘ flip{3,4}: 000000→001100, 000001→001101, 000010→001110, 000011→001111
    (3 4) ∘ flip{2,5}: 000000→010010, 000001→010011, 000010→010000, 000011→010001
    (3 4) ∘ flip{2,3,4,5}: 000000→011110, 000001→011111, 000010→011100, 000011→011101
    (3 4) ∘ flip{1,6}: 000000→100001, 000001→100000, 000010→100011, 000011→100010
    (3 4) ∘ flip{1,3,4,6}: 000000→101101, 000001→101100, 000010→101111, 000011→101110
    (3 4) ∘ flip{1,2,5,6}: 000000→110011, 000001→110010, 000010→110001, 000011→110000
    (3 4) ∘ flip{1,2,3,4,5,6}: 000000→111111, 000001→111110, 000010→111101, 000011→111100
    (2 3)(4 5): 000000→000000, 000001→000001, 000010→000100, 000011→000101
    (2 3)(4 5) ∘ flip{3,4}: 000000→001100, 000001→001101, 000010→001000, 000011→001001
    (2 3)(4 5) ∘ flip{2,5}: 000000→010010, 000001→010011, 000010→010110, 000011→010111
    (2 3)(4 5) ∘ flip{2,3,4,5}: 000000→011110, 000001→011111, 000010→011010, 000011→011011
    (2 3)(4 5) ∘ flip{1,6}: 000000→100001, 000001→100000, 000010→100101, 000011→100100
    (2 3)(4 5) ∘ flip{1,3,4,6}: 000000→101101, 000001→101100, 000010→101001, 000011→101000
    ... and 360 more

  Line permutations preserving KW:
    (3 4): preserves palindromes=True
    (2 3)(4 5): preserves palindromes=True
    (2 3 5 4): preserves palindromes=True
    (2 4 5 3): preserves palindromes=True
    (2 4)(3 5): preserves palindromes=True
    (2 5): preserves palindromes=True
    (2 5)(3 4): preserves palindromes=True
    (1 2)(5 6): preserves palindromes=True
    (1 2)(3 4)(5 6): preserves palindromes=True
    (1 2 3)(4 6 5): preserves palindromes=True
    (1 2 3 6 5 4): preserves palindromes=True
    (1 2 4 6 5 3): preserves palindromes=True
    (1 2 4)(3 6 5): preserves palindromes=True
    (1 2 6 5): preserves palindromes=True
    (1 2 6 5)(3 4): preserves palindromes=True
    (1 3 2)(4 5 6): preserves palindromes=True
    (1 3 5 6 4 2): preserves palindromes=True
    (1 3)(4 6): preserves palindromes=True
    (1 3 6 4): preserves palindromes=True
    (1 3)(2 5)(4 6): preserves palindromes=True
    (1 3 6 4)(2 5): preserves palindromes=True
    (1 3 2 6 4 5): preserves palindromes=True
    (1 3 5)(2 6 4): preserves palindromes=True
    (1 4 5 6 3 2): preserves palindromes=True
    (1 4 2)(3 5 6): preserves palindromes=True
    (1 4 6 3): preserves palindromes=True
    (1 4)(3 6): preserves palindromes=True
    (1 4 6 3)(2 5): preserves palindromes=True
    (1 4)(2 5)(3 6): preserves palindromes=True
    (1 4 5)(2 6 3): preserves palindromes=True
    (1 4 2 6 3 5): preserves palindromes=True
    (1 5 6 2): preserves palindromes=True
    (1 5 6 2)(3 4): preserves palindromes=True
    (1 5 4 6 2 3): preserves palindromes=True
    (1 5 4)(2 3 6): preserves palindromes=True
    (1 5 3)(2 4 6): preserves palindromes=True
    (1 5 3 6 2 4): preserves palindromes=True
    (1 5)(2 6): preserves palindromes=True
    (1 5)(2 6)(3 4): preserves palindromes=True
    (1 6): preserves palindromes=True
    (1 6)(3 4): preserves palindromes=True
    (1 6)(2 3)(4 5): preserves palindromes=True
    (1 6)(2 3 5 4): preserves palindromes=True
    (1 6)(2 4 5 3): preserves palindromes=True
    (1 6)(2 4)(3 5): preserves palindromes=True
    (1 6)(2 5): preserves palindromes=True
    (1 6)(2 5)(3 4): preserves palindromes=True

## Structural Interpretation

  A line permutation π preserves KW iff π commutes with reversal:
  π(rev(x)) = rev(π(x)) for all x
  Equivalently: π preserves the mirror-pair partition {L1↔L6, L2↔L5, L3↔L4}
  Such π can permute the 3 pairs among themselves and/or swap within pairs.
  This gives S₃ ⋊ (Z₂)³ — but swapping within a pair IS reversal of that pair,
  and we need the PRODUCT of all swaps to preserve the palindrome structure.

  Pure permutations preserving KW: 48
    perm=(0, 1, 2, 3, 4, 5): mirror pairs map to [(0, 5), (1, 4), (2, 3)]
    perm=(0, 1, 3, 2, 4, 5): mirror pairs map to [(0, 5), (1, 4), (2, 3)]
    perm=(0, 2, 1, 4, 3, 5): mirror pairs map to [(0, 5), (2, 3), (1, 4)]
    perm=(0, 2, 4, 1, 3, 5): mirror pairs map to [(0, 5), (2, 3), (1, 4)]
    perm=(0, 3, 1, 4, 2, 5): mirror pairs map to [(0, 5), (2, 3), (1, 4)]
    perm=(0, 3, 4, 1, 2, 5): mirror pairs map to [(0, 5), (2, 3), (1, 4)]
    perm=(0, 4, 2, 3, 1, 5): mirror pairs map to [(0, 5), (1, 4), (2, 3)]
    perm=(0, 4, 3, 2, 1, 5): mirror pairs map to [(0, 5), (1, 4), (2, 3)]
    perm=(1, 0, 2, 3, 5, 4): mirror pairs map to [(1, 4), (0, 5), (2, 3)]
    perm=(1, 0, 3, 2, 5, 4): mirror pairs map to [(1, 4), (0, 5), (2, 3)]
    perm=(1, 2, 0, 5, 3, 4): mirror pairs map to [(1, 4), (2, 3), (0, 5)]
    perm=(1, 2, 5, 0, 3, 4): mirror pairs map to [(1, 4), (2, 3), (0, 5)]
    perm=(1, 3, 0, 5, 2, 4): mirror pairs map to [(1, 4), (2, 3), (0, 5)]
    perm=(1, 3, 5, 0, 2, 4): mirror pairs map to [(1, 4), (2, 3), (0, 5)]
    perm=(1, 5, 2, 3, 0, 4): mirror pairs map to [(1, 4), (0, 5), (2, 3)]
    perm=(1, 5, 3, 2, 0, 4): mirror pairs map to [(1, 4), (0, 5), (2, 3)]
    perm=(2, 0, 1, 4, 5, 3): mirror pairs map to [(2, 3), (0, 5), (1, 4)]
    perm=(2, 0, 4, 1, 5, 3): mirror pairs map to [(2, 3), (0, 5), (1, 4)]
    perm=(2, 1, 0, 5, 4, 3): mirror pairs map to [(2, 3), (1, 4), (0, 5)]
    perm=(2, 1, 5, 0, 4, 3): mirror pairs map to [(2, 3), (1, 4), (0, 5)]
    perm=(2, 4, 0, 5, 1, 3): mirror pairs map to [(2, 3), (1, 4), (0, 5)]
    perm=(2, 4, 5, 0, 1, 3): mirror pairs map to [(2, 3), (1, 4), (0, 5)]
    perm=(2, 5, 1, 4, 0, 3): mirror pairs map to [(2, 3), (0, 5), (1, 4)]
    perm=(2, 5, 4, 1, 0, 3): mirror pairs map to [(2, 3), (0, 5), (1, 4)]
    perm=(3, 0, 1, 4, 5, 2): mirror pairs map to [(2, 3), (0, 5), (1, 4)]
    perm=(3, 0, 4, 1, 5, 2): mirror pairs map to [(2, 3), (0, 5), (1, 4)]
    perm=(3, 1, 0, 5, 4, 2): mirror pairs map to [(2, 3), (1, 4), (0, 5)]
    perm=(3, 1, 5, 0, 4, 2): mirror pairs map to [(2, 3), (1, 4), (0, 5)]
    perm=(3, 4, 0, 5, 1, 2): mirror pairs map to [(2, 3), (1, 4), (0, 5)]
    perm=(3, 4, 5, 0, 1, 2): mirror pairs map to [(2, 3), (1, 4), (0, 5)]
    perm=(3, 5, 1, 4, 0, 2): mirror pairs map to [(2, 3), (0, 5), (1, 4)]
    perm=(3, 5, 4, 1, 0, 2): mirror pairs map to [(2, 3), (0, 5), (1, 4)]
    perm=(4, 0, 2, 3, 5, 1): mirror pairs map to [(1, 4), (0, 5), (2, 3)]
    perm=(4, 0, 3, 2, 5, 1): mirror pairs map to [(1, 4), (0, 5), (2, 3)]
    perm=(4, 2, 0, 5, 3, 1): mirror pairs map to [(1, 4), (2, 3), (0, 5)]
    perm=(4, 2, 5, 0, 3, 1): mirror pairs map to [(1, 4), (2, 3), (0, 5)]
    perm=(4, 3, 0, 5, 2, 1): mirror pairs map to [(1, 4), (2, 3), (0, 5)]
    perm=(4, 3, 5, 0, 2, 1): mirror pairs map to [(1, 4), (2, 3), (0, 5)]
    perm=(4, 5, 2, 3, 0, 1): mirror pairs map to [(1, 4), (0, 5), (2, 3)]
    perm=(4, 5, 3, 2, 0, 1): mirror pairs map to [(1, 4), (0, 5), (2, 3)]
    perm=(5, 1, 2, 3, 4, 0): mirror pairs map to [(0, 5), (1, 4), (2, 3)]
    perm=(5, 1, 3, 2, 4, 0): mirror pairs map to [(0, 5), (1, 4), (2, 3)]
    perm=(5, 2, 1, 4, 3, 0): mirror pairs map to [(0, 5), (2, 3), (1, 4)]
    perm=(5, 2, 4, 1, 3, 0): mirror pairs map to [(0, 5), (2, 3), (1, 4)]
    perm=(5, 3, 1, 4, 2, 0): mirror pairs map to [(0, 5), (2, 3), (1, 4)]
    perm=(5, 3, 4, 1, 2, 0): mirror pairs map to [(0, 5), (2, 3), (1, 4)]
    perm=(5, 4, 2, 3, 1, 0): mirror pairs map to [(0, 5), (1, 4), (2, 3)]
    perm=(5, 4, 3, 2, 1, 0): mirror pairs map to [(0, 5), (1, 4), (2, 3)]

======================================================================
SUMMARY
======================================================================

  |Stab_B₆(KW)| = 384
  Stab_B₆(KW) strictly contains Z₂² (index 96).
  Generators: 6
