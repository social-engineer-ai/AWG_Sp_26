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

# Display settings
pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', '{:,.2f}'.format)

# Plot settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['font.size'] = 11

print("Setup complete!")

# =============================================================================
# LOAD PREPARED DATA
# =============================================================================

DATA_DIR = r'C:\Users\ashishk\Dropbox\My PC (BUS-P10E67720)\Documents\Development\AWG_Spring_26\prepared_data_normalized'

# Load price changes dataset (primary for this analysis)
df = pd.read_csv(f'{DATA_DIR}/price_changes.csv')

# Load product master for reference
df_products = pd.read_csv(f'{DATA_DIR}/product_master.csv')

print(f"Price changes data: {len(df):,} rows")
print(f"Product master: {len(df_products):,} products")

# =============================================================================
# DATA OVERVIEW
# =============================================================================

print("Columns available:")
print([col for col in df.columns if 'change' in col.lower() or 'pass' in col.lower()])

print("\nData preview:")
df.head()

# =============================================================================
# FILTER TO ITEMS WITH COST CHANGES
# =============================================================================

# Filter to rows with non-zero list cost changes
df_cost_changes = df[
    (df['list_cost_change'].notna()) & 
    (df['list_cost_change'] != 0) &
    (df['bsp_change'].notna())
].copy()

print(f"Rows with cost changes: {len(df_cost_changes):,}")
print(f"Unique items with cost changes: {df_cost_changes['item_code'].nunique():,}")
print(f"\nPeriods: {df_cost_changes['period'].value_counts().to_dict()}")

# =============================================================================
# PASS-THROUGH RATE STATISTICS
# =============================================================================

# Filter to reasonable pass-through rates (avoid extreme outliers)
df_valid_pt = df_cost_changes[
    (df_cost_changes['pass_through_rate'].notna()) &
    (df_cost_changes['pass_through_rate'].between(-5, 5))  # Reasonable range
].copy()

print("="*60)
print("PASS-THROUGH RATE SUMMARY")
print("="*60)

pt_stats = df_valid_pt['pass_through_rate'].describe(percentiles=[.10, .25, .50, .75, .90])
print(f"\nPass-Through Rate Statistics:")
print(pt_stats.round(3))

print(f"\n--- Key Findings ---")
print(f"Mean pass-through rate: {df_valid_pt['pass_through_rate'].mean():.2f}")
print(f"Median pass-through rate: {df_valid_pt['pass_through_rate'].median():.2f}")
print(f"\nInterpretation:")
print(f"  - A rate of 1.0 means 100% of cost changes are passed to BSP")
print(f"  - A rate > 1.0 means BSP increases MORE than cost increases")
print(f"  - A rate < 1.0 means BSP absorbs some of the cost change")

# =============================================================================
# PASS-THROUGH RATE DISTRIBUTION
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(df_valid_pt['pass_through_rate'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].axvline(x=1.0, color='red', linestyle='--', linewidth=2, label='100% Pass-Through')
axes[0].axvline(x=df_valid_pt['pass_through_rate'].mean(), color='green', linestyle='--', linewidth=2,
                label=f'Mean ({df_valid_pt["pass_through_rate"].mean():.2f})')
axes[0].set_xlabel('Pass-Through Rate')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Cost Pass-Through Rates', fontweight='bold')
axes[0].legend()

# Box plot
axes[1].boxplot(df_valid_pt['pass_through_rate'].dropna(), vert=True)
axes[1].axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='100% Pass-Through')
axes[1].set_ylabel('Pass-Through Rate')
axes[1].set_title('Pass-Through Rate Box Plot', fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.show()

# =============================================================================
# PASS-THROUGH CATEGORIES
# =============================================================================

def categorize_passthrough(rate):
    if rate < 0:
        return 'Negative (Price moved opposite)'
    elif rate < 0.5:
        return 'Low (<50%)'
    elif rate < 0.9:
        return 'Partial (50-90%)'
    elif rate <= 1.1:
        return 'Full (90-110%)'
    else:
        return 'Amplified (>110%)'

df_valid_pt['pt_category'] = df_valid_pt['pass_through_rate'].apply(categorize_passthrough)

# Summary by category
pt_category_summary = df_valid_pt['pt_category'].value_counts()
pt_category_pct = (pt_category_summary / len(df_valid_pt) * 100).round(1)

print("\nPass-Through Rate Distribution by Category:")
print("-" * 50)
for cat in ['Negative (Price moved opposite)', 'Low (<50%)', 'Partial (50-90%)', 'Full (90-110%)', 'Amplified (>110%)']:
    if cat in pt_category_summary:
        count = pt_category_summary[cat]
        pct = pt_category_pct[cat]
        print(f"  {cat}: {count:,} ({pct}%)")

# =============================================================================
# PASS-THROUGH BY BRAND
# =============================================================================

brand_pt = df_valid_pt.groupby('brand').agg({
    'pass_through_rate': ['mean', 'median', 'std', 'count'],
    'list_cost_change_pct': 'mean',
    'bsp_change_pct': 'mean'
}).round(3)

brand_pt.columns = ['avg_pt_rate', 'median_pt_rate', 'std_pt_rate', 'observations', 
                    'avg_cost_change_pct', 'avg_bsp_change_pct']

print("Pass-Through Rate by Brand:")
display(brand_pt)

# =============================================================================
# VISUALIZATION BY BRAND
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart of average pass-through
colors = ['#2ecc71', '#3498db', '#e74c3c']
brands = brand_pt.index.tolist()
axes[0].bar(brands, brand_pt['avg_pt_rate'], color=colors[:len(brands)], edgecolor='black')
axes[0].axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='100% Pass-Through')
axes[0].set_xlabel('Brand')
axes[0].set_ylabel('Average Pass-Through Rate')
axes[0].set_title('Average Pass-Through Rate by Brand', fontweight='bold')
axes[0].legend()

