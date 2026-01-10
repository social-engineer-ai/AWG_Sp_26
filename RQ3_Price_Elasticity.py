# =============================================================================
# IMPORTS
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from IPython.display import display, Markdown
import warnings

warnings.filterwarnings('ignore')

# Display settings
pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', '{:,.2f}'.format)

# Plot settings
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = [12, 6]

print("Setup complete!")

# =============================================================================
# LOAD PREPARED DATA
# =============================================================================

DATA_DIR = r'C:\Users\ashishk\Dropbox\My PC (BUS-P10E67720)\Documents\Development\AWG_Spring_26\prepared_data_normalized'

# Load price changes dataset with sales
df = pd.read_csv(f'{DATA_DIR}/price_changes.csv')

print(f"Price changes data: {len(df):,} rows")
print(f"Columns: {df.columns.tolist()}")

# =============================================================================
# PREPARE ELASTICITY DATA
# =============================================================================

# Filter to rows with both price and sales changes
df_elast = df[
    (df['bsp_change_pct'].notna()) & 
    (df['bsp_change_pct'] != 0) &
    (df['sales_dollars_change_pct'].notna()) &
    (df['bsp_prev'] > 0) &
    (df['sales_dollars_prev'] > 0)
].copy()

# Calculate price elasticity
df_elast['elasticity'] = df_elast['sales_dollars_change_pct'] / df_elast['bsp_change_pct']

# Filter extreme outliers
df_elast = df_elast[df_elast['elasticity'].between(-20, 20)]

print(f"Rows for elasticity analysis: {len(df_elast):,}")
print(f"Unique items: {df_elast['item_code'].nunique():,}")

# =============================================================================
# ELASTICITY SUMMARY STATISTICS
# =============================================================================

print("="*60)
print("PRICE ELASTICITY SUMMARY")
print("="*60)

elast_stats = df_elast['elasticity'].describe(percentiles=[.10, .25, .50, .75, .90])
print(f"\nElasticity Statistics:")
print(elast_stats.round(3))

print(f"\n--- Interpretation ---")
mean_elast = df_elast['elasticity'].mean()
median_elast = df_elast['elasticity'].median()
print(f"Mean elasticity: {mean_elast:.2f}")
print(f"Median elasticity: {median_elast:.2f}")

if median_elast < -1:
    print("Overall demand is ELASTIC - sales are highly responsive to price changes")
elif median_elast < 0:
    print("Overall demand is INELASTIC - sales are not very responsive to price changes")
else:
    print("Unusual positive elasticity - requires investigation")

# =============================================================================
# ELASTICITY DISTRIBUTION
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
axes[0].hist(df_elast['elasticity'], bins=50, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].axvline(x=-1, color='red', linestyle='--', linewidth=2, label='Unit Elastic (-1)')
axes[0].axvline(x=0, color='green', linestyle='--', linewidth=2, label='Zero')
axes[0].axvline(x=median_elast, color='orange', linestyle='--', linewidth=2, 
                label=f'Median ({median_elast:.2f})')
axes[0].set_xlabel('Price Elasticity')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Price Elasticity', fontweight='bold')
axes[0].legend()

# Box plot
axes[1].boxplot(df_elast['elasticity'].dropna(), vert=True)
axes[1].axhline(y=-1, color='red', linestyle='--', linewidth=2, label='Unit Elastic')
axes[1].axhline(y=0, color='green', linestyle='--', linewidth=2, label='Zero')
axes[1].set_ylabel('Price Elasticity')
axes[1].set_title('Elasticity Box Plot', fontweight='bold')
axes[1].legend()

plt.tight_layout()
plt.show()

# =============================================================================
# ELASTICITY CATEGORIES
# =============================================================================

def categorize_elasticity(e):
    if e < -2:
        return 'Highly Elastic (<-2)'
    elif e < -1:
        return 'Elastic (-2 to -1)'
    elif e < 0:
        return 'Inelastic (-1 to 0)'
    else:
        return 'Positive (>0)'

df_elast['elast_category'] = df_elast['elasticity'].apply(categorize_elasticity)

elast_summary = df_elast['elast_category'].value_counts()
elast_pct = (elast_summary / len(df_elast) * 100).round(1)

