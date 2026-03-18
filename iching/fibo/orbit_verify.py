"""
Verify singleton-at-endpoints property across GL(3,F₂) × Aut(Z₅) orbit.

Key question: does GL(3,F₂) preserve Hamming structure?
GL(3,F₂) acts linearly on F₂³. Edge (x, x+eᵢ) maps to (gx, gx+geᵢ).
Hamming dist preserved iff wt(geᵢ)=1 for all i, i.e. g is a permutation matrix.
So only S₃ ⊂ GL(3,F₂) preserves the cube graph. |GL(3,F₂)|=168, |S₃|=6.

This means most orbit representatives will have DIFFERENT cube-edge partitions.
Let's check whether the singleton-at-endpoints property survives anyway.
"""

import numpy as np
from itertools import combinations

# ── Data ──────────────────────────────────────────────────────────────
TRIGRAMS = {
    0: ("Kun ☷",  "Earth"),  1: ("Zhen ☳", "Wood"),
    2: ("Kan ☵",  "Water"),  3: ("Dui ☱",  "Metal"),
    4: ("Gen ☶",  "Earth"),  5: ("Li ☲",   "Fire"),
    6: ("Xun ☴",  "Wood"),   7: ("Qian ☰", "Metal"),
}
ELEM_Z5 = {"Wood": 0, "Fire": 1, "Earth": 2, "Metal": 3, "Water": 4}

# Base surjection f: F₂³ → Z₅
BASE_F = {v: ELEM_Z5[TRIGRAMS[v][1]] for v in range(8)}
# 0→2, 1→0, 2→4, 3→3, 4→2, 5→1, 6→0, 7→3

def hamming(a, b):
    return bin(a ^ b).count('1')

def mat_apply(M, v):
    """Apply 3×3 F₂ matrix to 3-bit vector."""
    bits = [(v >> 2) & 1, (v >> 1) & 1, v & 1]
    out = [sum(M[i][j] * bits[j] for j in range(3)) % 2 for i in range(3)]
    return (out[0] << 2) | (out[1] << 1) | out[2]

def is_invertible_f2(M):
    """Check if 3×3 matrix is invertible over F₂ (det ≠ 0 mod 2)."""
    a = [row[:] for row in M]
    n = 3
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if a[row][col] % 2:
                pivot = row
                break
        if pivot is None:
            return False
        a[col], a[pivot] = a[pivot], a[col]
        for row in range(n):
            if row != col and a[row][col] % 2:
                a[row] = [(a[row][j] + a[col][j]) % 2 for j in range(n)]
    return True

def z5_relation(a, b):
    d = (b - a) % 5
    if d == 0: return "bihe"
    if d in (1, 4): return "sheng"
    return "ke"

def analyze_surjection(f_map, label=""):
    """Given f: {0..7} → Z₅, analyze cube-edge partition."""
    # Build fibers
    fibers = {}
    for v in range(8):
        fibers.setdefault(f_map[v], []).append(v)
    fiber_sizes = {v: len(fibers[f_map[v]]) for v in range(8)}
    singletons = {v for v in range(8) if fiber_sizes[v] == 1}

    # Build adjacency matrices for each relation
    adj = {"bihe": np.zeros((8,8),int), "sheng": np.zeros((8,8),int), "ke": np.zeros((8,8),int)}
    for a, b in combinations(range(8), 2):
        if hamming(a, b) != 1:
            continue
        rel = z5_relation(f_map[a], f_map[b])
        adj[rel][a, b] = adj[rel][b, a] = 1

    results = {}
    for rel_name in ["ke", "sheng"]:
        A = adj[rel_name]
        degrees = A.sum(axis=1).astype(int)

        # Find components
        visited = set()
        components = []
        for start in range(8):
            if start in visited or degrees[start] == 0:
                continue
            comp = []
            queue = [start]
            while queue:
                v = queue.pop(0)
                if v in visited: continue
                visited.add(v)
                comp.append(v)
                for u in range(8):
                    if A[v, u] and u not in visited:
                        queue.append(u)
            components.append(sorted(comp))

        # For each component, check if it's a path and where singletons land
        comp_info = []
        for comp in components:
            sub_deg = {v: degrees[v] for v in comp}
            endpoints = [v for v in comp if sub_deg[v] == 1]
            interior = [v for v in comp if sub_deg[v] >= 2]
            is_path = all(d <= 2 for d in sub_deg.values()) and len(endpoints) == 2

            singleton_endpoints = [v for v in endpoints if v in singletons]
            singleton_interior = [v for v in interior if v in singletons]

            comp_info.append({
                "size": len(comp),
                "is_path": is_path,
                "endpoints": endpoints,
                "interior": interior,
                "singleton_at_endpoint": singleton_endpoints,
                "singleton_at_interior": singleton_interior,
            })

        results[rel_name] = comp_info

    return results, fibers, singletons


