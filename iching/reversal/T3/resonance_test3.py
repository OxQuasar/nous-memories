#!/usr/bin/env python3
"""Resonance Test 3: Empirical Asymmetry in Climate Cycles.

Does the {4,2,2,2,2} cascade — Earth at 4/12 branch positions — predict
observable asymmetries in natural 12-fold cycles?

Phase 1: Acquire monthly temperature normals for ~100 diverse global locations
Phase 2: Cluster 12 months into 5 groups, record partition types
Phase 3: Compare empirical partition distribution to {4,2,2,2,2}
Phase 4: Rate-of-change (dT/dt) structure — transition month detection
Phase 5: Multi-variable extension (temperature + day-length)
"""

import numpy as np
import json
import time
import requests
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations

from scipy.stats import chi2_contingency, fisher_exact
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

OUT_DIR = Path(__file__).resolve().parent
CACHE_PATH = OUT_DIR / "climate_normals_cache.json"

N_PERM = 10_000
RNG = np.random.default_rng(42)

# ═══════════════════════════════════════════════════════
# City database — diverse global coverage
# ═══════════════════════════════════════════════════════

# (name, lat, lon, climate_zone)
# Zones: tropical, arid, temperate, continental, polar, monsoon
CITIES = [
    # Northern Hemisphere — Continental
    ("Moscow", 55.76, 37.62, "continental"),
    ("Helsinki", 60.17, 24.94, "continental"),
    ("Stockholm", 59.33, 18.07, "continental"),
    ("Warsaw", 52.23, 21.01, "continental"),
    ("Kyiv", 50.45, 30.52, "continental"),
    ("Minsk", 53.90, 27.57, "continental"),
    ("Novosibirsk", 55.03, 82.92, "continental"),
    ("Irkutsk", 52.29, 104.30, "continental"),
    ("Ulaanbaatar", 47.92, 106.91, "continental"),
    ("Harbin", 45.75, 126.65, "continental"),
    ("Sapporo", 43.06, 141.35, "continental"),
    ("Chicago", 41.88, -87.63, "continental"),
    ("Minneapolis", 44.98, -93.27, "continental"),
    ("Montreal", 45.50, -73.57, "continental"),
    ("Toronto", 43.65, -79.38, "continental"),
    ("Winnipeg", 49.90, -97.14, "continental"),
    ("Astana", 51.17, 71.43, "continental"),
    ("Bucharest", 44.43, 26.10, "continental"),
    ("Prague", 50.08, 14.44, "continental"),
    ("Vienna", 48.21, 16.37, "continental"),

    # Northern Hemisphere — Temperate oceanic
    ("London", 51.51, -0.13, "temperate"),
    ("Paris", 48.86, 2.35, "temperate"),
    ("Berlin", 52.52, 13.41, "temperate"),
    ("Amsterdam", 52.37, 4.90, "temperate"),
    ("Dublin", 53.35, -6.26, "temperate"),
    ("Brussels", 50.85, 4.35, "temperate"),
    ("Seattle", 47.61, -122.33, "temperate"),
    ("Portland_OR", 45.52, -122.68, "temperate"),
    ("Vancouver", 49.28, -123.12, "temperate"),
    ("San_Francisco", 37.77, -122.42, "temperate"),

    # Northern Hemisphere — Temperate/Subtropical
    ("New_York", 40.71, -74.01, "temperate"),
    ("Washington_DC", 38.91, -77.04, "temperate"),
    ("Tokyo", 35.68, 139.69, "temperate"),
    ("Seoul", 37.57, 126.98, "temperate"),
    ("Beijing", 39.90, 116.40, "continental"),
    ("Shanghai", 31.23, 121.47, "temperate"),
    ("Osaka", 34.69, 135.50, "temperate"),
    ("Milan", 45.46, 9.19, "temperate"),
    ("Rome", 41.90, 12.50, "temperate"),
    ("Madrid", 40.42, -3.70, "temperate"),
    ("Lisbon", 38.72, -9.14, "temperate"),
    ("Athens", 37.98, 23.73, "temperate"),
    ("Istanbul", 41.01, 28.98, "temperate"),
    ("Tbilisi", 41.69, 44.80, "temperate"),
    ("Tehran", 35.69, 51.39, "arid"),
    ("Tashkent", 41.30, 69.28, "continental"),

    # Northern Hemisphere — Subtropical/Tropical
    ("Houston", 29.76, -95.37, "subtropical"),
    ("Miami", 25.76, -80.19, "tropical"),
    ("Havana", 23.11, -82.37, "tropical"),
    ("Mexico_City", 19.43, -99.13, "subtropical"),
    ("Cairo", 30.04, 31.24, "arid"),
    ("Riyadh", 24.71, 46.67, "arid"),
    ("Dubai", 25.20, 55.27, "arid"),
    ("Mumbai", 19.08, 72.88, "monsoon"),
    ("Delhi", 28.61, 77.21, "monsoon"),
    ("Bangkok", 13.76, 100.50, "tropical"),
    ("Hanoi", 21.03, 105.85, "monsoon"),
    ("Manila", 14.60, 120.98, "tropical"),
    ("Hong_Kong", 22.32, 114.17, "subtropical"),
    ("Taipei", 25.03, 121.57, "subtropical"),
    ("Guangzhou", 23.13, 113.26, "subtropical"),

    # Equatorial/Tropical
    ("Singapore", 1.35, 103.82, "tropical"),
    ("Jakarta", -6.21, 106.85, "tropical"),
    ("Kuala_Lumpur", 3.14, 101.69, "tropical"),
    ("Nairobi", -1.29, 36.82, "tropical"),
    ("Lagos", 6.52, 3.38, "tropical"),
    ("Kinshasa", -4.32, 15.31, "tropical"),
    ("Bogota", 4.71, -74.07, "tropical"),
    ("Quito", -0.18, -78.47, "tropical"),
    ("Lima", -12.05, -77.04, "arid"),
    ("Manaus", -3.12, -60.02, "tropical"),

    # Southern Hemisphere — Temperate
    ("Buenos_Aires", -34.60, -58.38, "temperate"),
    ("Santiago", -33.45, -70.67, "temperate"),
    ("Montevideo", -34.88, -56.17, "temperate"),
    ("Cape_Town", -33.93, 18.42, "temperate"),
    ("Sydney", -33.87, 151.21, "temperate"),
    ("Melbourne", -37.81, 144.96, "temperate"),
    ("Auckland", -36.85, 174.76, "temperate"),
    ("Christchurch", -43.53, 172.64, "temperate"),
    ("Perth", -31.95, 115.86, "temperate"),
    ("Adelaide", -34.93, 138.60, "temperate"),

    # Southern Hemisphere — Subtropical/Other
    ("Sao_Paulo", -23.55, -46.63, "subtropical"),
    ("Rio_de_Janeiro", -22.91, -43.17, "subtropical"),
    ("Johannesburg", -26.20, 28.04, "subtropical"),
    ("Durban", -29.86, 31.02, "subtropical"),
    ("Brasilia", -15.79, -47.88, "tropical"),

    # Arid/Desert
    ("Phoenix", 33.45, -112.07, "arid"),
    ("Las_Vegas", 36.17, -115.14, "arid"),
    ("Karachi", 24.86, 67.01, "arid"),
    ("Baghdad", 33.31, 44.37, "arid"),
    ("Marrakech", 31.63, -8.01, "arid"),

    # High latitude
    ("Reykjavik", 64.15, -21.94, "polar"),
    ("Tromsø", 69.65, 18.96, "polar"),
    ("Fairbanks", 64.84, -147.72, "polar"),
    ("Anchorage", 61.22, -149.90, "polar"),
    ("Murmansk", 68.97, 33.09, "polar"),
    ("Yakutsk", 62.04, 129.74, "continental"),
]

