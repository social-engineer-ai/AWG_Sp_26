# =============================================================================
# IMPORTS
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Markdown
import warnings

warnings.filterwarnings('ignore')

# Display settings
pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', '{:,.2f}'.format)

# Plot settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['font.size'] = 11

# Color scheme
COLORS = {'Best Choice': '#2ecc71', 'Always Save': '#3498db', 'National Brand': '#e74c3c'}
TARGET_GAP = 20  # Target price gap percentage

print("Setup complete!")

# =============================================================================
# LOAD PREPARED DATA (NORMALIZED - Using Unit Prices)
# =============================================================================

DATA_DIR = r'C:\Users\ashishk\Dropbox\My PC (BUS-P10E67720)\Documents\Development\AWG_Spring_26\prepared_data_normalized'

# Load BC-National comparison dataset (primary for this analysis)
df = pd.read_csv(f'{DATA_DIR}/bc_national_comparison.csv')

# Load product master for reference
df_products = pd.read_csv(f'{DATA_DIR}/product_master.csv')

print(f"BC-National Comparison data: {len(df):,} rows")
print(f"Product master: {len(df_products):,} products")
print(f"\nNote: Using NORMALIZED data with unit-level prices (BSP/Pack)")

# =============================================================================
# DATA OVERVIEW
# =============================================================================

print("Columns available:")
print(df.columns.tolist())

print("\nData preview:")
df.head()

# =============================================================================
# FILTER TO VALID PRICE GAP DATA
# =============================================================================

# Filter to rows with valid price gap calculations (using unit prices)
df_valid = df[
    df['price_gap_pct'].notna() & 
    (df['bsp_per_unit'] > 0) & 
    (df['national_bsp_per_unit'] > 0)
].copy()

print(f"Rows with valid price gap data: {len(df_valid):,} ({len(df_valid)/len(df)*100:.1f}%)")
print(f"Unique BC items: {df_valid['item_code'].nunique():,}")
print(f"Divisions: {df_valid['division'].nunique()}")
print(f"Quarters: {df_valid['quarter'].unique().tolist()}")
print(f"\nPrice gap calculated using: BSP per Unit (case price / pack size)")

# =============================================================================
# PRICE GAP SUMMARY STATISTICS
# =============================================================================

print("="*60)
print("PRICE GAP SUMMARY STATISTICS")
print("="*60)

gap_stats = df_valid['price_gap_pct'].describe(percentiles=[.10, .25, .50, .75, .90])
print(f"\nPrice Gap (%) Statistics:")
print(gap_stats.round(2))

print(f"\n--- Key Findings ---")
print(f"Mean price gap: {df_valid['price_gap_pct'].mean():.1f}%")
print(f"Median price gap: {df_valid['price_gap_pct'].median():.1f}%")
print(f"Target gap: {TARGET_GAP}%")
print(f"Gap vs Target: {df_valid['price_gap_pct'].mean() - TARGET_GAP:+.1f}% points")

