# =============================================================================
# IMPORTS
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from IPython.display import display
import warnings

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', '{:,.2f}'.format)

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = [12, 6]

print("Setup complete!")

# =============================================================================
# LOAD PREPARED DATA
# =============================================================================

DATA_DIR = r'C:\Users\ashishk\Dropbox\My PC (BUS-P10E67720)\Documents\Development\AWG_Spring_26\prepared_data_normalized'

# Load category summary
df_cat = pd.read_csv(f'{DATA_DIR}/category_summary.csv')

# Load merged pricing-sales data
df_merged = pd.read_csv(f'{DATA_DIR}/pricing_sales_merged.csv')

# Load product master
df_products = pd.read_csv(f'{DATA_DIR}/product_master.csv')

print(f"Category summary: {len(df_cat):,} rows")
print(f"Merged data: {len(df_merged):,} rows")

# =============================================================================
# IDENTIFY CATEGORIES WITH BOTH BRANDS
# =============================================================================

# Find categories with both Best Choice and Always Save
category_brands = df_products.groupby('Category')['Brand Label Name'].apply(set).reset_index()
category_brands.columns = ['category', 'brands']

# Categories with both BC and AS
bc_as_categories = category_brands[
    category_brands['brands'].apply(lambda x: 'Best Choice' in x and 'Always Save' in x)
]['category'].tolist()

# Categories with all three brands
all_three_categories = category_brands[
    category_brands['brands'].apply(lambda x: 'Best Choice' in x and 'Always Save' in x and 'National Brand' in x)
]['category'].tolist()

print("="*60)
print("CATEGORY BRAND COVERAGE")
print("="*60)
print(f"\nCategories with BOTH Best Choice AND Always Save: {len(bc_as_categories)}")
print(f"Categories with ALL THREE brands: {len(all_three_categories)}")

# =============================================================================
# LIST BC-AS CATEGORIES WITH ITEM COUNTS
# =============================================================================

# Count items per brand in each BC-AS category
bc_as_detail = []

for cat in bc_as_categories:
    cat_products = df_products[df_products['Category'] == cat]
    bc_count = len(cat_products[cat_products['Brand Label Name'] == 'Best Choice'])
    as_count = len(cat_products[cat_products['Brand Label Name'] == 'Always Save'])
    
    bc_as_detail.append({
        'Category': cat,
        'BC Items': bc_count,
        'AS Items': as_count,
        'Total': bc_count + as_count
    })

df_bc_as_cats = pd.DataFrame(bc_as_detail).sort_values('Total', ascending=False)

print("\nTop 20 Categories with Both BC and AS:")
display(df_bc_as_cats.head(20))

# =============================================================================
# BC vs AS PRICE COMPARISON
# =============================================================================

# Filter to BC and AS items in shared categories
df_bc_as = df_merged[
    (df_merged['category'].isin(bc_as_categories)) &
    (df_merged['brand'].isin(['Best Choice', 'Always Save'])) &
    (df_merged['bsp'].notna())
].copy()

# Calculate average price by category, division, quarter, brand
price_comparison = df_bc_as.groupby(['category', 'division', 'quarter', 'brand']).agg({
    'bsp': 'mean',
    'sales_dollars': 'sum',
    'item_code': 'count'
}).reset_index()

price_comparison.columns = ['category', 'division', 'quarter', 'brand', 'avg_bsp', 'total_sales', 'item_count']

# Pivot to have BC and AS side by side
bc_prices = price_comparison[price_comparison['brand'] == 'Best Choice'].copy()
as_prices = price_comparison[price_comparison['brand'] == 'Always Save'].copy()

bc_prices = bc_prices.rename(columns={'avg_bsp': 'bc_bsp', 'total_sales': 'bc_sales', 'item_count': 'bc_items'})
as_prices = as_prices.rename(columns={'avg_bsp': 'as_bsp', 'total_sales': 'as_sales', 'item_count': 'as_items'})

# Merge
df_bc_as_compare = pd.merge(
    bc_prices[['category', 'division', 'quarter', 'bc_bsp', 'bc_sales', 'bc_items']],
    as_prices[['category', 'division', 'quarter', 'as_bsp', 'as_sales', 'as_items']],
    on=['category', 'division', 'quarter'],
    how='inner'
)

# Calculate BC-AS gap
df_bc_as_compare['bc_as_gap'] = df_bc_as_compare['bc_bsp'] - df_bc_as_compare['as_bsp']
df_bc_as_compare['bc_as_gap_pct'] = (df_bc_as_compare['bc_as_gap'] / df_bc_as_compare['as_bsp']) * 100

