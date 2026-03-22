#!/usr/bin/env python3
"""
Exhaustive doubly-magic search using constraint propagation.
Find a permutation of 1..30 on the 2×3×5 cube where
element slices all sum to 93 and line slices all sum to 155.
"""
import random
from itertools import combinations

N_POL, N_LINE, N_ELEM = 2, 3, 5

def cell_index(p, l, e):
    return p * (N_LINE * N_ELEM) + l * N_ELEM + e

# Better approach: simulated annealing with temperature
random.seed(42)
best_global = float('inf')
best_perm_global = None

for restart in range(50):
    perm = list(range(1, 31))
    random.shuffle(perm)
    
    T = 10.0
    T_min = 0.001
    cooling = 0.99995
    best = float('inf')
    best_perm = None
    
    step = 0
    while T > T_min and best > 0:
        i, j = random.sample(range(30), 2)
        perm[i], perm[j] = perm[j], perm[i]
        
        e_sums = [0] * 5
        l_sums = [0] * 3
        for p in range(2):
            for l in range(3):
                for e in range(5):
                    v = perm[cell_index(p, l, e)]
                    e_sums[e] += v
                    l_sums[l] += v
        
        cost = sum((s - 93)**2 for s in e_sums) + sum((s - 155)**2 for s in l_sums)
        
        if cost < best:
            best = cost
            best_perm = perm.copy()
        
        import math
        if cost <= best or random.random() < math.exp(-(cost - best) / T):
            pass  # accept
        else:
            perm[i], perm[j] = perm[j], perm[i]
        
        T *= cooling
        step += 1
    
    if best < best_global:
        best_global = best
        best_perm_global = best_perm
        print(f"Restart {restart}: best cost = {best}")
    
    if best_global == 0:
        break

print(f"\nFinal best cost: {best_global}")
if best_global == 0:
    perm = best_perm_global
    e_sums = [0]*5; l_sums = [0]*3
    for p in range(2):
        for l in range(3):
            for e in range(5):
                v = perm[cell_index(p, l, e)]
                e_sums[e] += v
                l_sums[l] += v
    print(f"Element sums: {e_sums}")
    print(f"Line sums: {l_sums}")
    
    ELEM_NAMES = {0: 'Wood', 1: 'Fire', 2: 'Earth', 3: 'Metal', 4: 'Water'}
    LINE_NAMES = {0: 'H', 1: 'P', 2: 'Q'}
    print(f"\n{'':8s}", end='')
    for e in range(5):
        print(f"  {ELEM_NAMES[e]:>6s}", end='')
    print("  | sum")
    for p in range(2):
        for l in range(3):
            label = f"{'pos' if p==0 else 'neg'} {LINE_NAMES[l]}"
            row_sum = 0
            print(f"{label:8s}", end='')
            for e in range(5):
                v = perm[cell_index(p, l, e)]
                print(f"  {v:6d}", end='')
                row_sum += v
            print(f"  | {row_sum}")
else:
    perm = best_perm_global
    e_sums = [0]*5; l_sums = [0]*3
    for p in range(2):
        for l in range(3):
            for e in range(5):
                v = perm[cell_index(p, l, e)]
                e_sums[e] += v
                l_sums[l] += v
    print(f"Element sums: {e_sums}")
    print(f"Line sums: {l_sums}")
    print("Doubly-magic not found in this search.")