# =============================================================================
# PRICE GAP DISTRIBUTION HISTOGRAM
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(df_valid['price_gap_pct'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].axvline(x=TARGET_GAP, color='red', linestyle='--', linewidth=2, label=f'Target ({TARGET_GAP}%)')
axes[0].axvline(x=df_valid['price_gap_pct'].mean(), color='green', linestyle='--', linewidth=2, 
                label=f'Mean ({df_valid["price_gap_pct"].mean():.1f}%)')
axes[0].axvline(x=df_valid['price_gap_pct'].median(), color='orange', linestyle='--', linewidth=2,
                label=f'Median ({df_valid["price_gap_pct"].median():.1f}%)')
axes[0].set_xlabel('Price Gap (%)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of BC vs National Brand Price Gaps', fontweight='bold')
axes[0].legend()

# Box plot
axes[1].boxplot(df_valid['price_gap_pct'].dropna(), vert=True)
axes[1].axhline(y=TARGET_GAP, color='red', linestyle='--', linewidth=2, label=f'Target ({TARGET_GAP}%)')
axes[1].set_ylabel('Price Gap (%)')
axes[1].set_title('Price Gap Box Plot', fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.show()

print("\nInterpretation:")
print(f"- The actual price gap ({df_valid['price_gap_pct'].mean():.1f}%) is {'above' if df_valid['price_gap_pct'].mean() > TARGET_GAP else 'below'} the {TARGET_GAP}% target")
print(f"- This suggests BC products may be priced {'too low' if df_valid['price_gap_pct'].mean() > TARGET_GAP else 'appropriately'} relative to National Brands")

# =============================================================================
# PRICE GAP CATEGORIES
# =============================================================================

# Categorize price gaps
def categorize_gap(gap):
    if gap < 10:
        return '< 10% (Too Small)'
    elif gap < 20:
        return '10-20% (Below Target)'
    elif gap < 30:
        return '20-30% (Near Target)'
    elif gap < 40:
        return '30-40% (Above Target)'
    else:
        return '> 40% (Very Large)'

df_valid['gap_category'] = df_valid['price_gap_pct'].apply(categorize_gap)

# Summary by category
gap_category_summary = df_valid['gap_category'].value_counts().sort_index()
gap_category_pct = (gap_category_summary / len(df_valid) * 100).round(1)

print("\nPrice Gap Distribution by Category:")
print("-" * 50)
for cat, count in gap_category_summary.items():
    pct = gap_category_pct[cat]
    print(f"  {cat}: {count:,} ({pct}%)")

# =============================================================================
# PRICE GAP BY CATEGORY
# =============================================================================

# Aggregate by category
category_gaps = df_valid.groupby('category').agg({
    'price_gap_pct': ['mean', 'median', 'std', 'count'],
    'item_code': 'nunique'
}).round(2)

category_gaps.columns = ['avg_gap', 'median_gap', 'std_gap', 'observations', 'unique_items']
category_gaps = category_gaps.sort_values('avg_gap', ascending=False)

# Filter to categories with sufficient data
category_gaps_filtered = category_gaps[category_gaps['observations'] >= 20]

print(f"Categories with 20+ observations: {len(category_gaps_filtered)}")
print("\nTop 15 Categories by Average Price Gap:")
display(category_gaps_filtered.head(15))

# =============================================================================
# PRICE GAP BY CATEGORY - VISUALIZATION
# =============================================================================

# Top 20 categories
top_categories = category_gaps_filtered.head(20)

fig, ax = plt.subplots(figsize=(12, 8))

colors = ['green' if x <= 25 else 'orange' if x <= 35 else 'red' for x in top_categories['avg_gap']]

bars = ax.barh(range(len(top_categories)), top_categories['avg_gap'], color=colors, edgecolor='black')
ax.axvline(x=TARGET_GAP, color='red', linestyle='--', linewidth=2, label=f'Target ({TARGET_GAP}%)')

ax.set_yticks(range(len(top_categories)))
ax.set_yticklabels(top_categories.index)
ax.set_xlabel('Average Price Gap (%)')
ax.set_title('Price Gap by Category (Top 20 by Gap Size)', fontweight='bold')
ax.legend()

# Add value labels
for i, v in enumerate(top_categories['avg_gap']):
    ax.text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=9)

plt.tight_layout()
plt.show()

# =============================================================================
# CATEGORIES CLOSEST TO TARGET (20%)
# =============================================================================

category_gaps_filtered['gap_vs_target'] = abs(category_gaps_filtered['avg_gap'] - TARGET_GAP)
closest_to_target = category_gaps_filtered.sort_values('gap_vs_target').head(10)

print("\nCategories Closest to 20% Target Gap:")
display(closest_to_target[['avg_gap', 'median_gap', 'observations', 'gap_vs_target']])

# =============================================================================
# PRICE GAP BY DIVISION
# =============================================================================

division_gaps = df_valid.groupby('division').agg({
    'price_gap_pct': ['mean', 'median', 'std'],
    'item_code': 'nunique'
}).round(2)

division_gaps.columns = ['avg_gap', 'median_gap', 'std_gap', 'unique_items']
division_gaps = division_gaps.sort_values('avg_gap', ascending=False)

# Add division names
DIVISIONS = {
    'KC': 'Kansas City', 'SP': 'Springfield', 'OK': 'Oklahoma',
    'NA': 'Nashville', 'GC': 'Gulf Coast', 'NE': 'Nebraska',
    'GL': 'Great Lakes', 'HN': 'Hernando', 'UM': 'Upper Midwest'
}
division_gaps['division_name'] = division_gaps.index.map(DIVISIONS)

print("Price Gap by Division:")
display(division_gaps)

# =============================================================================
# PRICE GAP BY DIVISION - VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart
colors = ['green' if x <= 25 else 'orange' if x <= 35 else 'red' for x in division_gaps['avg_gap']]
axes[0].bar(division_gaps.index, division_gaps['avg_gap'], color=colors, edgecolor='black')
axes[0].axhline(y=TARGET_GAP, color='red', linestyle='--', linewidth=2, label=f'Target ({TARGET_GAP}%)')
axes[0].set_xlabel('Division')
axes[0].set_ylabel('Average Price Gap (%)')
axes[0].set_title('Average Price Gap by Division', fontweight='bold')
axes[0].legend()

# Add value labels
for i, (div, gap) in enumerate(zip(division_gaps.index, division_gaps['avg_gap'])):
    axes[0].text(i, gap + 0.5, f'{gap:.1f}%', ha='center', fontsize=9)

# Box plot by division
division_order = division_gaps.index.tolist()
df_valid['division_ordered'] = pd.Categorical(df_valid['division'], categories=division_order, ordered=True)
df_valid.boxplot(column='price_gap_pct', by='division', ax=axes[1])
axes[1].axhline(y=TARGET_GAP, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Division')
axes[1].set_ylabel('Price Gap (%)')
axes[1].set_title('Price Gap Distribution by Division', fontweight='bold')
plt.suptitle('')  # Remove automatic title

plt.tight_layout()
plt.show()

print("\nKey Finding:")
gap_range = division_gaps['avg_gap'].max() - division_gaps['avg_gap'].min()
print(f"Division gap range: {gap_range:.1f}% points (from {division_gaps['avg_gap'].min():.1f}% to {division_gaps['avg_gap'].max():.1f}%)")

# =============================================================================
# PRICE GAP BY QUARTER
# =============================================================================

quarter_gaps = df_valid.groupby('quarter').agg({
    'price_gap_pct': ['mean', 'median', 'std'],
    'item_code': 'nunique'
}).round(2)

quarter_gaps.columns = ['avg_gap', 'median_gap', 'std_gap', 'unique_items']

print("Price Gap by Quarter:")
display(quarter_gaps)

# =============================================================================
# PRICE GAP TREND VISUALIZATION
# =============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

quarters = ['Q1', 'Q2', 'Q3', 'Q4']
quarter_gaps_ordered = quarter_gaps.reindex(quarters)

ax.plot(quarters, quarter_gaps_ordered['avg_gap'], marker='o', linewidth=2, markersize=10, label='Average Gap')
ax.plot(quarters, quarter_gaps_ordered['median_gap'], marker='s', linewidth=2, markersize=8, label='Median Gap')
ax.axhline(y=TARGET_GAP, color='red', linestyle='--', linewidth=2, label=f'Target ({TARGET_GAP}%)')

ax.fill_between(quarters, 
                quarter_gaps_ordered['avg_gap'] - quarter_gaps_ordered['std_gap'],
                quarter_gaps_ordered['avg_gap'] + quarter_gaps_ordered['std_gap'],
                alpha=0.2, label='±1 Std Dev')

ax.set_xlabel('Quarter')
ax.set_ylabel('Price Gap (%)')
ax.set_title('Price Gap Trend Over Quarters', fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Calculate Q1 to Q4 change
if 'Q1' in quarter_gaps_ordered.index and 'Q4' in quarter_gaps_ordered.index:
    q1_gap = quarter_gaps_ordered.loc['Q1', 'avg_gap']
    q4_gap = quarter_gaps_ordered.loc['Q4', 'avg_gap']
    change = q4_gap - q1_gap
    print(f"\nQ1 to Q4 Change: {change:+.1f}% points")
    print(f"  Q1 average gap: {q1_gap:.1f}%")
    print(f"  Q4 average gap: {q4_gap:.1f}%")

# =============================================================================
# PRICE GAP TREND BY DIVISION
# =============================================================================

# Pivot for heatmap
gap_pivot = df_valid.pivot_table(
    values='price_gap_pct',
    index='division',
    columns='quarter',
    aggfunc='mean'
).reindex(columns=['Q1', 'Q2', 'Q3', 'Q4'])

fig, ax = plt.subplots(figsize=(10, 8))

sns.heatmap(gap_pivot, annot=True, fmt='.1f', cmap='RdYlGn_r', 
            center=TARGET_GAP, cbar_kws={'label': 'Price Gap (%)'}, ax=ax)

ax.set_title('Price Gap by Division and Quarter\n(Red = Higher Gap, Green = Closer to Target)', fontweight='bold')
ax.set_xlabel('Quarter')
ax.set_ylabel('Division')

plt.tight_layout()
plt.show()

# =============================================================================
# IDENTIFY OUTLIERS
# =============================================================================

# Very large gaps (>40%)
large_gaps = df_valid[df_valid['price_gap_pct'] > 40].copy()

# Very small gaps (<10%)
small_gaps = df_valid[df_valid['price_gap_pct'] < 10].copy()

# Negative gaps (BC more expensive than National!)
negative_gaps = df_valid[df_valid['price_gap_pct'] < 0].copy()

print("="*60)
print("OUTLIER SUMMARY")
print("="*60)
print(f"\nLarge gaps (>40%): {len(large_gaps):,} observations ({len(large_gaps)/len(df_valid)*100:.1f}%)")
print(f"Small gaps (<10%): {len(small_gaps):,} observations ({len(small_gaps)/len(df_valid)*100:.1f}%)")
print(f"Negative gaps (BC > National): {len(negative_gaps):,} observations ({len(negative_gaps)/len(df_valid)*100:.1f}%)")

# =============================================================================
# SAMPLE LARGE GAP ITEMS
# =============================================================================

if len(large_gaps) > 0:
    print("\nSample Items with Large Price Gaps (>40%):")
    print("-" * 80)
    
    large_gap_sample = large_gaps.groupby('item_code').agg({
        'item_name': 'first',
        'category': 'first',
        'bsp': 'mean',
        'national_bsp': 'mean',
        'price_gap_pct': 'mean'
    }).sort_values('price_gap_pct', ascending=False).head(15)
    
    large_gap_sample.columns = ['Item Name', 'Category', 'BC BSP', 'National BSP', 'Gap %']
    display(large_gap_sample)

# =============================================================================
# SAMPLE SMALL/NEGATIVE GAP ITEMS
# =============================================================================

if len(small_gaps) > 0:
    print("\nSample Items with Small Price Gaps (<10%):")
    print("-" * 80)
    
    small_gap_sample = small_gaps.groupby('item_code').agg({
        'item_name': 'first',
        'category': 'first',
        'bsp': 'mean',
        'national_bsp': 'mean',
        'price_gap_pct': 'mean'
    }).sort_values('price_gap_pct', ascending=True).head(15)
    
    small_gap_sample.columns = ['Item Name', 'Category', 'BC BSP', 'National BSP', 'Gap %']
    display(small_gap_sample)

# =============================================================================
# CATEGORIES WITH MOST OUTLIERS
# =============================================================================

print("\nCategories with Most Large Gap Items (>40%):")
if len(large_gaps) > 0:
    large_gap_categories = large_gaps.groupby('category')['item_code'].nunique().sort_values(ascending=False).head(10)
    print(large_gap_categories.to_string())

print("\nCategories with Most Small Gap Items (<10%):")
if len(small_gaps) > 0:
    small_gap_categories = small_gaps.groupby('category')['item_code'].nunique().sort_values(ascending=False).head(10)
    print(small_gap_categories.to_string())

# =============================================================================
# EXECUTIVE SUMMARY
# =============================================================================

print("="*70)
print("RQ1: PRICE GAP ANALYSIS - EXECUTIVE SUMMARY")
print("="*70)

print("\n1. OVERALL PRICE GAP")
print(f"   - Average gap: {df_valid['price_gap_pct'].mean():.1f}%")
print(f"   - Median gap: {df_valid['price_gap_pct'].median():.1f}%")
print(f"   - Target gap: {TARGET_GAP}%")
print(f"   - Status: {'ABOVE' if df_valid['price_gap_pct'].mean() > TARGET_GAP else 'BELOW'} TARGET by {abs(df_valid['price_gap_pct'].mean() - TARGET_GAP):.1f}% points")

print("\n2. CATEGORY VARIATION")
print(f"   - Categories analyzed: {len(category_gaps_filtered)}")
print(f"   - Highest gap category: {category_gaps_filtered.index[0]} ({category_gaps_filtered['avg_gap'].iloc[0]:.1f}%)")
print(f"   - Lowest gap category: {category_gaps_filtered.index[-1]} ({category_gaps_filtered['avg_gap'].iloc[-1]:.1f}%)")

print("\n3. GEOGRAPHIC VARIATION")
print(f"   - Highest gap division: {division_gaps.index[0]} ({division_gaps['avg_gap'].iloc[0]:.1f}%)")
print(f"   - Lowest gap division: {division_gaps.index[-1]} ({division_gaps['avg_gap'].iloc[-1]:.1f}%)")
print(f"   - Division range: {division_gaps['avg_gap'].max() - division_gaps['avg_gap'].min():.1f}% points")

print("\n4. OUTLIERS")
print(f"   - Items with gap >40%: {len(large_gaps):,} observations")
print(f"   - Items with gap <10%: {len(small_gaps):,} observations")
print(f"   - Items with negative gap: {len(negative_gaps):,} observations")

print("\n5. RECOMMENDATIONS")
print("   - Review categories with gaps significantly above 40%")
print("   - Investigate items with negative gaps (BC priced above National)")
print("   - Consider division-specific pricing strategies")
print("   - Monitor quarterly trends for pricing alignment")