print(f"BC-AS Comparison rows: {len(df_bc_as_compare):,}")
print(f"\nBC-AS Price Gap Statistics:")
print(df_bc_as_compare['bc_as_gap_pct'].describe().round(2))

# =============================================================================
# BC-AS GAP BY CATEGORY
# =============================================================================

cat_bc_as_gap = df_bc_as_compare.groupby('category').agg({
    'bc_as_gap_pct': ['mean', 'median'],
    'bc_sales': 'sum',
    'as_sales': 'sum'
}).round(2)

cat_bc_as_gap.columns = ['avg_gap_pct', 'median_gap_pct', 'total_bc_sales', 'total_as_sales']
cat_bc_as_gap['bc_sales_share'] = (cat_bc_as_gap['total_bc_sales'] / 
                                    (cat_bc_as_gap['total_bc_sales'] + cat_bc_as_gap['total_as_sales']) * 100).round(1)
cat_bc_as_gap = cat_bc_as_gap.sort_values('avg_gap_pct', ascending=False)

print("\nBC-AS Price Gap by Category:")
display(cat_bc_as_gap.head(20))

# =============================================================================
# BC-AS GAP VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Distribution of BC-AS gap
axes[0].hist(df_bc_as_compare['bc_as_gap_pct'], bins=40, edgecolor='black', alpha=0.7)
axes[0].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Equal Price')
axes[0].axvline(x=df_bc_as_compare['bc_as_gap_pct'].median(), color='green', linestyle='--', linewidth=2,
                label=f'Median ({df_bc_as_compare["bc_as_gap_pct"].median():.1f}%)')
axes[0].set_xlabel('BC-AS Price Gap (%)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of BC vs AS Price Gap', fontweight='bold')
axes[0].legend()

# Top categories by gap
top_gap_cats = cat_bc_as_gap.head(15)
axes[1].barh(range(len(top_gap_cats)), top_gap_cats['avg_gap_pct'], color='steelblue', edgecolor='black')
axes[1].axvline(x=0, color='red', linestyle='--', linewidth=2)
axes[1].set_yticks(range(len(top_gap_cats)))
axes[1].set_yticklabels(top_gap_cats.index)
axes[1].set_xlabel('Avg BC-AS Gap (%)')
axes[1].set_title('BC-AS Price Gap by Category', fontweight='bold')

plt.tight_layout()
plt.show()

print("\nInterpretation:")
print(f"- Positive gap means Best Choice is priced HIGHER than Always Save")
print(f"- Median gap: {df_bc_as_compare['bc_as_gap_pct'].median():.1f}%")

# =============================================================================
# PREPARE DATA FOR CROSS-ELASTICITY
# =============================================================================

# Sort for lag calculation
df_bc_as_compare_sorted = df_bc_as_compare.sort_values(['category', 'division', 'quarter']).copy()

# Calculate changes
for col in ['bc_bsp', 'as_bsp', 'bc_sales', 'as_sales']:
    df_bc_as_compare_sorted[f'{col}_prev'] = df_bc_as_compare_sorted.groupby(['category', 'division'])[col].shift(1)
    df_bc_as_compare_sorted[f'{col}_change_pct'] = (
        (df_bc_as_compare_sorted[col] - df_bc_as_compare_sorted[f'{col}_prev']) / 
        df_bc_as_compare_sorted[f'{col}_prev'] * 100
    )

# Filter to valid rows
df_cross = df_bc_as_compare_sorted[
    (df_bc_as_compare_sorted['bc_bsp_change_pct'].notna()) &
    (df_bc_as_compare_sorted['as_sales_change_pct'].notna())
].copy()

print(f"Rows for cross-elasticity analysis: {len(df_cross):,}")

# =============================================================================
# CROSS-ELASTICITY CALCULATION
# =============================================================================

# Cross-elasticity: AS sales response to BC price change
df_cross_valid = df_cross[
    (df_cross['bc_bsp_change_pct'] != 0) &
    (df_cross['bc_bsp_change_pct'].between(-50, 50)) &
    (df_cross['as_sales_change_pct'].between(-100, 100))
].copy()

df_cross_valid['cross_elast_bc_to_as'] = df_cross_valid['as_sales_change_pct'] / df_cross_valid['bc_bsp_change_pct']

# Filter extreme values
df_cross_valid = df_cross_valid[df_cross_valid['cross_elast_bc_to_as'].between(-10, 10)]

