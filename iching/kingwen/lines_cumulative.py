"""
Cumulative line change plot for the King Wen sequence.
For each line, track a running count of state changes through the sequence.
"""

import numpy as np
import matplotlib.pyplot as plt
from sequence import all_bits

N = 64
DIMS = 6
M = np.array(all_bits())

# Compute cumulative changes per line
cumulative = np.zeros((N, DIMS))
for k in range(1, N):
    for line in range(DIMS):
        change = int(M[k, line] != M[k - 1, line])
        cumulative[k, line] = cumulative[k - 1, line] + change

positions = np.arange(N)

fig, ax = plt.subplots(figsize=(14, 7))

colors = ['#e41a1c', '#ff7f00', '#4daf4a', '#377eb8', '#984ea3', '#a65628']
labels = [f'L{i+1} ({"bottom" if i == 0 else "top" if i == 5 else "inner" if i in (2,3) else "middle"})'
          for i in range(DIMS)]

for line in range(DIMS):
    ax.plot(positions, cumulative[:, line], color=colors[line],
            label=labels[line], linewidth=2, alpha=0.85)

# Reference: uniform change rate (total_changes / 63 per step)
for line in range(DIMS):
    total = cumulative[-1, line]
    ax.plot([0, N - 1], [0, total], color=colors[line],
            linewidth=1, linestyle='--', alpha=0.3)

# Mark pair boundaries
for k in range(2, N, 2):
    ax.axvline(k, color='grey', linewidth=0.3, alpha=0.3)

# Mark Upper/Lower Canon boundary
ax.axvline(30, color='black', linewidth=1.5, linestyle=':', alpha=0.6, label='Canon boundary (30)')

ax.set_xlabel('Position in King Wen sequence', fontsize=12)
ax.set_ylabel('Cumulative changes', fontsize=12)
ax.set_title('Cumulative Line Changes Through the King Wen Sequence', fontsize=14)
ax.legend(loc='upper left', fontsize=10)
ax.set_xlim(0, N - 1)
ax.set_ylim(0, None)
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('lines_cumulative.png', dpi=150)
print(f"Saved to lines_cumulative.png")

# Print the data
print(f"\nCumulative changes at key positions:")
print(f"{'Pos':>4s}", end="")
for line in range(DIMS):
    print(f"  L{line+1:d}", end="")
print(f"  Total")

for k in [0, 8, 16, 24, 30, 32, 40, 48, 56, 63]:
    print(f"{k+1:4d}", end="")
    for line in range(DIMS):
        print(f"  {int(cumulative[k, line]):3d}", end="")
    print(f"  {int(sum(cumulative[k, :])):5d}")