print("\nElasticity Distribution by Category:")
print("-" * 50)
for cat in ['Highly Elastic (<-2)', 'Elastic (-2 to -1)', 'Inelastic (-1 to 0)', 'Positive (>0)']:
    if cat in elast_summary:
        print(f"  {cat}: {elast_summary[cat]:,} ({elast_pct[cat]}%)")

# =============================================================================
# ELASTICITY BY BRAND
# =============================================================================

brand_elast = df_elast.groupby('brand').agg({
    'elasticity': ['mean', 'median', 'std', 'count']
}).round(3)

brand_elast.columns = ['mean_elasticity', 'median_elasticity', 'std_elasticity', 'observations']

print("Elasticity by Brand:")
display(brand_elast)

# =============================================================================
# BRAND ELASTICITY VISUALIZATION
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart
colors = ['#2ecc71', '#3498db', '#e74c3c']
brands = brand_elast.index.tolist()
axes[0].bar(brands, brand_elast['median_elasticity'], color=colors[:len(brands)], edgecolor='black')
axes[0].axhline(y=-1, color='red', linestyle='--', linewidth=2, label='Unit Elastic')
axes[0].axhline(y=0, color='green', linestyle='--', linewidth=2, label='Zero')
axes[0].set_xlabel('Brand')
axes[0].set_ylabel('Median Elasticity')
axes[0].set_title('Median Price Elasticity by Brand', fontweight='bold')
axes[0].legend()

# Box plot by brand
df_elast.boxplot(column='elasticity', by='brand', ax=axes[1])
axes[1].axhline(y=-1, color='red', linestyle='--', linewidth=2)
axes[1].axhline(y=0, color='green', linestyle='--', linewidth=2)
axes[1].set_xlabel('Brand')
axes[1].set_ylabel('Price Elasticity')
axes[1].set_title('Elasticity Distribution by Brand', fontweight='bold')
plt.suptitle('')

plt.tight_layout()
plt.show()

# =============================================================================
# ELASTICITY BY CATEGORY
# =============================================================================

category_elast = df_elast.groupby('category').agg({
    'elasticity': ['mean', 'median', 'count']
}).round(3)

category_elast.columns = ['mean_elasticity', 'median_elasticity', 'observations']

# Filter to categories with sufficient data
category_elast_filtered = category_elast[category_elast['observations'] >= 10]
category_elast_filtered = category_elast_filtered.sort_values('median_elasticity')

print(f"Categories with 10+ observations: {len(category_elast_filtered)}")
print("\nMost Elastic Categories (Top 15):")
display(category_elast_filtered.head(15))

# =============================================================================
# MOST ELASTIC VS INELASTIC CATEGORIES
# =============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Most elastic (negative elasticity)
most_elastic = category_elast_filtered.head(15)
axes[0].barh(range(len(most_elastic)), most_elastic['median_elasticity'], color='steelblue', edgecolor='black')
axes[0].axvline(x=-1, color='red', linestyle='--', linewidth=2)
axes[0].set_yticks(range(len(most_elastic)))
axes[0].set_yticklabels(most_elastic.index)
axes[0].set_xlabel('Median Elasticity')
axes[0].set_title('Most Elastic Categories', fontweight='bold')

# Least elastic
least_elastic = category_elast_filtered.tail(15)
axes[1].barh(range(len(least_elastic)), least_elastic['median_elasticity'], color='coral', edgecolor='black')
axes[1].axvline(x=-1, color='red', linestyle='--', linewidth=2)
axes[1].axvline(x=0, color='green', linestyle='--', linewidth=2)
axes[1].set_yticks(range(len(least_elastic)))
axes[1].set_yticklabels(least_elastic.index)
axes[1].set_xlabel('Median Elasticity')
axes[1].set_title('Least Elastic Categories', fontweight='bold')

plt.tight_layout()
plt.show()

# =============================================================================
# ELASTICITY BY PRICE CHANGE SIZE
# =============================================================================

def categorize_price_change(pct):
    abs_pct = abs(pct)
    if abs_pct < 5:
        return 'Small (<5%)'
    elif abs_pct < 10:
        return 'Medium (5-10%)'
    else:
        return 'Large (>10%)'

df_elast['price_change_size'] = df_elast['bsp_change_pct'].apply(categorize_price_change)

size_elast = df_elast.groupby('price_change_size').agg({
    'elasticity': ['mean', 'median', 'count']
}).round(3)

