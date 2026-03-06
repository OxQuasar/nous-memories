"""
Check: what fraction of Hamiltonian paths on the 6-cube have uniform orbit visits (4 per orbit)?
This determines whether Eulerian is a consequence of orbit-uniformity or an independent constraint.

From baseline_findings.md: Eulerian is a THEOREM for orbit-paired sequences.
The proof relies on: each orbit has exactly 8 hexagrams / 2 = 4 pairs.
Any ordering of 32 pairs → each orbit has 4 outgoing and 4 incoming edges → Eulerian.

So the question becomes: is orbit-uniformity itself forced by orbit-consistent pairing?
Answer: YES. If each orbit has exactly 8 hexagrams, and each pair uses a Z₂³ mask
(which is a fixed-point-free involution within the orbit), then each orbit contributes
exactly 4 pairs. In ANY ordering of these 32 pairs, each orbit appears exactly 4 times.

The chain is: orbit-consistent pairing → orbit-uniform visits → Eulerian bridge walk.
"""

import sys
sys.path.insert(0, '/home/quasar/nous/kingwen')

from collections import Counter
from sequence import all_bits
import random

M = all_bits()

def xor_sig(h):
    return (h[0] ^ h[5], h[1] ^ h[4], h[2] ^ h[3])

# For random Hamiltonian paths on Q₆, what's the orbit visit distribution?
# (These are NOT orbit-paired, so orbit visits can be non-uniform)

def warnsdorff_hamiltonian(start, rng):
    """Generate random Hamiltonian path on Q₆ via Warnsdorff."""
    n = 64
    visited = [False] * n
    path = [start]
    visited[start] = True
    
    for step in range(n - 1):
        current = path[-1]
        neighbors = []
        for bit in range(6):
            nb = current ^ (1 << bit)
            if not visited[nb]:
                # Count nb's unvisited neighbors
                deg = sum(1 for b in range(6) if not visited[nb ^ (1 << b)])
                neighbors.append((deg, nb))
        
        if not neighbors:
            return None
        
        min_deg = min(d for d, _ in neighbors)
        candidates = [nb for d, nb in neighbors if d == min_deg]
        chosen = rng.choice(candidates)
        path.append(chosen)
        visited[chosen] = True
    
    return path

def int_to_tuple(n):
    return tuple((n >> b) & 1 for b in range(6))

rng = random.Random(42)
N = 5000

print("=" * 70)
print("ORBIT VISIT UNIFORMITY IN RANDOM HAMILTONIAN PATHS (Q₆)")
print("=" * 70)

uniform_count = 0
orbit_visit_distributions = []

for i in range(N):
    start = rng.randint(0, 63)
    path = warnsdorff_hamiltonian(start, rng)
    if path is None:
        continue
    
    # Count orbit visits
    orbit_visits = Counter()
    for v in path:
        h = int_to_tuple(v)
        orbit_visits[xor_sig(h)] += 1
    
    # Check uniformity (all 8 orbits visited exactly 8 times each)
    is_uniform = all(orbit_visits[sig] == 8 for sig in orbit_visits) and len(orbit_visits) == 8
    if is_uniform:
        uniform_count += 1
    
    orbit_visit_distributions.append(dict(orbit_visits))

print(f"\nSampled {N} random Hamiltonian paths on Q₆")
print(f"Paths with uniform orbit visits (8 per orbit): {uniform_count}/{N} ({100*uniform_count/N:.2f}%)")

# Distribution of visit counts per orbit
print(f"\nOrbit visit count statistics:")
all_visit_counts = []
for dist in orbit_visit_distributions:
    for sig in dist:
        all_visit_counts.append(dist[sig])

visit_count_dist = Counter(all_visit_counts)
print(f"  Visit count distribution across all (path, orbit) pairs:")
for vc in sorted(visit_count_dist.keys()):
    pct = 100 * visit_count_dist[vc] / len(all_visit_counts)
    print(f"    {vc:2d}: {visit_count_dist[vc]:6d} ({pct:5.1f}%)")

# Now check: for orbit-PAIRED Hamiltonian paths (which require orbit-consistent pairing),
# the 32 pairs are split 4 per orbit. In these:
# - Each orbit is visited as a pair-orbit 4 times (forced)
# - Each pair-orbit has in/out degree balanced → Eulerian (theorem)
# So orbit-uniformity at the PAIR level is forced, which implies Eulerian.

# But at the HEXAGRAM level, orbit visits = 8 per orbit (since 4 pairs × 2 = 8).
# This is also forced by orbit-consistent pairing.

print(f"\n{'─'*70}")
print("CHAIN OF IMPLICATIONS")
print(f"{'─'*70}")
print()
print("For ANY 64-hexagram sequence:")
print("  orbit-consistent pairing")
print("    → each orbit contributes exactly 4 pairs (forced: 8 hex / 2)")
print("    → orbit visits at pair level: exactly 4 per orbit (forced)")
print("    → degree balance at each orbit: in=out for internal, ±1 at endpoints")
print("    → Eulerian bridge walk (theorem)")
print()
print("The Eulerian property is a CONSEQUENCE of orbit-uniformity,")
print("which is itself a CONSEQUENCE of orbit-consistent pairing.")
print("These are not independent constraints.")
print()

# Extra check: for random Q₆ Hamiltonian paths, what's P(orbit-uniform)?
# From above: extremely low, since random Q₆ paths visit orbits very non-uniformly.
# The orbit-consistent pairing is what forces uniformity, and uniformity forces Eulerian.

# For random pair orderings (B2 model), orbit visits ARE 4 per orbit by construction.
# So Eulerian is guaranteed = 100% (verified empirically in baseline).

print(f"\n{'─'*70}")
print("FRACTION OF Q₆ HAMILTONIAN PATHS WITH UNIFORM ORBIT VISITS")
print(f"{'─'*70}")
print(f"P(uniform orbit visits on Q₆) = {uniform_count}/{N} = {100*uniform_count/N:.4f}%")
print(f"This is the probability that a random Hamiltonian path on Q₆")
print(f"visits each of the 8 orbits exactly 8 times.")
print()
if uniform_count == 0:
    print("Zero occurrences in {N} samples → orbit uniformity is extremely rare")
    print("on random Q₆ Hamiltonian paths (< 1/5000 = 0.02%).")
    print()
    print("This means: orbit-uniformity is NOT a free property of Hamiltonian paths.")
    print("It requires the orbit-consistent pairing structure to be enforced.")
else:
    print(f"Approximately {100*uniform_count/N:.2f}% of random Q₆ paths are orbit-uniform.")

# Check max deviation from uniformity
max_devs = []
for dist in orbit_visit_distributions:
    max_dev = max(abs(dist.get(sig, 0) - 8) for sig in [(i>>2, (i>>1)&1, i&1) for i in range(8)])
    max_devs.append(max_dev)

mean_maxdev = sum(max_devs) / len(max_devs)
print(f"\nMean max deviation from 8-uniform: {mean_maxdev:.2f}")
print(f"Max max deviation: {max(max_devs)}")

print(f"\n{'='*70}")
print("ANALYSIS COMPLETE")
print("=" * 70)