assert len(CITIES) == len(set(c[0] for c in CITIES)), "Duplicate city names"


# ═══════════════════════════════════════════════════════
# Phase 1: Data acquisition
# ═══════════════════════════════════════════════════════

def fetch_monthly_normals(cities, start_year=1991, end_year=2020):
    """Fetch 30-year monthly temperature normals from Open-Meteo."""
    
    # Check cache
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            cached = json.load(f)
        if len(cached) >= len(cities):
            print(f"  Loaded {len(cached)} cities from cache")
            return cached
    
    results = {}
    total = len(cities)
    
    for i, (name, lat, lon, zone) in enumerate(cities):
        print(f"  [{i+1}/{total}] {name}...", end=" ", flush=True)
        
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            'latitude': lat,
            'longitude': lon,
            'start_date': f'{start_year}-01-01',
            'end_date': f'{end_year}-12-31',
            'daily': 'temperature_2m_mean',
            'timezone': 'UTC'
        }
        
        try:
            r = requests.get(url, params=params, timeout=60)
            data = r.json()
            
            if 'daily' not in data:
                print(f"ERROR: {data.get('reason', 'unknown')}")
                continue
            
            times = data['daily']['time']
            temps = data['daily']['temperature_2m_mean']
            
            monthly = defaultdict(list)
            for t, v in zip(times, temps):
                if v is not None:
                    month = int(t[5:7])
                    monthly[month].append(v)
            
            normals = [float(np.mean(monthly[m])) for m in range(1, 13)]
            results[name] = {
                'lat': lat, 'lon': lon, 'zone': zone,
                'normals': normals,
                'n_days': sum(len(monthly[m]) for m in range(1, 13))
            }
            print(f"OK ({results[name]['n_days']} days)")
            
        except Exception as e:
            print(f"FAILED: {e}")
        
        # Rate limiting — Open-Meteo free tier allows ~10 requests/minute
        time.sleep(7)
    
    # Cache results
    with open(CACHE_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Cached {len(results)} cities to {CACHE_PATH}")
    
    return results


# ═══════════════════════════════════════════════════════
# Phase 2: Clustering
# ═══════════════════════════════════════════════════════

def partition_type(labels, k):
    """Return sorted partition sizes (descending)."""
    counts = Counter(labels)
    sizes = sorted(counts.values(), reverse=True)
    return tuple(sizes)


def cluster_months(normals_12, k=5, method='ward'):
    """Cluster 12 months into k groups using hierarchical clustering.
    
    Uses temperature + rate-of-change as features for each month.
    Returns: labels (length 12), partition type.
    """
    T = np.array(normals_12)
    
    # Feature 1: temperature (standardized)
    T_std = (T - T.mean()) / (T.std() + 1e-10)
    
    # Feature 2: rate of change (forward difference, circular)
    dT = np.zeros(12)
    for i in range(12):
        dT[i] = T[(i+1) % 12] - T[i]
    dT_std = (dT - dT.mean()) / (dT.std() + 1e-10)
    
    # Combine features
    X = np.column_stack([T_std, dT_std])
    
    # Hierarchical clustering
    Z = linkage(X, method=method)
    labels = fcluster(Z, t=k, criterion='maxclust') - 1  # 0-indexed
    
    return labels, partition_type(labels, k)


def cluster_months_temp_only(normals_12, k=5, method='ward'):
    """Cluster using temperature only (no rate-of-change)."""
    T = np.array(normals_12).reshape(-1, 1)
    Z = linkage(T, method=method)
    labels = fcluster(Z, t=k, criterion='maxclust') - 1
    return labels, partition_type(labels, k)


# ═══════════════════════════════════════════════════════
# Phase 3: Partition distribution analysis
# ═══════════════════════════════════════════════════════

def enumerate_partitions_of_12_into_5():
    """Enumerate all integer partitions of 12 into exactly 5 parts."""
    parts = []
    for a in range(8, 0, -1):  # largest part
        for b in range(min(a, 12-a), 0, -1):
            for c in range(min(b, 12-a-b), 0, -1):
                for d in range(min(c, 12-a-b-c), 0, -1):
                    e = 12 - a - b - c - d
                    if 0 < e <= d:
                        parts.append((a, b, c, d, e))
    return sorted(set(parts), reverse=True)


def null_partition_distribution(n_points=12, k=5, n_sim=100_000, method='ward'):
    """Monte Carlo: cluster n_points of random data into k groups. 
    What partition types emerge?
    
    Uses random 1D + dT data to match our analysis pipeline.
    """
    partition_counts = Counter()
    
    for _ in range(n_sim):
        # Random smooth annual cycle: sum of harmonics with random phases
        t = np.arange(12) * 2 * np.pi / 12
        T = RNG.normal(0, 1) * np.sin(t + RNG.uniform(0, 2*np.pi))
        T += RNG.normal(0, 0.3) * np.sin(2*t + RNG.uniform(0, 2*np.pi))
        T += RNG.normal(0, 0.1, 12)  # noise
        
        T_std = (T - T.mean()) / (T.std() + 1e-10)
        dT = np.array([T[(i+1) % 12] - T[i] for i in range(12)])
        dT_std = (dT - dT.mean()) / (dT.std() + 1e-10)
        
        X = np.column_stack([T_std, dT_std])
        Z = linkage(X, method=method)
        labels = fcluster(Z, t=k, criterion='maxclust') - 1
        pt = partition_type(labels, k)
        partition_counts[pt] += 1
    
    return partition_counts


def null_partition_uniform(n_points=12, k=5, n_sim=100_000, method='ward'):
    """Null: cluster 12 uniform random points in 2D."""
    partition_counts = Counter()
    for _ in range(n_sim):
        X = RNG.normal(0, 1, (n_points, 2))
        Z = linkage(X, method=method)
        labels = fcluster(Z, t=k, criterion='maxclust') - 1
        pt = partition_type(labels, k)
        partition_counts[pt] += 1
    return partition_counts


# ═══════════════════════════════════════════════════════
# Phase 4: Rate-of-change analysis
# ═══════════════════════════════════════════════════════

def analyze_rate_of_change(normals_12):
    """Analyze the monthly rate-of-change structure.
    
    Returns: dT array, transition_months (top 4 by |dT|), stable_months
    """
    T = np.array(normals_12)
    dT = np.array([T[(i+1) % 12] - T[i] for i in range(12)])
    
    # Rank months by |dT|
    ranked = np.argsort(-np.abs(dT))
    transition_months = sorted(ranked[:4].tolist())  # top 4 by |dT|
    stable_months = sorted(ranked[4:].tolist())
    
    return dT, transition_months, stable_months


def check_transition_spacing(transition_months):
    """Check if the 4 transition months are evenly spaced (~3 apart).
    
    The {4,2,2,2,2} prediction says the 4 Earth months are the
    inter-seasonal transitions: months 3, 6, 9, 12 (0-indexed: 2, 5, 8, 11).
    This means they should be roughly evenly spaced at intervals of 3.
    """
    if len(transition_months) != 4:
        return False, 0
    
    # Compute circular gaps
    gaps = []
    for i in range(4):
        gap = (transition_months[(i+1) % 4] - transition_months[i]) % 12
        gaps.append(gap)
    
    # Perfect spacing: all gaps = 3
    # Measure: max deviation from 3
    max_dev = max(abs(g - 3) for g in gaps)
    is_evenly_spaced = max_dev <= 1  # allow ±1 month tolerance
    
    return is_evenly_spaced, max_dev


# ═══════════════════════════════════════════════════════
# Phase 5: Day-length extension
# ═══════════════════════════════════════════════════════

def compute_daylength(lat, month):
    """Approximate day length in hours for a given latitude and month.
    
    Uses the simplified formula based on solar declination.
    """
    # Day of year at mid-month
    mid_days = [15, 46, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349]
    doy = mid_days[month - 1]
    
    # Solar declination (radians)
    decl = 23.45 * np.sin(np.radians((360/365) * (doy - 81)))
    decl_rad = np.radians(decl)
    lat_rad = np.radians(lat)
    
    # Hour angle at sunrise
    cos_ha = -np.tan(lat_rad) * np.tan(decl_rad)
    cos_ha = np.clip(cos_ha, -1, 1)  # handle polar day/night
    ha = np.degrees(np.arccos(cos_ha))
    
    return 2 * ha / 15  # hours of daylight


def cluster_months_multivar(normals_12, lat, k=5, method='ward'):
    """Cluster using temperature + day-length + their rates of change."""
    T = np.array(normals_12)
    D = np.array([compute_daylength(lat, m) for m in range(1, 13)])
    
    T_std = (T - T.mean()) / (T.std() + 1e-10)
    D_std = (D - D.mean()) / (D.std() + 1e-10)
    
    dT = np.array([T[(i+1) % 12] - T[i] for i in range(12)])
    dD = np.array([D[(i+1) % 12] - D[i] for i in range(12)])
    dT_std = (dT - dT.mean()) / (dT.std() + 1e-10)
    dD_std = (dD - dD.mean()) / (dD.std() + 1e-10)
    
    X = np.column_stack([T_std, D_std, dT_std, dD_std])
    
    Z = linkage(X, method=method)
    labels = fcluster(Z, t=k, criterion='maxclust') - 1
    
    return labels, partition_type(labels, k)


# ═══════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════

def main():
    print("Resonance Test 3: Empirical Asymmetry in Climate Cycles")
    print("=" * 70)
    
    # ── Phase 1: Data ──
    print("\nPhase 1: Load monthly temperature normals")
    print("-" * 50)
    from climate_normals import CLIMATE_NORMALS
    data = CLIMATE_NORMALS
    print(f"  Loaded {len(data)} cities")
    
    # Filter: only cities with seasonal variation (std > 2°C)
    seasonal_cities = {}
    flat_cities = {}
    for name, info in data.items():
        std = np.std(info['normals'])
        if std > 2.0:
            seasonal_cities[name] = info
        else:
            flat_cities[name] = info
    
    print(f"  Seasonal (std > 2°C): {len(seasonal_cities)}")
    print(f"  Flat (std ≤ 2°C): {len(flat_cities)} — {list(flat_cities.keys())}")
    
    # ── Phase 2: Clustering ──
    print(f"\n\nPhase 2: Cluster months into 5 groups")
    print("-" * 50)
    
    results_temp_dt = {}  # temperature + dT/dt
    results_temp_only = {}  # temperature only
    results_multivar = {}  # temperature + daylength + rates
    
    for name, info in seasonal_cities.items():
        normals = info['normals']
        lat = info['lat']
        
        labels_td, pt_td = cluster_months(normals)
        labels_t, pt_t = cluster_months_temp_only(normals)
        labels_m, pt_m = cluster_months_multivar(normals, lat)
        
        results_temp_dt[name] = {'labels': labels_td.tolist(), 'partition': pt_td}
        results_temp_only[name] = {'labels': labels_t.tolist(), 'partition': pt_t}
        results_multivar[name] = {'labels': labels_m.tolist(), 'partition': pt_m}
    
    # Partition distribution
    print(f"\n  Partition distributions (k=5 groups):")
    for method_name, results in [("T+dT", results_temp_dt), 
                                   ("T only", results_temp_only),
                                   ("T+D+dT+dD", results_multivar)]:
        partitions = [r['partition'] for r in results.values()]
        dist = Counter(partitions)
        total = len(partitions)
        
        print(f"\n  Method: {method_name} ({total} cities)")
        print(f"  {'Partition':>20} {'Count':>6} {'%':>7}")
        print(f"  {'-'*35}")
        for pt, count in dist.most_common():
            pct = 100 * count / total
            marker = " ◄ PREDICTED" if pt == (4, 2, 2, 2, 2) else ""
            print(f"  {str(pt):>20} {count:>6} {pct:>6.1f}%{marker}")
    
    # ── Phase 3: Statistical comparison ──
    print(f"\n\nPhase 3: Compare to {'{4,2,2,2,2}'} prediction")
    print("-" * 50)
    
    # Observed rate of (4,2,2,2,2)
    for method_name, results in [("T+dT", results_temp_dt), 
                                   ("T only", results_temp_only),
                                   ("T+D+dT+dD", results_multivar)]:
        partitions = [r['partition'] for r in results.values()]
        n_422 = sum(1 for p in partitions if p == (4, 2, 2, 2, 2))
        n_total = len(partitions)
        obs_rate = n_422 / n_total if n_total > 0 else 0
        print(f"\n  {method_name}: {n_422}/{n_total} = {obs_rate:.1%} are (4,2,2,2,2)")
    
    # Null distribution — smooth annual cycles
    print(f"\n  Null distribution (100K random smooth annual cycles):")
    null_dist = null_partition_distribution(n_sim=100_000)
    null_total = sum(null_dist.values())
    null_422 = null_dist.get((4, 2, 2, 2, 2), 0)
    null_rate = null_422 / null_total
    print(f"  Null rate of (4,2,2,2,2): {null_422}/{null_total} = {null_rate:.1%}")
    print(f"\n  Top null partitions:")
    for pt, count in null_dist.most_common(8):
        pct = 100 * count / null_total
        print(f"    {str(pt):>20} {count:>7} {pct:>6.1f}%")
    
    # Null distribution — uniform random points (most conservative)
    print(f"\n  Null distribution (100K uniform random 2D points):")
    null_unif = null_partition_uniform(n_sim=100_000)
    null_unif_total = sum(null_unif.values())
    null_unif_422 = null_unif.get((4, 2, 2, 2, 2), 0)
    null_unif_rate = null_unif_422 / null_unif_total
    print(f"  Null rate of (4,2,2,2,2): {null_unif_422}/{null_unif_total} = {null_unif_rate:.1%}")
    
    # Statistical test: is (4,2,2,2,2) overrepresented?
    # Use T+dT results as primary
    partitions_primary = [r['partition'] for r in results_temp_dt.values()]
    n_obs_422 = sum(1 for p in partitions_primary if p == (4, 2, 2, 2, 2))
    n_obs_total = len(partitions_primary)
    
    # One-sided binomial test: is observed rate > null rate?
    from scipy.stats import binomtest
    binom_result = binomtest(n_obs_422, n_obs_total, null_rate, alternative='greater')
    print(f"\n  Binomial test (T+dT): observed={n_obs_422}/{n_obs_total}, "
          f"null_rate={null_rate:.4f}, p={binom_result.pvalue:.4f}")
    
    # Same for smooth-cycle null
    binom_smooth = binomtest(n_obs_422, n_obs_total, null_rate, alternative='greater')
    
    # ── Phase 4: Rate-of-change analysis ──
    print(f"\n\nPhase 4: Rate-of-change structure")
    print("-" * 50)
    
    transition_data = {}
    spacing_counts = Counter()
    
    for name, info in seasonal_cities.items():
        dT, trans, stable = analyze_rate_of_change(info['normals'])
        is_spaced, max_dev = check_transition_spacing(trans)
        transition_data[name] = {
            'dT': dT.tolist(),
            'transition_months': trans,
            'stable_months': stable,
            'evenly_spaced': is_spaced,
            'max_deviation': max_dev,
        }
        if is_spaced:
            spacing_counts['evenly_spaced'] += 1
        else:
            spacing_counts['not_spaced'] += 1
    
    n_spaced = spacing_counts['evenly_spaced']
    n_not = spacing_counts['not_spaced']
    n_tot = n_spaced + n_not
    print(f"\n  Transition months (top 4 by |dT|) evenly spaced (±1 month)?")
    print(f"  Yes: {n_spaced}/{n_tot} ({100*n_spaced/n_tot:.1f}%)")
    print(f"  No:  {n_not}/{n_tot} ({100*n_not/n_tot:.1f}%)")
    
    # What are the actual transition months?
    all_trans_months = Counter()
    for name, td in transition_data.items():
        for m in td['transition_months']:
            all_trans_months[m] += 1
    
    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    print(f"\n  Transition month frequency (across all seasonal cities):")
    print(f"  {'Month':>5} {'Count':>6} {'%':>7}")
    for m in range(12):
        count = all_trans_months[m]
        pct = 100 * count / n_tot
        predicted = m in [2, 5, 8, 11]  # Mar, Jun, Sep, Dec (0-indexed)
        marker = " ◄" if predicted else ""
        print(f"  {month_names[m]:>5} {count:>6} {pct:>6.1f}%{marker}")
    
    # Null expectation for spacing
    print(f"\n  Null: how often are 4 random months evenly spaced?")
    null_spaced = 0
    for _ in range(N_PERM):
        rand_months = sorted(RNG.choice(12, 4, replace=False))
        spaced, _ = check_transition_spacing(rand_months)
        if spaced:
            null_spaced += 1
    null_spacing_rate = null_spaced / N_PERM
    print(f"  Null rate: {null_spaced}/{N_PERM} = {null_spacing_rate:.1%}")
    obs_spacing_rate = n_spaced / n_tot
    print(f"  Observed rate: {obs_spacing_rate:.1%}")
    
    binom_spacing = binomtest(n_spaced, n_tot, null_spacing_rate, alternative='greater')
    print(f"  Binomial p-value: {binom_spacing.pvalue:.6f}")
    
    # ── Phase 5: By climate zone ──
    print(f"\n\nPhase 5: Results by climate zone")
    print("-" * 50)
    
    zone_partitions = defaultdict(list)
    zone_spacing = defaultdict(lambda: {'spaced': 0, 'total': 0})
    
    for name, info in seasonal_cities.items():
        zone = info['zone']
        pt = results_temp_dt[name]['partition']
        zone_partitions[zone].append(pt)
        zone_spacing[zone]['total'] += 1
        if transition_data[name]['evenly_spaced']:
            zone_spacing[zone]['spaced'] += 1
    
    print(f"\n  {'Zone':<15} {'N':>4} {'(4,2,2,2,2)':>12} {'%':>6}  {'Spaced':>8} {'%':>6}")
    print(f"  {'-'*55}")
    for zone in sorted(zone_partitions.keys()):
        parts = zone_partitions[zone]
        n = len(parts)
        n422 = sum(1 for p in parts if p == (4, 2, 2, 2, 2))
        sp = zone_spacing[zone]
        print(f"  {zone:<15} {n:>4} {n422:>12} {100*n422/n:>5.1f}%  "
              f"{sp['spaced']:>8} {100*sp['spaced']/sp['total']:>5.1f}%")
    
    # ── Summary ──
    print(f"\n\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    
    write_results(
        data, seasonal_cities, flat_cities,
        results_temp_dt, results_temp_only, results_multivar,
        null_dist, null_unif,
        transition_data, all_trans_months,
        zone_partitions, zone_spacing,
        n_obs_422, n_obs_total, null_rate, binom_result,
        n_spaced, n_tot, null_spacing_rate, binom_spacing,
    )


def write_results(
    data, seasonal_cities, flat_cities,
    results_temp_dt, results_temp_only, results_multivar,
    null_dist, null_unif,
    transition_data, all_trans_months,
    zone_partitions, zone_spacing,
    n_obs_422, n_obs_total, null_rate, binom_result,
    n_spaced, n_tot, null_spacing_rate, binom_spacing,
):
    """Write results to markdown."""
    month_names = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    
    lines = [
        "# Resonance Test 3: Empirical Asymmetry in Climate Cycles",
        "",
        "## Prediction",
        "",
        "The {4,2,2,2,2} cascade assigns Earth to 4/12 branch positions",
        "(inter-seasonal transitions: months 3, 6, 9, 12). If the five-phase",
        "model captures something real about seasonal dynamics, natural 12-month",
        "temperature cycles should partition into 5 groups with {4,2,2,2,2} structure,",
        "where the 4-member group consists of transition months.",
        "",
        "## Data",
        "",
        f"- {len(data)} cities worldwide, 30-year normals (1991-2020)",
        f"- {len(seasonal_cities)} seasonal (monthly std > 2°C)",
        f"- {len(flat_cities)} flat (excluded): {', '.join(flat_cities.keys())}",
        "",
        "## Phase 2: Partition Types (k=5 clustering)",
        "",
    ]
    
    for method_name, results in [("T+dT", results_temp_dt), 
                                   ("T only", results_temp_only),
                                   ("T+D+dT+dD", results_multivar)]:
        partitions = [r['partition'] for r in results.values()]
        dist = Counter(partitions)
        total = len(partitions)
        
        lines.append(f"### {method_name} ({total} cities)")
        lines.append("")
        lines.append("| Partition | Count | % |")
        lines.append("|-----------|-------|---|")
        for pt, count in dist.most_common():
            pct = 100 * count / total
            marker = " **◄ PREDICTED**" if pt == (4, 2, 2, 2, 2) else ""
            lines.append(f"| {pt} | {count} | {pct:.1f}%{marker} |")
        lines.append("")
    
    lines += [
        "## Phase 3: Statistical Test",
        "",
        f"Observed (T+dT): {n_obs_422}/{n_obs_total} = {100*n_obs_422/n_obs_total:.1f}% are (4,2,2,2,2)",
        "",
        "### Null distributions",
        "",
        f"- Smooth annual cycles (100K sims): {100*null_rate:.1f}% are (4,2,2,2,2)",
        "",
    ]
    
    # Null top partitions
    null_total = sum(null_dist.values())
    lines.append("Top null partitions (smooth cycles):")
    lines.append("")
    lines.append("| Partition | Count | % |")
    lines.append("|-----------|-------|---|")
    for pt, count in null_dist.most_common(8):
        pct = 100 * count / null_total
        lines.append(f"| {pt} | {count} | {pct:.1f}% |")
    lines.append("")
    
    null_unif_total = sum(null_unif.values())
    null_unif_422 = null_unif.get((4, 2, 2, 2, 2), 0)
    lines.append(f"Uniform random null: {100*null_unif_422/null_unif_total:.1f}% are (4,2,2,2,2)")
    lines.append("")
    
    lines.append(f"**Binomial test**: p = {binom_result.pvalue:.4f}")
    lines.append("")
    
    lines += [
        "## Phase 4: Rate-of-Change Structure",
        "",
        f"Top 4 months by |dT| are evenly spaced (±1 month): "
        f"{n_spaced}/{n_tot} = {100*n_spaced/n_tot:.1f}%",
        f"Null rate: {100*null_spacing_rate:.1f}%",
        f"Binomial p: {binom_spacing.pvalue:.6f}",
        "",
        "### Transition month frequency",
        "",
        "| Month | Count | % | Predicted? |",
        "|-------|-------|---|------------|",
    ]
    for m in range(12):
        count = all_trans_months[m]
        pct = 100 * count / n_tot
        predicted = "✓" if m in [2, 5, 8, 11] else ""
        lines.append(f"| {month_names[m]} | {count} | {pct:.1f}% | {predicted} |")
    
    lines += [
        "",
        "## Phase 5: By Climate Zone",
        "",
        "| Zone | N | (4,2,2,2,2) | % | Spaced | % |",
        "|------|---|-------------|---|--------|---|",
    ]
    for zone in sorted(zone_partitions.keys()):
        parts = zone_partitions[zone]
        n = len(parts)
        n422 = sum(1 for p in parts if p == (4, 2, 2, 2, 2))
        sp = zone_spacing[zone]
        lines.append(
            f"| {zone} | {n} | {n422} | {100*n422/n:.1f}% | "
            f"{sp['spaced']} | {100*sp['spaced']/sp['total']:.1f}% |"
        )
    
    out_path = OUT_DIR / "resonance_test3_results.md"
    out_path.write_text("\n".join(lines))
    print(f"\nResults written to {out_path}")


if __name__ == '__main__':
    main()
