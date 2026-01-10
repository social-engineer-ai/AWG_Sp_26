# =============================================================================
# IMPORTS
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage
from IPython.display import display
import warnings

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', '{:,.2f}'.format)

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = [12, 6]

# Division mapping
DIVISIONS = {
    'KC': 'Kansas City', 'SP': 'Springfield', 'OK': 'Oklahoma',
    'NA': 'Nashville', 'GC': 'Gulf Coast', 'NE': 'Nebraska',
    'GL': 'Great Lakes', 'HN': 'Hernando', 'UM': 'Upper Midwest'
}

REGIONS = {
    'KC': 'Central', 'SP': 'Central', 'OK': 'South',
    'NA': 'Southeast', 'GC': 'South', 'NE': 'North',
    'GL': 'North', 'HN': 'Southeast', 'UM': 'North'
}

print("Setup complete!")

# =============================================================================
# LOAD PREPARED DATA
# =============================================================================

DATA_DIR = r'C:\Users\ashishk\Dropbox\My PC (BUS-P10E67720)\Documents\Development\AWG_Spring_26\prepared_data_normalized'

# Load pricing long format
df = pd.read_csv(f'{DATA_DIR}/pricing_long.csv')

# Load product master
df_products = pd.read_csv(f'{DATA_DIR}/product_master.csv')

# Add product info
df = pd.merge(df, df_products[['Item Code', 'Item Name', 'Category', 'Brand Label Name']], 
              left_on='item_code', right_on='Item Code', how='left')

# Add region
df['region'] = df['division'].map(REGIONS)

print(f"Pricing data: {len(df):,} rows")
print(f"Divisions: {df['division'].nunique()}")

# =============================================================================
# AVERAGE PRICES BY DIVISION
# =============================================================================

division_prices = df.groupby('division').agg({
    'list_cost': 'mean',
    'bsp': 'mean',
    'city_srp': 'mean',
    'rural_srp': 'mean',
    'item_code': 'count'
}).round(2)

division_prices.columns = ['Avg List Cost', 'Avg BSP', 'Avg City SRP', 'Avg Rural SRP', 'Observations']
division_prices['Division Name'] = division_prices.index.map(DIVISIONS)
division_prices['Region'] = division_prices.index.map(REGIONS)

print("Average Prices by Division:")
display(division_prices)

# =============================================================================
# PRICE COMPARISON VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

divisions = division_prices.index.tolist()
x_pos = range(len(divisions))

# List Cost
axes[0, 0].bar(x_pos, division_prices['Avg List Cost'], color='steelblue', edgecolor='black')
axes[0, 0].set_xticks(x_pos)
axes[0, 0].set_xticklabels(divisions)
axes[0, 0].set_ylabel('Average List Cost ($)')
axes[0, 0].set_title('Average List Cost by Division', fontweight='bold')
axes[0, 0].axhline(y=division_prices['Avg List Cost'].mean(), color='red', linestyle='--', label='Overall Mean')
axes[0, 0].legend()

# BSP
axes[0, 1].bar(x_pos, division_prices['Avg BSP'], color='coral', edgecolor='black')
axes[0, 1].set_xticks(x_pos)
axes[0, 1].set_xticklabels(divisions)
axes[0, 1].set_ylabel('Average BSP ($)')
axes[0, 1].set_title('Average BSP by Division', fontweight='bold')
axes[0, 1].axhline(y=division_prices['Avg BSP'].mean(), color='red', linestyle='--', label='Overall Mean')
axes[0, 1].legend()

# City SRP
axes[1, 0].bar(x_pos, division_prices['Avg City SRP'], color='green', edgecolor='black')
axes[1, 0].set_xticks(x_pos)
axes[1, 0].set_xticklabels(divisions)
axes[1, 0].set_ylabel('Average City SRP ($)')
axes[1, 0].set_title('Average City SRP by Division', fontweight='bold')
axes[1, 0].axhline(y=division_prices['Avg City SRP'].mean(), color='red', linestyle='--', label='Overall Mean')
axes[1, 0].legend()

# Rural SRP
axes[1, 1].bar(x_pos, division_prices['Avg Rural SRP'], color='purple', edgecolor='black')
axes[1, 1].set_xticks(x_pos)
axes[1, 1].set_xticklabels(divisions)
axes[1, 1].set_ylabel('Average Rural SRP ($)')
axes[1, 1].set_title('Average Rural SRP by Division', fontweight='bold')
axes[1, 1].axhline(y=division_prices['Avg Rural SRP'].mean(), color='red', linestyle='--', label='Overall Mean')
axes[1, 1].legend()

plt.tight_layout()
plt.show()