# Box plot by brand
df_valid_pt.boxplot(column='pass_through_rate', by='brand', ax=axes[1])
axes[1].axhline(y=1.0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Brand')
axes[1].set_ylabel('Pass-Through Rate')
axes[1].set_title('Pass-Through Distribution by Brand', fontweight='bold')
plt.suptitle('')

plt.tight_layout()
plt.show()

# =============================================================================
# PASS-THROUGH BY CATEGORY
# =============================================================================

category_pt = df_valid_pt.groupby('category').agg({
    'pass_through_rate': ['mean', 'median', 'count'],
    'list_cost_change_pct': 'mean',
    'bsp_change_pct': 'mean'
}).round(3)

category_pt.columns = ['avg_pt_rate', 'median_pt_rate', 'observations', 
                       'avg_cost_change_pct', 'avg_bsp_change_pct']

# Filter to categories with sufficient data
category_pt_filtered = category_pt[category_pt['observations'] >= 10].sort_values('avg_pt_rate', ascending=False)

print(f"Categories with 10+ observations: {len(category_pt_filtered)}")
print("\nTop 15 Categories by Pass-Through Rate:")
display(category_pt_filtered.head(15))

# =============================================================================
# CATEGORY PASS-THROUGH VISUALIZATION
# =============================================================================

top_cats = category_pt_filtered.head(20)

fig, ax = plt.subplots(figsize=(12, 8))

colors = ['green' if 0.9 <= x <= 1.1 else 'orange' if x < 0.9 else 'red' for x in top_cats['avg_pt_rate']]

bars = ax.barh(range(len(top_cats)), top_cats['avg_pt_rate'], color=colors, edgecolor='black')
ax.axvline(x=1.0, color='red', linestyle='--', linewidth=2, label='100% Pass-Through')

ax.set_yticks(range(len(top_cats)))
ax.set_yticklabels(top_cats.index)
ax.set_xlabel('Average Pass-Through Rate')
ax.set_title('Pass-Through Rate by Category (Top 20)', fontweight='bold')
ax.legend()

plt.tight_layout()
plt.show()

# =============================================================================
# PASS-THROUGH BY PERIOD
# =============================================================================

period_pt = df_valid_pt.groupby('period').agg({
    'pass_through_rate': ['mean', 'median', 'std', 'count'],
    'list_cost_change_pct': 'mean',
    'bsp_change_pct': 'mean'
}).round(3)

period_pt.columns = ['avg_pt_rate', 'median_pt_rate', 'std_pt_rate', 'observations',
                     'avg_cost_change_pct', 'avg_bsp_change_pct']

print("Pass-Through Rate by Period:")
display(period_pt)

# =============================================================================
# PERIOD VISUALIZATION
# =============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

periods = ['Q1→Q2', 'Q2→Q3', 'Q3→Q4']
period_pt_ordered = period_pt.reindex(periods)

ax.bar(periods, period_pt_ordered['avg_pt_rate'], color='steelblue', edgecolor='black')
ax.axhline(y=1.0, color='red', linestyle='--', linewidth=2, label='100% Pass-Through')

ax.set_xlabel('Period')
ax.set_ylabel('Average Pass-Through Rate')
ax.set_title('Pass-Through Rate by Quarter Transition', fontweight='bold')
ax.legend()

# Add value labels
for i, v in enumerate(period_pt_ordered['avg_pt_rate']):
    ax.text(i, v + 0.02, f'{v:.2f}', ha='center', fontsize=11)

plt.tight_layout()
plt.show()

# =============================================================================
# ASYMMETRIC PASS-THROUGH ANALYSIS
# =============================================================================

# Split into cost increases and decreases
df_cost_increase = df_valid_pt[df_valid_pt['list_cost_change'] > 0].copy()
df_cost_decrease = df_valid_pt[df_valid_pt['list_cost_change'] < 0].copy()

print("="*60)
print("ASYMMETRIC PASS-THROUGH ANALYSIS")
print("="*60)

print(f"\nCost INCREASES:")
print(f"  Observations: {len(df_cost_increase):,}")
print(f"  Avg cost change: {df_cost_increase['list_cost_change_pct'].mean():.1f}%")
print(f"  Avg BSP change: {df_cost_increase['bsp_change_pct'].mean():.1f}%")
print(f"  Avg pass-through rate: {df_cost_increase['pass_through_rate'].mean():.2f}")

print(f"\nCost DECREASES:")
print(f"  Observations: {len(df_cost_decrease):,}")
print(f"  Avg cost change: {df_cost_decrease['list_cost_change_pct'].mean():.1f}%")
print(f"  Avg BSP change: {df_cost_decrease['bsp_change_pct'].mean():.1f}%")
print(f"  Avg pass-through rate: {df_cost_decrease['pass_through_rate'].mean():.2f}")

# =============================================================================
# ASYMMETRY VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Bar comparison
categories = ['Cost Increases', 'Cost Decreases']
pt_rates = [df_cost_increase['pass_through_rate'].mean(), df_cost_decrease['pass_through_rate'].mean()]

colors = ['#e74c3c', '#2ecc71']
axes[0].bar(categories, pt_rates, color=colors, edgecolor='black')
axes[0].axhline(y=1.0, color='black', linestyle='--', linewidth=2, label='100% Pass-Through')
axes[0].set_ylabel('Average Pass-Through Rate')
axes[0].set_title('Pass-Through Rate: Increases vs Decreases', fontweight='bold')
axes[0].legend()

# Add value labels
for i, v in enumerate(pt_rates):
    axes[0].text(i, v + 0.02, f'{v:.2f}', ha='center', fontsize=12, fontweight='bold')

# Box plot comparison
data_to_plot = [df_cost_increase['pass_through_rate'].dropna(), df_cost_decrease['pass_through_rate'].dropna()]
bp = axes[1].boxplot(data_to_plot, labels=categories, patch_artist=True)
bp['boxes'][0].set_facecolor('#e74c3c')
bp['boxes'][1].set_facecolor('#2ecc71')
axes[1].axhline(y=1.0, color='black', linestyle='--', linewidth=2)
axes[1].set_ylabel('Pass-Through Rate')
axes[1].set_title('Pass-Through Distribution: Increases vs Decreases', fontweight='bold')

plt.tight_layout()
plt.show()

# Statistical test
if len(df_cost_increase) > 10 and len(df_cost_decrease) > 10:
    stat, pvalue = stats.mannwhitneyu(df_cost_increase['pass_through_rate'].dropna(), 
                                       df_cost_decrease['pass_through_rate'].dropna())
    print(f"\nMann-Whitney U test p-value: {pvalue:.4f}")
    print(f"Difference is {'statistically significant' if pvalue < 0.05 else 'not statistically significant'} at 0.05 level")

# =============================================================================
# EXECUTIVE SUMMARY
# =============================================================================

print("="*70)
print("RQ2: COST PASS-THROUGH ANALYSIS - EXECUTIVE SUMMARY")
print("="*70)

print("\n1. OVERALL PASS-THROUGH")
print(f"   - Average rate: {df_valid_pt['pass_through_rate'].mean():.2f}")
print(f"   - Median rate: {df_valid_pt['pass_through_rate'].median():.2f}")
print(f"   - Interpretation: {'Full pass-through' if 0.9 <= df_valid_pt['pass_through_rate'].mean() <= 1.1 else 'Partial pass-through' if df_valid_pt['pass_through_rate'].mean() < 0.9 else 'Amplified pass-through'}")

print("\n2. BRAND DIFFERENCES")
for brand in brand_pt.index:
    print(f"   - {brand}: {brand_pt.loc[brand, 'avg_pt_rate']:.2f}")

print("\n3. ASYMMETRY")
print(f"   - Cost increases pass-through: {df_cost_increase['pass_through_rate'].mean():.2f}")
print(f"   - Cost decreases pass-through: {df_cost_decrease['pass_through_rate'].mean():.2f}")
asymmetry = df_cost_increase['pass_through_rate'].mean() - df_cost_decrease['pass_through_rate'].mean()
print(f"   - Asymmetry: {asymmetry:+.2f}")

print("\n4. RECOMMENDATIONS")
print("   - Monitor categories with low pass-through rates")
print("   - Investigate asymmetric behavior if significant")
print("   - Consider brand-specific pricing strategies")
