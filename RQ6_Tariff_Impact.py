# =============================================================================
# IMPORTS
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from IPython.display import display, Markdown
import warnings

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', '{:,.2f}'.format)

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = [12, 6]

# Tariff-sensitive category patterns
TARIFF_PATTERNS = {
    'Coffee & Creamers': ['COFFEE', 'CREAMER'],
    'Oils/Shortenings': ['OIL', 'SHORTENING', 'VEGETABLE OIL'],
    'Chocolate/Baking': ['CHOCOLATE', 'COCOA', 'BAKING']
}

print("Setup complete!")

# =============================================================================
# LOAD PREPARED DATA
# =============================================================================

DATA_DIR = r'C:\Users\ashishk\Dropbox\My PC (BUS-P10E67720)\Documents\Development\AWG_Spring_26\prepared_data_normalized'

# Load price changes dataset
df = pd.read_csv(f'{DATA_DIR}/price_changes.csv')

# Load product master
df_products = pd.read_csv(f'{DATA_DIR}/product_master.csv')

print(f"Price changes data: {len(df):,} rows")
print(f"Periods: {df['period'].value_counts().to_dict()}")

# =============================================================================
# FLAG TARIFF-SENSITIVE CATEGORIES
# =============================================================================

def is_tariff_sensitive(category):
    if pd.isna(category):
        return False
    category_upper = category.upper()
    for group, patterns in TARIFF_PATTERNS.items():
        if any(p in category_upper for p in patterns):
            return True
    return False

def get_tariff_group(category):
    if pd.isna(category):
        return 'Other'
    category_upper = category.upper()
    for group, patterns in TARIFF_PATTERNS.items():
        if any(p in category_upper for p in patterns):
            return group
    return 'Other'

df['tariff_sensitive'] = df['category'].apply(is_tariff_sensitive)
df['tariff_group'] = df['category'].apply(get_tariff_group)

print(f"Tariff-sensitive observations: {df['tariff_sensitive'].sum():,} ({df['tariff_sensitive'].mean()*100:.1f}%)")
print(f"\nBy tariff group:")
print(df['tariff_group'].value_counts())

# =============================================================================
# PRICE CHANGE SUMMARY BY PERIOD
# =============================================================================

# Filter to valid changes
df_valid = df[df['list_cost_change_pct'].notna() | df['bsp_change_pct'].notna()].copy()

# Summary by period
period_summary = df_valid.groupby('period').agg({
    'list_cost_change_pct': ['mean', 'median', 'std'],
    'bsp_change_pct': ['mean', 'median', 'std'],
    'item_code': 'count'
}).round(2)

period_summary.columns = ['LC Mean', 'LC Median', 'LC Std', 'BSP Mean', 'BSP Median', 'BSP Std', 'Observations']

print("Price Change Summary by Period (%)")
display(period_summary)

# =============================================================================
# ITEMS WITH PRICE CHANGES BY PERIOD
# =============================================================================

# Count items with non-zero changes
change_counts = []

for period in ['Q1→Q2', 'Q2→Q3', 'Q3→Q4']:
    period_df = df_valid[df_valid['period'] == period]
    
    lc_changes = (period_df['list_cost_change'].notna() & (period_df['list_cost_change'] != 0)).sum()
    bsp_changes = (period_df['bsp_change'].notna() & (period_df['bsp_change'] != 0)).sum()
    
    change_counts.append({
        'Period': period,
        'Items with LC Change': lc_changes,
        '% LC Changed': lc_changes / len(period_df) * 100 if len(period_df) > 0 else 0,
        'Items with BSP Change': bsp_changes,
        '% BSP Changed': bsp_changes / len(period_df) * 100 if len(period_df) > 0 else 0
    })

df_change_counts = pd.DataFrame(change_counts).round(1)
print("Items with Price Changes by Period:")
display(df_change_counts)

# =============================================================================
# PRICE CHANGE DISTRIBUTION BY PERIOD
# =============================================================================

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

periods = ['Q1→Q2', 'Q2→Q3', 'Q3→Q4']