print("="*60)
print("CROSS-ELASTICITY: AS Sales ~ BC Price")
print("="*60)
print(f"\nObservations: {len(df_cross_valid):,}")
print(f"Mean cross-elasticity: {df_cross_valid['cross_elast_bc_to_as'].mean():.3f}")
print(f"Median cross-elasticity: {df_cross_valid['cross_elast_bc_to_as'].median():.3f}")

print("\nInterpretation:")
if df_cross_valid['cross_elast_bc_to_as'].median() > 0:
    print("  Positive cross-elasticity suggests SUBSTITUTION")
    print("  When BC prices increase, AS sales tend to increase (customers switch)")
else:
    print("  Negative/zero cross-elasticity suggests COMPLEMENTARY or independent demand")

# =============================================================================
# CROSS-ELASTICITY VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Distribution
axes[0].hist(df_cross_valid['cross_elast_bc_to_as'], bins=40, edgecolor='black', alpha=0.7)
axes[0].axvline(x=0, color='red', linestyle='--', linewidth=2, label='No Effect')
axes[0].axvline(x=df_cross_valid['cross_elast_bc_to_as'].median(), color='green', linestyle='--', linewidth=2,
                label=f'Median ({df_cross_valid["cross_elast_bc_to_as"].median():.2f})')
axes[0].set_xlabel('Cross-Elasticity (AS Sales / BC Price)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Cross-Elasticity Distribution', fontweight='bold')
axes[0].legend()

# Scatter: BC price change vs AS sales change
axes[1].scatter(df_cross_valid['bc_bsp_change_pct'], df_cross_valid['as_sales_change_pct'], alpha=0.3, s=20)
axes[1].axhline(y=0, color='gray', linestyle='-', linewidth=1)
axes[1].axvline(x=0, color='gray', linestyle='-', linewidth=1)

# Trend line
z = np.polyfit(df_cross_valid['bc_bsp_change_pct'], df_cross_valid['as_sales_change_pct'], 1)
p = np.poly1d(z)
x_line = np.linspace(-30, 30, 100)
axes[1].plot(x_line, p(x_line), 'r--', linewidth=2, label=f'Trend (slope={z[0]:.3f})')

axes[1].set_xlabel('BC Price Change (%)')
axes[1].set_ylabel('AS Sales Change (%)')
axes[1].set_title('BC Price Change vs AS Sales Change', fontweight='bold')
axes[1].legend()
axes[1].set_xlim(-40, 40)
axes[1].set_ylim(-80, 80)

plt.tight_layout()
plt.show()

# =============================================================================
# CROSS-ELASTICITY BY CATEGORY
# =============================================================================

cat_cross_elast = df_cross_valid.groupby('category').agg({
    'cross_elast_bc_to_as': ['mean', 'median', 'count']
}).round(3)

cat_cross_elast.columns = ['mean_cross_elast', 'median_cross_elast', 'observations']

# Filter to categories with sufficient data
cat_cross_elast_filtered = cat_cross_elast[cat_cross_elast['observations'] >= 5].sort_values(
    'median_cross_elast', ascending=False
)

print("Categories with Highest Cross-Elasticity (Strong Substitution):")
display(cat_cross_elast_filtered.head(15))

print("\nCategories with Lowest/Negative Cross-Elasticity:")
display(cat_cross_elast_filtered.tail(15))

# =============================================================================
# EXECUTIVE SUMMARY
# =============================================================================

print("="*70)
print("RQ4: CROSS-BRAND EFFECTS - EXECUTIVE SUMMARY")
print("="*70)

print("\n1. CATEGORY COVERAGE")
print(f"   - Categories with both BC and AS: {len(bc_as_categories)}")
print(f"   - Categories with all three brands: {len(all_three_categories)}")

print("\n2. BC-AS PRICE POSITIONING")
print(f"   - Median BC-AS gap: {df_bc_as_compare['bc_as_gap_pct'].median():.1f}%")
print(f"   - BC is typically {'higher' if df_bc_as_compare['bc_as_gap_pct'].median() > 0 else 'lower'} priced than AS")

print("\n3. CROSS-ELASTICITY (AS Sales ~ BC Price)")
print(f"   - Mean: {df_cross_valid['cross_elast_bc_to_as'].mean():.3f}")
print(f"   - Median: {df_cross_valid['cross_elast_bc_to_as'].median():.3f}")
print(f"   - Evidence of {'substitution' if df_cross_valid['cross_elast_bc_to_as'].median() > 0 else 'no significant substitution'}")

print("\n4. RECOMMENDATIONS")
print("   - Monitor BC-AS price gaps to maintain brand positioning")
print("   - Consider cross-brand effects in pricing decisions")
print("   - Focus on high-substitution categories for coordinated pricing")