# ── Generate GL(3,F₂) elements ──────────────────────────────────────
# Pick specific interesting ones:
# 1. Identity (baseline)
# 2. Coordinate permutation (012) → (120) — preserves Hamming
# 3. Non-Hamming-preserving: e1→e1, e2→e2, e3→e1+e3
# 4. Non-Hamming-preserving: e1→e1+e2, e2→e2+e3, e3→e1+e3
# 5. Another: e1→e2, e2→e3, e3→e1+e2

GL_ELEMENTS = [
    ("Identity", [[1,0,0],[0,1,0],[0,0,1]]),
    ("Coord perm (120)", [[0,0,1],[1,0,0],[0,1,0]]),
    ("Shear e3→e1+e3", [[1,0,0],[0,1,0],[1,0,1]]),
    ("Mixed 1", [[1,1,0],[0,1,1],[0,0,1]]),
    ("Mixed 2", [[0,1,0],[0,0,1],[1,1,0]]),
]

# Also apply Aut(Z₅) = {1,2,3,4} (multiplication mod 5)
AUT_Z5 = [1, 2, 3, 4]

print("="*75)
print("ORBIT VERIFICATION: singleton placement under GL(3,F₂) × Aut(Z₅)")
print("="*75)

# First: does GL(3,F₂) preserve Hamming?
print("\n── Does each GL(3,F₂) element preserve Hamming distance? ──\n")
for name, M in GL_ELEMENTS:
    assert is_invertible_f2(M), f"{name} not invertible!"
    # Check if Hamming-preserving: images of e1,e2,e3 must have weight 1
    images = [mat_apply(M, 1), mat_apply(M, 2), mat_apply(M, 4)]
    weights = [bin(img).count('1') for img in images]
    preserves = all(w == 1 for w in weights)
    print(f"  {name:25s}: basis image weights = {weights}, preserves Hamming = {preserves}")

# Now test all combinations
print("\n── Singleton placement across orbit representatives ──\n")
print(f"{'GL element':25s} {'Aut(Z5)':>8s} | {'克 components':40s} | {'生 components':40s} | {'singletons':>10s}")
print("-"*140)

all_ke_singleton_at_endpoint = True
all_sheng_singleton_at_interior = True

