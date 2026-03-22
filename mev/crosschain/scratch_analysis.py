import pandas as pd
import numpy as np

df = pd.read_csv('data/swaps_daily.csv')
depths = pd.read_csv('data/depths_daily.csv')

# === Conjecture 1: Correction ratio volatility as stress indicator ===
btc = df[(df['pool'] == 'BTC.BTC') & (df['date'] >= '2024-07-01')].copy()
btc['organic_net'] = btc['toAssetVolumeUSD'] - btc['toRuneVolumeUSD']
btc['trade_net'] = btc['toTradeVolumeUSD'] - btc['fromTradeVolumeUSD']

# Correction ratio: -trade_net / organic_net (should be ~1.0 when stable)
# Use absolute values to avoid sign confusion
mask = btc['organic_net'].abs() > 50e6  # filter noise
btc.loc[mask, 'corr_ratio'] = -btc.loc[mask, 'trade_net'] / btc.loc[mask, 'organic_net']
btc['corr_ratio_7d_std'] = btc['corr_ratio'].rolling(7, min_periods=3).std()

# Get BTC price
btc_depth = depths[depths['pool'] == 'BTC.BTC'][['date', 'assetPriceUSD']].copy()
btc_depth.columns = ['date', 'btc_price']
btc = btc.merge(btc_depth, on='date', how='left')
btc['price_return'] = btc['btc_price'].pct_change()
btc['next_day_return'] = btc['price_return'].shift(-1)
btc['next_3d_return'] = btc['btc_price'].shift(-3) / btc['btc_price'] - 1
btc['abs_return_5d'] = btc['price_return'].abs().rolling(5).mean()

print("=== Correction ratio 7d std vs subsequent volatility ===")
# When correction ratio variance is high, does volatility follow?
btc_valid = btc.dropna(subset=['corr_ratio_7d_std', 'abs_return_5d'])
high_var = btc_valid['corr_ratio_7d_std'] > btc_valid['corr_ratio_7d_std'].quantile(0.8)
low_var = btc_valid['corr_ratio_7d_std'] < btc_valid['corr_ratio_7d_std'].quantile(0.2)

print(f"High corr_ratio variance periods:")
print(f"  Mean abs 5d return: {btc_valid[high_var]['abs_return_5d'].mean()*100:.2f}%")
print(f"  Mean next-3d return: {btc_valid[high_var]['next_3d_return'].mean()*100:.2f}%")
print(f"Low corr_ratio variance periods:")
print(f"  Mean abs 5d return: {btc_valid[low_var]['abs_return_5d'].mean()*100:.2f}%")
print(f"  Mean next-3d return: {btc_valid[low_var]['next_3d_return'].mean()*100:.2f}%")

# Show the correction ratio during known stress periods
print("\n=== Correction ratio timeline: Aug 2024 crash ===")
aug = btc[(btc['date'] >= '2024-07-28') & (btc['date'] <= '2024-08-10')]
for _, r in aug.iterrows():
    cr = f"{r.corr_ratio:.2f}" if pd.notna(r.corr_ratio) else "N/A"
    std7 = f"{r.corr_ratio_7d_std:.3f}" if pd.notna(r.corr_ratio_7d_std) else "N/A"
    print(f"  {r.date}: ratio={cr}, 7d_std={std7}, price=${r.btc_price:.0f}")

print("\n=== Correction ratio timeline: Jan-Feb 2025 crash ===")
jan = btc[(btc['date'] >= '2025-01-18') & (btc['date'] <= '2025-02-05')]
for _, r in jan.iterrows():
    cr = f"{r.corr_ratio:.2f}" if pd.notna(r.corr_ratio) else "N/A"
    std7 = f"{r.corr_ratio_7d_std:.3f}" if pd.notna(r.corr_ratio_7d_std) else "N/A"
    print(f"  {r.date}: ratio={cr}, 7d_std={std7}, price=${r.btc_price:.0f}")