for i, period in enumerate(periods):
    period_df = df_valid[(df_valid['period'] == period) & (df_valid['list_cost_change_pct'].notna())]
    
    # Filter to reasonable range
    changes = period_df['list_cost_change_pct'][period_df['list_cost_change_pct'].between(-50, 50)]
    
    axes[i].hist(changes, bins=40, edgecolor='black', alpha=0.7, color='steelblue')
    axes[i].axvline(x=0, color='red', linestyle='--', linewidth=2)
    axes[i].axvline(x=changes.median(), color='green', linestyle='--', linewidth=2,
                    label=f'Median: {changes.median():.1f}%')
    axes[i].set_xlabel('List Cost Change (%)')
    axes[i].set_ylabel('Frequency')
    axes[i].set_title(f'{period}', fontweight='bold')
    axes[i].legend()

plt.suptitle('List Cost Change Distribution by Period', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# =============================================================================
# CATEGORY-LEVEL PRICE CHANGES
# =============================================================================

category_changes = df_valid.groupby('category').agg({
    'list_cost_change_pct': ['mean', 'median', 'count'],
    'bsp_change_pct': ['mean', 'median']
}).round(2)

category_changes.columns = ['LC_Mean', 'LC_Median', 'Observations', 'BSP_Mean', 'BSP_Median']

# Filter to categories with sufficient data
category_changes_filtered = category_changes[category_changes['Observations'] >= 20]

# Sort by mean list cost change (potential tariff impact)
category_changes_sorted = category_changes_filtered.sort_values('LC_Mean', ascending=False)

print("Top 20 Categories by Average List Cost Increase:")
display(category_changes_sorted.head(20))

# =============================================================================
# VISUALIZATION: TOP INCREASING CATEGORIES
# =============================================================================

top_cats = category_changes_sorted.head(20)

fig, ax = plt.subplots(figsize=(12, 8))

# Color by tariff sensitivity
colors = ['red' if is_tariff_sensitive(cat) else 'steelblue' for cat in top_cats.index]

bars = ax.barh(range(len(top_cats)), top_cats['LC_Mean'], color=colors, edgecolor='black')
ax.axvline(x=0, color='black', linestyle='-', linewidth=1)

ax.set_yticks(range(len(top_cats)))
ax.set_yticklabels(top_cats.index)
ax.set_xlabel('Average List Cost Change (%)')
ax.set_title('Categories with Largest Cost Increases\n(Red = Tariff-Sensitive)', fontweight='bold')

plt.tight_layout()
plt.show()

# =============================================================================
# WHICH QUARTER HAD MOST CHANGES?
# =============================================================================

print("="*60)
print("TIMING ANALYSIS: When Did Price Changes Occur?")
print("="*60)

# Large increases (>5%)
df_valid['large_increase'] = df_valid['list_cost_change_pct'] > 5
df_valid['large_decrease'] = df_valid['list_cost_change_pct'] < -5

timing_summary = df_valid.groupby('period').agg({
    'large_increase': 'sum',
    'large_decrease': 'sum',
    'item_code': 'count'
})

timing_summary['% Large Increases'] = (timing_summary['large_increase'] / timing_summary['item_code'] * 100).round(1)
timing_summary['% Large Decreases'] = (timing_summary['large_decrease'] / timing_summary['item_code'] * 100).round(1)

print("\nLarge Price Changes by Period:")
display(timing_summary[['large_increase', '% Large Increases', 'large_decrease', '% Large Decreases']])

# =============================================================================
# TIMING VISUALIZATION
# =============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

periods = ['Q1→Q2', 'Q2→Q3', 'Q3→Q4']
x = np.arange(len(periods))
width = 0.35

increases = [timing_summary.loc[p, '% Large Increases'] for p in periods]
decreases = [timing_summary.loc[p, '% Large Decreases'] for p in periods]

ax.bar(x - width/2, increases, width, label='Large Increases (>5%)', color='red', edgecolor='black')
ax.bar(x + width/2, decreases, width, label='Large Decreases (<-5%)', color='green', edgecolor='black')

ax.set_xlabel('Period')
ax.set_ylabel('% of Items')
ax.set_title('Large Price Changes by Period', fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(periods)
ax.legend()

plt.tight_layout()
plt.show()

# =============================================================================
# TARIFF-SENSITIVE VS OTHER CATEGORIES
# =============================================================================

print("="*60)
print("TARIFF-SENSITIVE VS OTHER CATEGORIES")
print("="*60)

tariff_comparison = df_valid.groupby('tariff_sensitive').agg({
    'list_cost_change_pct': ['mean', 'median', 'std'],
    'bsp_change_pct': ['mean', 'median'],
    'item_code': 'count'
}).round(2)

tariff_comparison.columns = ['LC_Mean', 'LC_Median', 'LC_Std', 'BSP_Mean', 'BSP_Median', 'Observations']
tariff_comparison.index = ['Other Categories', 'Tariff-Sensitive']

display(tariff_comparison)

# =============================================================================
# DEEP DIVE BY TARIFF GROUP
# =============================================================================

tariff_group_detail = df_valid.groupby(['tariff_group', 'period']).agg({
    'list_cost_change_pct': ['mean', 'median'],
    'item_code': 'count'
}).round(2)

tariff_group_detail.columns = ['LC_Mean', 'LC_Median', 'Observations']
tariff_group_detail = tariff_group_detail.reset_index()

# Pivot for display
pivot_display = tariff_group_detail.pivot(index='tariff_group', columns='period', values='LC_Mean')

print("\nAverage List Cost Change by Tariff Group and Period:")
display(pivot_display)

# =============================================================================
# TARIFF GROUP VISUALIZATION
# =============================================================================

fig, ax = plt.subplots(figsize=(12, 6))

# Reorder for plotting
groups = ['Coffee & Creamers', 'Oils/Shortenings', 'Chocolate/Baking', 'Other']
periods = ['Q1→Q2', 'Q2→Q3', 'Q3→Q4']

x = np.arange(len(groups))
width = 0.25

for i, period in enumerate(periods):
    values = [pivot_display.loc[g, period] if g in pivot_display.index and period in pivot_display.columns else 0 
              for g in groups]
    ax.bar(x + i*width, values, width, label=period)

ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax.set_xlabel('Category Group')
ax.set_ylabel('Average List Cost Change (%)')
ax.set_title('Price Changes in Tariff-Sensitive Categories by Period', fontweight='bold')
ax.set_xticks(x + width)
ax.set_xticklabels(groups, rotation=15)
ax.legend()

plt.tight_layout()
plt.show()

# =============================================================================
# CALCULATE ANOMALY SCORES
# =============================================================================

# Calculate z-score for each category's price change
overall_mean = df_valid['list_cost_change_pct'].mean()
overall_std = df_valid['list_cost_change_pct'].std()

category_anomaly = category_changes_filtered.copy()
category_anomaly['z_score'] = (category_anomaly['LC_Mean'] - overall_mean) / overall_std
category_anomaly['anomaly_flag'] = abs(category_anomaly['z_score']) > 2

# Sort by z-score
category_anomaly_sorted = category_anomaly.sort_values('z_score', ascending=False)

print("Categories with Anomalous Price Changes (|Z| > 2):")
anomalies = category_anomaly_sorted[category_anomaly_sorted['anomaly_flag']]
display(anomalies[['LC_Mean', 'LC_Median', 'Observations', 'z_score']])

# =============================================================================
# ANOMALY VISUALIZATION
# =============================================================================

fig, ax = plt.subplots(figsize=(12, 6))

# Scatter plot of z-scores
colors = ['red' if a else 'steelblue' for a in category_anomaly_sorted['anomaly_flag']]
sizes = [100 if a else 30 for a in category_anomaly_sorted['anomaly_flag']]

ax.scatter(range(len(category_anomaly_sorted)), category_anomaly_sorted['z_score'], 
           c=colors, s=sizes, alpha=0.6)

ax.axhline(y=2, color='red', linestyle='--', linewidth=1, label='Anomaly Threshold (+2)')
ax.axhline(y=-2, color='red', linestyle='--', linewidth=1, label='Anomaly Threshold (-2)')
ax.axhline(y=0, color='gray', linestyle='-', linewidth=1)

ax.set_xlabel('Category (ranked by z-score)')
ax.set_ylabel('Z-Score of Price Change')
ax.set_title('Category Price Change Anomaly Detection\n(Red = Anomalous)', fontweight='bold')
ax.legend()

plt.tight_layout()
plt.show()

print(f"\nTotal anomalous categories: {category_anomaly_sorted['anomaly_flag'].sum()}")

# =============================================================================
# COST VS RETAIL COMPARISON
# =============================================================================

print("="*60)
print("COST vs RETAIL PRICE CHANGES")
print("="*60)

# For tariff-sensitive categories, compare cost changes to retail changes
df_tariff = df_valid[df_valid['tariff_sensitive']].copy()

print(f"\nTariff-sensitive items: {len(df_tariff):,}")

print(f"\nCost Change Statistics:")
print(f"  Mean: {df_tariff['list_cost_change_pct'].mean():.2f}%")
print(f"  Median: {df_tariff['list_cost_change_pct'].median():.2f}%")

print(f"\nBSP Change Statistics:")
print(f"  Mean: {df_tariff['bsp_change_pct'].mean():.2f}%")
print(f"  Median: {df_tariff['bsp_change_pct'].median():.2f}%")

# Pass-through comparison
if 'pass_through_rate' in df_tariff.columns:
    print(f"\nPass-Through Rate:")
    print(f"  Mean: {df_tariff['pass_through_rate'].mean():.2f}")
    print(f"  Median: {df_tariff['pass_through_rate'].median():.2f}")

# =============================================================================
# COST VS BSP CHANGE SCATTER
# =============================================================================

fig, ax = plt.subplots(figsize=(10, 8))

# Sample for visualization
sample = df_tariff[df_tariff['list_cost_change_pct'].between(-30, 30) & 
                   df_tariff['bsp_change_pct'].between(-30, 30)].sample(min(2000, len(df_tariff)))

ax.scatter(sample['list_cost_change_pct'], sample['bsp_change_pct'], alpha=0.4, s=20)

# Add 45-degree line (100% pass-through)
ax.plot([-30, 30], [-30, 30], 'r--', linewidth=2, label='100% Pass-Through')

ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.5)

ax.set_xlabel('List Cost Change (%)')
ax.set_ylabel('BSP Change (%)')
ax.set_title('Cost Change vs BSP Change (Tariff-Sensitive Categories)', fontweight='bold')
ax.legend()
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)