for gl_name, M in GL_ELEMENTS:
    for aut_k in AUT_Z5:
        # New surjection: f'(v) = aut_k * f(g⁻¹(v)) mod 5
        # But easier: f'(v) = aut_k * BASE_F[M⁻¹ v] mod 5
        # Or equivalently: define f' on transformed vertices
        # f'(v) = (aut_k * BASE_F[v]) mod 5, then apply g to vertex labels
        # 
        # Actually: the orbit action is:
        #   (g, σ) · f = σ ∘ f ∘ g⁻¹
        # So new_f(v) = σ(f(g⁻¹(v))) = (aut_k * BASE_F[g⁻¹(v)]) % 5
        #
        # We need g⁻¹. Compute by brute force on 8 elements.
        
        g_map = {v: mat_apply(M, v) for v in range(8)}
        g_inv = {w: v for v, w in g_map.items()}
        
        new_f = {v: (aut_k * BASE_F[g_inv[v]]) % 5 for v in range(8)}
        
        # Verify it's still a surjection with same fiber sizes
        fiber_sizes = sorted([list(new_f.values()).count(z) for z in set(new_f.values())])
        assert fiber_sizes == [1, 1, 2, 2, 2], f"Fiber sizes changed: {fiber_sizes}"
        
        results, fibers, singletons = analyze_surjection(new_f)
        
        # Format ke results
        ke_parts = []
        for ci in results["ke"]:
            s = f"P{ci['size']}"
            if ci["singleton_at_endpoint"]:
                s += f"(sing@endpt:{len(ci['singleton_at_endpoint'])})"
            if ci["singleton_at_interior"]:
                s += f"(sing@intr:{len(ci['singleton_at_interior'])})"
            ke_parts.append(s)
        ke_str = " ∪ ".join(ke_parts)
        
        # Format sheng results
        sh_parts = []
        for ci in results["sheng"]:
            s = f"P{ci['size']}"
            if ci["singleton_at_endpoint"]:
                s += f"(sing@endpt:{len(ci['singleton_at_endpoint'])})"
            if ci["singleton_at_interior"]:
                s += f"(sing@intr:{len(ci['singleton_at_interior'])})"
            sh_parts.append(s)
        sh_str = " ∪ ".join(sh_parts)
        
        # Check invariant
        ke_ok = all(
            len(ci["singleton_at_interior"]) == 0 and len(ci["singleton_at_endpoint"]) > 0
            for ci in results["ke"] if any(v in singletons for v in ci["endpoints"] + ci["interior"])
        )
        sh_ok = all(
            len(ci["singleton_at_endpoint"]) == 0 and len(ci["singleton_at_interior"]) > 0
            for ci in results["sheng"] if any(v in singletons for v in ci["endpoints"] + ci["interior"])
        )
        
        # More careful check: for 克, are ALL singletons at endpoints?
        ke_sing_endpt = sum(len(ci["singleton_at_endpoint"]) for ci in results["ke"])
        ke_sing_intr = sum(len(ci["singleton_at_interior"]) for ci in results["ke"])
        sh_sing_endpt = sum(len(ci["singleton_at_endpoint"]) for ci in results["sheng"])
        sh_sing_intr = sum(len(ci["singleton_at_interior"]) for ci in results["sheng"])
        
        if ke_sing_intr > 0:
            all_ke_singleton_at_endpoint = False
        if sh_sing_endpt > 0:
            all_sheng_singleton_at_interior = False
        
        sing_status = f"ke:{ke_sing_endpt}e/{ke_sing_intr}i sh:{sh_sing_endpt}e/{sh_sing_intr}i"
        
        print(f"{gl_name:25s} {'×'+str(aut_k):>8s} | {ke_str:40s} | {sh_str:40s} | {sing_status}")

print("\n" + "="*75)
print(f"克: singletons ALWAYS at endpoints? {all_ke_singleton_at_endpoint}")
print(f"生: singletons ALWAYS at interior?  {all_sheng_singleton_at_interior}")
print("="*75)

# Bonus: also check that component structure (P₄∪P₄ for 克, P₃∪P₃ for 生) is preserved
print("\n── Component structure preservation ──\n")
ke_structures = set()
sh_structures = set()

for gl_name, M in GL_ELEMENTS:
    for aut_k in AUT_Z5:
        g_map = {v: mat_apply(M, v) for v in range(8)}
        g_inv = {w: v for v, w in g_map.items()}
        new_f = {v: (aut_k * BASE_F[g_inv[v]]) % 5 for v in range(8)}
        results, _, _ = analyze_surjection(new_f)
        
        ke_sig = tuple(sorted(ci["size"] for ci in results["ke"]))
        sh_sig = tuple(sorted(ci["size"] for ci in results["sheng"]))
        ke_structures.add(ke_sig)
        sh_structures.add(sh_sig)

print(f"Distinct 克 component structures: {ke_structures}")
print(f"Distinct 生 component structures: {sh_structures}")

# If structures vary, the edge partition itself changes under non-Hamming GL elements
if len(ke_structures) > 1 or len(sh_structures) > 1:
    print("\n⚠ Component structures VARY across the orbit!")
    print("  GL(3,F₂) does NOT preserve Hamming distance in general.")
    print("  Only the S₃ subgroup (coordinate permutations) preserves edges.")
    print("  The singleton-at-endpoints property may not be an orbit invariant.")