# === Conjecture 2: Organic contrarian signal ===
print("\n=== Conjecture 2: Organic contrarian buys ===")
# Contrarian buy: organic buying (positive net) while price dropping
contrarian_buy = btc[(btc['organic_net'] > 100e6) & (btc['price_return'] < -0.01)]
agree_sell = btc[(btc['organic_net'] < -100e6) & (btc['price_return'] < -0.01)]

print(f"Contrarian buy days (organic >100M, price fell >1%): {len(contrarian_buy)}")
if len(contrarian_buy) > 0:
    print(f"  Mean next-day return: {contrarian_buy['next_day_return'].mean()*100:.2f}%")
    print(f"  Mean next-3d return: {contrarian_buy['next_3d_return'].mean()*100:.2f}%")
    pct_pos = (contrarian_buy['next_day_return'] > 0).mean() * 100
    print(f"  % positive next-day: {pct_pos:.0f}%")
    print(f"  Details:")
    for _, r in contrarian_buy.iterrows():
        nd = f"{r.next_day_return*100:.1f}%" if pd.notna(r.next_day_return) else "N/A"
        n3 = f"{r.next_3d_return*100:.1f}%" if pd.notna(r.next_3d_return) else "N/A"
        print(f"    {r.date}: org={r.organic_net/1e6:+.0f}M, ret={r.price_return*100:.1f}%, next_d={nd}, next_3d={n3}")

print(f"\nAgreeing sell days (organic <-100M, price fell >1%): {len(agree_sell)}")
if len(agree_sell) > 0:
    print(f"  Mean next-day return: {agree_sell['next_day_return'].mean()*100:.2f}%")
    print(f"  Mean next-3d return: {agree_sell['next_3d_return'].mean()*100:.2f}%")
    pct_pos = (agree_sell['next_day_return'] > 0).mean() * 100
    print(f"  % positive next-day: {pct_pos:.0f}%")

# === Conjecture 3: Synth era vs trade era signal quality ===
print("\n=== Conjecture 3: Signal quality across eras ===")
# For the synth era, compute a unified net flow: organic_net + synth_net
btc_all = df[df['pool'] == 'BTC.BTC'].copy()
btc_all['organic_net'] = btc_all['toAssetVolumeUSD'] - btc_all['toRuneVolumeUSD']
btc_all['synth_net'] = btc_all['synthMintVolumeUSD'] - btc_all['synthRedeemVolumeUSD']
btc_all['trade_net'] = btc_all['toTradeVolumeUSD'] - btc_all['fromTradeVolumeUSD']
btc_all['unified_net'] = btc_all['organic_net'] + btc_all['synth_net'] + btc_all['trade_net']
btc_all = btc_all.merge(btc_depth, on='date', how='left')
btc_all['price_return'] = btc_all['btc_price'].pct_change()

# Correlation of unified_net with price_return by era
synth_era = btc_all[(btc_all['date'] >= '2022-06-01') & (btc_all['date'] < '2024-06-01') & (btc_all['totalVolumeUSD'] > 0)]
trade_era = btc_all[(btc_all['date'] >= '2024-07-01') & (btc_all['totalVolumeUSD'] > 0)]

for name, era in [("Synth era (Jun 2022 - May 2024)", synth_era), ("Trade era (Jul 2024 - now)", trade_era)]:
    corr_org = era['organic_net'].corr(era['price_return'])
    corr_unified = era['unified_net'].corr(era['price_return'])
    vol_std = era['unified_net'].std() / 1e6
    mean_abs_net = era['unified_net'].abs().mean() / 1e6
    print(f"\n{name}:")
    print(f"  organic_net vs price_return correlation: {corr_org:.3f}")
    print(f"  unified_net vs price_return correlation: {corr_unified:.3f}")
    print(f"  Mean |unified_net|: {mean_abs_net:.0f}M")
    print(f"  Std unified_net: {vol_std:.0f}M")
    print(f"  N days: {len(era)}")