size_elast.columns = ['mean_elasticity', 'median_elasticity', 'observations']

print("Elasticity by Price Change Magnitude:")
display(size_elast)

# =============================================================================
# PRICE VS SALES CHANGE SCATTER
# =============================================================================

# Sample for visualization
sample = df_elast.sample(min(5000, len(df_elast)))

fig, ax = plt.subplots(figsize=(10, 8))

ax.scatter(sample['bsp_change_pct'], sample['sales_dollars_change_pct'], alpha=0.3, s=20)
ax.axhline(y=0, color='gray', linestyle='-', linewidth=1)
ax.axvline(x=0, color='gray', linestyle='-', linewidth=1)

# Add trend line
z = np.polyfit(sample['bsp_change_pct'].dropna(), sample['sales_dollars_change_pct'].dropna(), 1)
p = np.poly1d(z)
x_line = np.linspace(sample['bsp_change_pct'].min(), sample['bsp_change_pct'].max(), 100)
ax.plot(x_line, p(x_line), 'r--', linewidth=2, label=f'Trend (slope={z[0]:.2f})')

ax.set_xlabel('Price Change (%)')
ax.set_ylabel('Sales Change (%)')
ax.set_title('Price Change vs Sales Change', fontweight='bold')
ax.legend()
ax.set_xlim(-50, 50)
ax.set_ylim(-100, 100)

plt.tight_layout()
plt.show()

# =============================================================================
# SIMPLE REGRESSION: SALES CHANGE ~ PRICE CHANGE
# =============================================================================

# Prepare data
reg_data = df_elast[['bsp_change_pct', 'sales_dollars_change_pct', 'brand', 'category']].dropna()

# Simple regression
X = sm.add_constant(reg_data['bsp_change_pct'])
y = reg_data['sales_dollars_change_pct']

model = sm.OLS(y, X).fit()

print("="*60)
print("REGRESSION: Sales Change % ~ Price Change %")
print("="*60)
print(model.summary().tables[1])

# =============================================================================
# REGRESSION BY BRAND
# =============================================================================

print("\nRegression Results by Brand:")
print("-" * 60)

for brand in reg_data['brand'].unique():
    brand_data = reg_data[reg_data['brand'] == brand]
    if len(brand_data) >= 30:
        X_brand = sm.add_constant(brand_data['bsp_change_pct'])
        y_brand = brand_data['sales_dollars_change_pct']
        model_brand = sm.OLS(y_brand, X_brand).fit()
        
        print(f"\n{brand}:")
        print(f"  Elasticity coefficient: {model_brand.params['bsp_change_pct']:.3f}")
        print(f"  R-squared: {model_brand.rsquared:.3f}")
        print(f"  P-value: {model_brand.pvalues['bsp_change_pct']:.4f}")
        print(f"  Observations: {len(brand_data):,}")

# =============================================================================
# EXECUTIVE SUMMARY
# =============================================================================

print("="*70)
print("RQ3: PRICE ELASTICITY ANALYSIS - EXECUTIVE SUMMARY")
print("="*70)

print("\n1. OVERALL ELASTICITY")
print(f"   - Mean elasticity: {df_elast['elasticity'].mean():.2f}")
print(f"   - Median elasticity: {df_elast['elasticity'].median():.2f}")
print(f"   - Demand is: {'Elastic' if df_elast['elasticity'].median() < -1 else 'Inelastic'}")

print("\n2. BRAND COMPARISON")
for brand in brand_elast.index:
    elast = brand_elast.loc[brand, 'median_elasticity']
    status = 'Elastic' if elast < -1 else 'Inelastic'
    print(f"   - {brand}: {elast:.2f} ({status})")

print("\n3. CATEGORY INSIGHTS")
print(f"   - Most elastic: {category_elast_filtered.index[0]} ({category_elast_filtered['median_elasticity'].iloc[0]:.2f})")
print(f"   - Least elastic: {category_elast_filtered.index[-1]} ({category_elast_filtered['median_elasticity'].iloc[-1]:.2f})")

print("\n4. RECOMMENDATIONS")
print("   - Be cautious with price increases on elastic categories")
print("   - Inelastic categories may tolerate price adjustments better")
print("   - Consider brand-specific pricing strategies")