plt.tight_layout()
plt.show()

# =============================================================================
# EXECUTIVE SUMMARY
# =============================================================================

print("="*70)
print("RQ6: TARIFF IMPACT DETECTION - EXECUTIVE SUMMARY")
print("="*70)

print("\n1. OVERALL PRICE CHANGES")
print(f"   - Average List Cost change: {df_valid['list_cost_change_pct'].mean():.2f}%")
print(f"   - Average BSP change: {df_valid['bsp_change_pct'].mean():.2f}%")

print("\n2. TIMING ANALYSIS")
max_period = timing_summary['% Large Increases'].idxmax()
print(f"   - Period with most large increases: {max_period}")
print(f"   - % of items with >5% increase: {timing_summary.loc[max_period, '% Large Increases']:.1f}%")

print("\n3. TARIFF-SENSITIVE CATEGORIES")
if len(df_tariff) > 0:
    print(f"   - Avg cost change: {df_tariff['list_cost_change_pct'].mean():.2f}%")
    print(f"   - vs Other categories: {df_valid[~df_valid['tariff_sensitive']]['list_cost_change_pct'].mean():.2f}%")

print("\n4. ANOMALOUS CATEGORIES")
print(f"   - Categories with unusual changes: {category_anomaly_sorted['anomaly_flag'].sum()}")
if len(anomalies) > 0:
    print(f"   - Top anomaly: {anomalies.index[0]} (z={anomalies['z_score'].iloc[0]:.2f})")

print("\n5. RECOMMENDATIONS")
print("   - Monitor tariff-sensitive categories for continued cost pressure")
print("   - Investigate anomalous categories for tariff impact")
print("   - Review pass-through strategy for cost increases")
print("   - Consider timing of price adjustments")