# =============================================================================
# LIST COST CONSISTENCY CHECK
# =============================================================================

print("="*60)
print("LIST COST CONSISTENCY CHECK")
print("="*60)
print("\nExpectation: List Cost should be SAME across all divisions")

# For each item+quarter, check if list cost varies across divisions
list_cost_variation = df.groupby(['item_code', 'quarter'])['list_cost'].agg(['mean', 'std', 'count'])
list_cost_variation = list_cost_variation[list_cost_variation['count'] > 1]  # Multiple divisions

# Items with varying list cost
varying_cost = list_cost_variation[list_cost_variation['std'] > 0.01]

print(f"\nItem-quarters with data in multiple divisions: {len(list_cost_variation):,}")
print(f"Item-quarters with VARYING List Cost: {len(varying_cost):,} ({len(varying_cost)/len(list_cost_variation)*100:.1f}%)")

if len(varying_cost) > 0:
    print("\n⚠ Some items have different List Costs across divisions!")
    print(f"   Average variation (std): ${varying_cost['std'].mean():.2f}")
else:
    print("\n✓ List Cost is consistent across divisions")

# =============================================================================
# PRICE COEFFICIENT OF VARIATION BY ITEM
# =============================================================================

# Calculate CV (std/mean) for each item across divisions
item_price_cv = df.groupby('item_code').agg({
    'bsp': lambda x: x.std() / x.mean() * 100 if x.mean() > 0 else np.nan,
    'city_srp': lambda x: x.std() / x.mean() * 100 if x.mean() > 0 else np.nan,
}).round(2)

item_price_cv.columns = ['BSP_CV', 'City_SRP_CV']
item_price_cv = item_price_cv.dropna()

print("\nPrice Coefficient of Variation Across Divisions:")
print("-" * 50)
print(f"\nBSP Variation:")
print(f"  Mean CV: {item_price_cv['BSP_CV'].mean():.1f}%")
print(f"  Median CV: {item_price_cv['BSP_CV'].median():.1f}%")
print(f"  Items with >10% CV: {(item_price_cv['BSP_CV'] > 10).sum():,}")

print(f"\nCity SRP Variation:")
print(f"  Mean CV: {item_price_cv['City_SRP_CV'].mean():.1f}%")
print(f"  Median CV: {item_price_cv['City_SRP_CV'].median():.1f}%")
print(f"  Items with >10% CV: {(item_price_cv['City_SRP_CV'] > 10).sum():,}")

# =============================================================================
# CITY VS RURAL SRP GAP
# =============================================================================

# Calculate city-rural gap
df_srp = df[(df['city_srp'].notna()) & (df['rural_srp'].notna())].copy()
df_srp['city_rural_gap'] = df_srp['rural_srp'] - df_srp['city_srp']
df_srp['city_rural_gap_pct'] = (df_srp['city_rural_gap'] / df_srp['city_srp']) * 100

# Summary by division
division_srp_gap = df_srp.groupby('division').agg({
    'city_srp': 'mean',
    'rural_srp': 'mean',
    'city_rural_gap': 'mean',
    'city_rural_gap_pct': 'mean'
}).round(2)

division_srp_gap.columns = ['Avg City SRP', 'Avg Rural SRP', 'Avg Gap ($)', 'Avg Gap (%)']

print("City vs Rural SRP by Division:")
display(division_srp_gap)

# =============================================================================
# CITY-RURAL GAP VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gap by division
divisions = division_srp_gap.index.tolist()
axes[0].bar(divisions, division_srp_gap['Avg Gap (%)'], color='teal', edgecolor='black')
axes[0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[0].set_xlabel('Division')
axes[0].set_ylabel('City-Rural Gap (%)')
axes[0].set_title('City-Rural SRP Gap by Division', fontweight='bold')

# Distribution of gaps
axes[1].hist(df_srp['city_rural_gap_pct'], bins=50, edgecolor='black', alpha=0.7)
axes[1].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Equal Pricing')
axes[1].axvline(x=df_srp['city_rural_gap_pct'].median(), color='green', linestyle='--', linewidth=2,
                label=f'Median ({df_srp["city_rural_gap_pct"].median():.1f}%)')
axes[1].set_xlabel('City-Rural Gap (%)')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Distribution of City-Rural SRP Gap', fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.show()

print(f"\nOverall: Rural SRP is {'higher' if df_srp['city_rural_gap_pct'].median() > 0 else 'lower'} than City SRP by {abs(df_srp['city_rural_gap_pct'].median()):.1f}% on average")

# =============================================================================
# MARKUP ANALYSIS
# =============================================================================

# Calculate markups
df_markup = df[(df['list_cost'] > 0) & (df['bsp'] > 0) & (df['city_srp'] > 0)].copy()

df_markup['bsp_markup_pct'] = ((df_markup['bsp'] - df_markup['list_cost']) / df_markup['list_cost']) * 100
df_markup['srp_markup_pct'] = ((df_markup['city_srp'] - df_markup['bsp']) / df_markup['bsp']) * 100
df_markup['total_markup_pct'] = ((df_markup['city_srp'] - df_markup['list_cost']) / df_markup['list_cost']) * 100

# Summary by division
division_markup = df_markup.groupby('division').agg({
    'bsp_markup_pct': 'mean',
    'srp_markup_pct': 'mean',
    'total_markup_pct': 'mean'
}).round(1)

division_markup.columns = ['AWG Markup (Cost→BSP)', 'Retail Markup (BSP→SRP)', 'Total Markup (Cost→SRP)']

print("Markup Percentages by Division:")
display(division_markup)

# =============================================================================
# MARKUP VISUALIZATION
# =============================================================================

fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(len(division_markup))
width = 0.25

bars1 = ax.bar(x - width, division_markup['AWG Markup (Cost→BSP)'], width, label='AWG Markup', color='steelblue')
bars2 = ax.bar(x, division_markup['Retail Markup (BSP→SRP)'], width, label='Retail Markup', color='coral')
bars3 = ax.bar(x + width, division_markup['Total Markup (Cost→SRP)'], width, label='Total Markup', color='green')

ax.set_xlabel('Division')
ax.set_ylabel('Markup (%)')
ax.set_title('Markup Percentages by Division', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(division_markup.index)
ax.legend()

plt.tight_layout()
plt.show()

# =============================================================================
# PRICE HEATMAP BY DIVISION
# =============================================================================

# Create price index (division avg / overall avg)
price_index = df.groupby('division')[['bsp', 'city_srp']].mean()
overall_avg = df[['bsp', 'city_srp']].mean()

price_index['bsp_index'] = (price_index['bsp'] / overall_avg['bsp']) * 100
price_index['srp_index'] = (price_index['city_srp'] / overall_avg['city_srp']) * 100

fig, ax = plt.subplots(figsize=(10, 6))

heatmap_data = price_index[['bsp_index', 'srp_index']]
heatmap_data.columns = ['BSP Index', 'SRP Index']

sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn_r', center=100,
            cbar_kws={'label': 'Price Index (100 = Average)'}, ax=ax)

ax.set_title('Price Index by Division\n(100 = Overall Average)', fontweight='bold')
ax.set_ylabel('Division')

plt.tight_layout()
plt.show()

# =============================================================================
# REGIONAL SUMMARY
# =============================================================================

regional_summary = df.groupby('region').agg({
    'bsp': 'mean',
    'city_srp': 'mean',
    'item_code': 'count'
}).round(2)

regional_summary.columns = ['Avg BSP', 'Avg City SRP', 'Observations']

print("\nRegional Price Summary:")
display(regional_summary)

# =============================================================================
# EXECUTIVE SUMMARY
# =============================================================================

print("="*70)
print("RQ5: GEOGRAPHIC VARIATION - EXECUTIVE SUMMARY")
print("="*70)

print("\n1. LIST COST CONSISTENCY")
if len(varying_cost) / len(list_cost_variation) < 0.05:
    print("   ✓ List Cost is largely consistent across divisions")
else:
    print(f"   ⚠ {len(varying_cost)/len(list_cost_variation)*100:.1f}% of items have varying List Cost")

print("\n2. BSP VARIATION")
print(f"   - Average CV across divisions: {item_price_cv['BSP_CV'].mean():.1f}%")
print(f"   - Highest BSP division: {division_prices['Avg BSP'].idxmax()} (${division_prices['Avg BSP'].max():.2f})")
print(f"   - Lowest BSP division: {division_prices['Avg BSP'].idxmin()} (${division_prices['Avg BSP'].min():.2f})")

print("\n3. CITY-RURAL GAP")
print(f"   - Median gap: {df_srp['city_rural_gap_pct'].median():.1f}%")
print(f"   - Rural prices are {'higher' if df_srp['city_rural_gap_pct'].median() > 0 else 'similar to'} city prices")

print("\n4. MARKUP ANALYSIS")
print(f"   - Avg AWG markup: {division_markup['AWG Markup (Cost→BSP)'].mean():.1f}%")
print(f"   - Avg Retail markup: {division_markup['Retail Markup (BSP→SRP)'].mean():.1f}%")

print("\n5. RECOMMENDATIONS")
print("   - Monitor divisions with above-average pricing")
print("   - Review city-rural pricing strategy")
print("   - Consider regional pricing optimization")
