# =============================================================================
# IMPORTS
# =============================================================================

import pandas as pd
import numpy as np
import os
import re
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

print("Libraries imported successfully!")
print(f"Pandas version: {pd.__version__}")

# =============================================================================
# CONFIGURATION
# =============================================================================

# File paths
PRICING_FILE = r'C:\Users\ashishk\Dropbox\My PC (BUS-P10E67720)\Documents\Development\AWG_Spring_26\Product Details & Pricing by quarter by division 12.19.25.xlsx'
SALES_FILE = r'C:\Users\ashishk\Dropbox\My PC (BUS-P10E67720)\Documents\Development\AWG_Spring_26\Sales Data by Quarter - U of I Project 12.19.25.xlsx'

# Output directory - NORMALIZED DATA (separate from original)
OUTPUT_DIR = r'C:\Users\ashishk\Dropbox\My PC (BUS-P10E67720)\Documents\Development\AWG_Spring_26\prepared_data_normalized'

# Create output directory if it doesn't exist
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

print(f"Output directory: {OUTPUT_DIR}")
print("  (Normalized data with unit-level prices)")

# =============================================================================
# CONSTANTS & MAPPINGS
# =============================================================================

# Division codes and full names
DIVISIONS = {
    'KC': 'Kansas City',
    'SP': 'Springfield',
    'OK': 'Oklahoma',
    'NA': 'Nashville',
    'GC': 'Gulf Coast',
    'NE': 'Nebraska',
    'GL': 'Great Lakes',
    'HN': 'Hernando',
    'UM': 'Upper Midwest'
}

# Regional groupings
DIVISION_REGIONS = {
    'KC': 'Central',
    'SP': 'Central',
    'OK': 'South',
    'NA': 'Southeast',
    'GC': 'South',
    'NE': 'North',
    'GL': 'North',
    'HN': 'Southeast',
    'UM': 'North'
}

# Sales sheet name corrections (known typos)
SHEET_NAME_CORRECTIONS = {
    'GO Division Sales': 'NA',
    'NO Division Sales': 'NE'
}

# Quarter suffixes in column names
QUARTER_SUFFIXES = {
    '': 'Q1',
    '.1': 'Q2',
    '.2': 'Q3',
    '.3': 'Q4'
}

# Product attribute columns (first 13 columns)
PRODUCT_COLUMNS = [
    'Item Code',
    'Item Unit UPC Code',
    'Case UPC Code',
    'Size',
    'Pack (Units per Case)',
    'Item Name',
    'Inventory Department',
    'Category',
    'Sub Category',
    'Brand Label Name',
    'Brand Name',
    'Item Long Description',
    'National Comparison Item Code'
]

# Tariff-sensitive categories
TARIFF_SENSITIVE_PATTERNS = ['COFFEE', 'CREAMER', 'OIL', 'SHORTENING', 'CHOCOLATE', 'COCOA', 'BAKING']

print("Constants defined!")

# =============================================================================
# LOAD PRICING DATA
# =============================================================================

print("Loading pricing data...")
df_pricing_raw = pd.read_excel(PRICING_FILE, header=3)
df_pricing_raw.columns = df_pricing_raw.columns.str.strip()

print(f"✓ Pricing data loaded: {df_pricing_raw.shape[0]:,} rows × {df_pricing_raw.shape[1]:,} columns")

# =============================================================================
# LOAD SALES DATA (ALL SHEETS)
# =============================================================================

print("Loading sales data...")

xlsx = pd.ExcelFile(SALES_FILE)
sales_sheets = {}

for sheet_name in xlsx.sheet_names:
    df = pd.read_excel(SALES_FILE, sheet_name=sheet_name, header=2)
    df.columns = df.columns.str.strip()
    
    # Correct sheet name if needed
    if sheet_name in SHEET_NAME_CORRECTIONS:
        div_code = SHEET_NAME_CORRECTIONS[sheet_name]
    else:
        div_code = sheet_name.replace(' Division Sales', '')
    
    sales_sheets[div_code] = df
    print(f"  {div_code}: {len(df):,} rows")

print(f"\n✓ Sales data loaded: {len(sales_sheets)} division sheets")

# =============================================================================
# CLEAN BRAND LABELS
# =============================================================================

print("Cleaning brand labels...")

# Strip whitespace from brand labels
df_pricing_raw['Brand Label Name'] = df_pricing_raw['Brand Label Name'].str.strip()

# Show brand distribution
print("\nBrand distribution:")
print(df_pricing_raw['Brand Label Name'].value_counts())

print("\n✓ Brand labels cleaned!")

# =============================================================================
# CREATE PRODUCT MASTER TABLE
# =============================================================================

print("Creating product master table...")

# Extract product attributes (first 13 columns)
product_cols_available = [col for col in PRODUCT_COLUMNS if col in df_pricing_raw.columns]
df_product_master = df_pricing_raw[product_cols_available].copy()

# Add tariff sensitivity flag
df_product_master['tariff_sensitive'] = df_product_master['Category'].str.upper().str.contains(
    '|'.join(TARIFF_SENSITIVE_PATTERNS), na=False
).astype(int)

# Add flag for items with national brand linkage
df_product_master['has_national_link'] = df_product_master['National Comparison Item Code'].notna().astype(int)

print(f"\n✓ Product master created: {len(df_product_master):,} products")
print(f"  - With National Brand linkage: {df_product_master['has_national_link'].sum():,}")
print(f"  - Tariff sensitive: {df_product_master['tariff_sensitive'].sum():,}")

# =============================================================================
# PARSE PRICING COLUMN NAMES
# =============================================================================

def parse_pricing_column(col_name):
    """
    Parse a pricing column name to extract division, price type, and quarter.
    
    Examples:
        'KC LIST COST' -> ('KC', 'LIST_COST', 'Q1')
        'KC BSP.1' -> ('KC', 'BSP', 'Q2')
        'SP CITY SRP.3' -> ('SP', 'CITY_SRP', 'Q4')
    """
    # Check for quarter suffix
    quarter = 'Q1'
    for suffix, q in QUARTER_SUFFIXES.items():
        if suffix and col_name.endswith(suffix):
            quarter = q
            col_name = col_name[:-len(suffix)]
            break
    
    # Extract division (first 2 characters)
    parts = col_name.split(' ', 1)
    if len(parts) >= 2 and parts[0] in DIVISIONS:
        division = parts[0]
        price_type = parts[1].replace(' ', '_').upper()
        return division, price_type, quarter
    
    return None, None, None

# Test the parser
test_cols = ['KC LIST COST', 'KC BSP', 'KC BSP.1', 'SP CITY SRP.3', 'NA RURAL SRP.2']
print("Testing column parser:")
for col in test_cols:
    result = parse_pricing_column(col)
    print(f"  '{col}' -> {result}")

# =============================================================================
# MELT PRICING DATA
# =============================================================================

print("Melting pricing data to long format...")
print("This may take a minute...")

# Get pricing columns (after product attributes)
pricing_cols = [col for col in df_pricing_raw.columns if col not in PRODUCT_COLUMNS]

# Build a list to collect melted data
melted_records = []

# Process each row
for idx, row in df_pricing_raw.iterrows():
    item_code = row['Item Code']
    
    # Group pricing values by division and quarter
    div_qtr_prices = {}
    
    for col in pricing_cols:
        division, price_type, quarter = parse_pricing_column(col)
        
        if division and price_type:
            key = (division, quarter)
            if key not in div_qtr_prices:
                div_qtr_prices[key] = {'item_code': item_code, 'division': division, 'quarter': quarter}
            
            # Standardize price type names - normalize multiple spaces to single space
            price_type_clean = ' '.join(price_type.lower().replace('_', ' ').split())
            if 'list cost' in price_type_clean:
                div_qtr_prices[key]['list_cost'] = row[col]
            elif price_type_clean == 'bsp':
                div_qtr_prices[key]['bsp'] = row[col]
            elif 'city srp' in price_type_clean:
                div_qtr_prices[key]['city_srp'] = row[col]
            elif 'rural srp' in price_type_clean:
                div_qtr_prices[key]['rural_srp'] = row[col]
            elif 'srp unit' in price_type_clean:
                div_qtr_prices[key]['srp_unit_qty'] = row[col]
    
    melted_records.extend(div_qtr_prices.values())
    
    if (idx + 1) % 1000 == 0:
        print(f"  Processed {idx + 1:,} rows...")

# Create DataFrame
df_pricing_long = pd.DataFrame(melted_records)

print(f"\n✓ Pricing data melted: {len(df_pricing_long):,} rows")
print(f"  Columns: {list(df_pricing_long.columns)}")

# =============================================================================
# ADD REGION AND DIVISION NAME
# =============================================================================

df_pricing_long['division_name'] = df_pricing_long['division'].map(DIVISIONS)
df_pricing_long['region'] = df_pricing_long['division'].map(DIVISION_REGIONS)

# Preview
print("Pricing long format preview:")
df_pricing_long.head(10)

# =============================================================================
# EXAMINE SALES COLUMN STRUCTURE
# =============================================================================

# Look at one sheet to understand column structure
sample_div = list(sales_sheets.keys())[0]
sample_cols = sales_sheets[sample_div].columns.tolist()

print(f"Sample sales columns ({sample_div} division):")
for col in sample_cols:
    print(f"  {col}")

# =============================================================================
# MELT SALES DATA
# =============================================================================

print("Melting sales data to long format...")

# Column suffix to quarter mapping
# The sales file uses: '$ SALES' (Q1), '$ SALES.1' (Q2), '$ SALES.2' (Q3), '$ SALES.3' (Q4)
SUFFIX_TO_QUARTER = {
    '': 'Q1',
    '.1': 'Q2',
    '.2': 'Q3',
    '.3': 'Q4'
}

sales_long_records = []

for division, df_sales in sales_sheets.items():
    print(f"  Processing {division}...")
    
    # Find Item Code column
    item_code_col = None
    for col in df_sales.columns:
        if 'item code' in col.lower():
            item_code_col = col
            break
    
    if not item_code_col:
        print(f"    Warning: No Item Code column found in {division}")
        continue
    
    # Identify base sales column names (without suffix)
    # Look for '$ SALES' or 'BILLED CASE QUANTITY' base columns
    sales_dollar_base = None
    sales_units_base = None
    
    for col in df_sales.columns:
        col_upper = col.upper().strip()
        # Find the base column without suffix
        if col_upper == '$ SALES':
            sales_dollar_base = '$ SALES'
        elif col_upper == 'BILLED CASE QUANTITY':
            sales_units_base = 'BILLED CASE QUANTITY'
    
    # Process each row
    for _, row in df_sales.iterrows():
        item_code = row[item_code_col]
        
        # Create record for each quarter
        for suffix, quarter in SUFFIX_TO_QUARTER.items():
            record = {
                'item_code': item_code,
                'division': division,
                'quarter': quarter
            }
            
            # Get sales dollars for this quarter
            if sales_dollar_base:
                col_name = sales_dollar_base + suffix
                if col_name in df_sales.columns:
                    record['sales_dollars'] = row[col_name]
            
            # Get sales units for this quarter
            if sales_units_base:
                col_name = sales_units_base + suffix
                if col_name in df_sales.columns:
                    record['sales_units'] = row[col_name]
            
            # Add record if we have any sales data
            if 'sales_dollars' in record or 'sales_units' in record:
                sales_long_records.append(record)

df_sales_long = pd.DataFrame(sales_long_records)

print(f"\n✓ Sales data melted: {len(df_sales_long):,} rows")
print(f"  Divisions: {df_sales_long['division'].nunique()}")
print(f"  Quarters: {df_sales_long['quarter'].nunique()}")

# =============================================================================
# ADD REGION AND DIVISION NAME TO SALES
# =============================================================================

df_sales_long['division_name'] = df_sales_long['division'].map(DIVISIONS)
df_sales_long['region'] = df_sales_long['division'].map(DIVISION_REGIONS)

# Preview
print("Sales long format preview:")
df_sales_long.head(10)

# =============================================================================
# MERGE PRICING + SALES
# =============================================================================

print("Merging pricing and sales data...")

# Merge on item_code, division, quarter
df_merged = pd.merge(
    df_pricing_long,
    df_sales_long[['item_code', 'division', 'quarter', 'sales_dollars', 'sales_units']],
    on=['item_code', 'division', 'quarter'],
    how='left'
)

# Add product attributes (including Pack for unit price normalization)
df_merged = pd.merge(
    df_merged,
    df_product_master[['Item Code', 'Item Name', 'Category', 'Sub Category', 
                       'Brand Label Name', 'National Comparison Item Code',
                       'Pack (Units per Case)',
                       'tariff_sensitive', 'has_national_link']],
    left_on='item_code',
    right_on='Item Code',
    how='left'
)

# Clean up column names
df_merged = df_merged.rename(columns={
    'Item Name': 'item_name',
    'Category': 'category',
    'Sub Category': 'sub_category',
    'Brand Label Name': 'brand',
    'National Comparison Item Code': 'national_item_code',
    'Pack (Units per Case)': 'pack'
})

# Drop duplicate Item Code column
if 'Item Code' in df_merged.columns:
    df_merged = df_merged.drop(columns=['Item Code'])

print(f"\n✓ Merged dataset: {len(df_merged):,} rows × {len(df_merged.columns)} columns")
print(f"\nColumns: {list(df_merged.columns)}")

# =============================================================================
# CALCULATE UNIT-LEVEL PRICES (NORMALIZATION)
# =============================================================================

print("Calculating unit-level prices...")

# BSP and List Cost are CASE prices, need to divide by Pack to get unit prices
df_merged['bsp_per_unit'] = df_merged['bsp'] / df_merged['pack']
df_merged['list_cost_per_unit'] = df_merged['list_cost'] / df_merged['pack']

# Flag display/promotional items (SRP < $0.10 are placeholder prices)
df_merged['is_display_item'] = (df_merged['city_srp'] < 0.10).astype(int)

# Calculate unit BSP to SRP ratio (should be ~0.7 for normal items)
df_merged['unit_bsp_srp_ratio'] = np.where(
    df_merged['city_srp'] > 0,
    df_merged['bsp_per_unit'] / df_merged['city_srp'],
    np.nan
)

# Summary
display_count = df_merged['is_display_item'].sum()
print(f"  Display/promo items flagged: {display_count:,} ({100*display_count/len(df_merged):.1f}%)")
print(f"  Normal items: {len(df_merged) - display_count:,}")

# Unit price validation
valid_ratio = df_merged[(df_merged['unit_bsp_srp_ratio'] >= 0.5) & (df_merged['unit_bsp_srp_ratio'] <= 1.0)]
print(f"  Items with valid unit BSP/SRP ratio (0.5-1.0): {len(valid_ratio):,} ({100*len(valid_ratio)/len(df_merged):.1f}%)")

print("\n✓ Unit-level prices calculated!")
print("  New columns: bsp_per_unit, list_cost_per_unit, is_display_item, unit_bsp_srp_ratio")

# =============================================================================
# CALCULATE PRICE CHANGES
# =============================================================================

print("Calculating quarter-over-quarter price changes...")

# Sort data for proper lag calculation
df_merged_sorted = df_merged.sort_values(['item_code', 'division', 'quarter']).copy()

# Create quarter order for sorting
quarter_order = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
df_merged_sorted['quarter_num'] = df_merged_sorted['quarter'].map(quarter_order)

# Calculate lagged values and changes
price_cols = ['list_cost', 'bsp', 'city_srp', 'rural_srp']
sales_cols = ['sales_dollars', 'sales_units']

for col in price_cols + sales_cols:
    if col in df_merged_sorted.columns:
        # Previous quarter value
        df_merged_sorted[f'{col}_prev'] = df_merged_sorted.groupby(['item_code', 'division'])[col].shift(1)
        
        # Absolute change
        df_merged_sorted[f'{col}_change'] = df_merged_sorted[col] - df_merged_sorted[f'{col}_prev']
        
        # Percentage change
        df_merged_sorted[f'{col}_change_pct'] = (
            df_merged_sorted[f'{col}_change'] / df_merged_sorted[f'{col}_prev']
        ) * 100

# Create period label
df_merged_sorted['period'] = df_merged_sorted['quarter_num'].map({
    2: 'Q1→Q2',
    3: 'Q2→Q3',
    4: 'Q3→Q4'
})

# Filter to rows with changes (Q2, Q3, Q4 only - Q1 has no prior quarter)
df_price_changes = df_merged_sorted[df_merged_sorted['quarter'] != 'Q1'].copy()

print(f"\n✓ Price changes dataset: {len(df_price_changes):,} rows")

# =============================================================================
# CALCULATE PASS-THROUGH RATE
# =============================================================================

# Pass-through rate = BSP change / List Cost change
df_price_changes['pass_through_rate'] = np.where(
    df_price_changes['list_cost_change'] != 0,
    df_price_changes['bsp_change'] / df_price_changes['list_cost_change'],
    np.nan
)

# Pass-through percentage = BSP change % / List Cost change %
df_price_changes['pass_through_pct'] = np.where(
    df_price_changes['list_cost_change_pct'] != 0,
    df_price_changes['bsp_change_pct'] / df_price_changes['list_cost_change_pct'] * 100,
    np.nan
)

print("Pass-through metrics calculated!")

# =============================================================================
# CREATE NATIONAL BRAND COMPARISON DATASET (Using Unit Prices)
# =============================================================================

print("Creating National Brand comparison dataset...")

# Filter to Best Choice items with national linkage, EXCLUDING display items
df_bc = df_merged[(df_merged['brand'] == 'Best Choice') & (df_merged['is_display_item'] == 0)].copy()
df_bc_linked = df_bc[df_bc['national_item_code'].notna()].copy()

print(f"  Best Choice items (non-display): {len(df_bc):,}")
print(f"  With National linkage: {len(df_bc_linked):,}")

# Get National Brand prices (using unit prices) - exclude display items
df_national = df_merged[df_merged['is_display_item'] == 0][
    ['item_code', 'division', 'quarter', 'bsp', 'bsp_per_unit', 'city_srp', 'pack']
].copy()

# Rename for joining
df_national = df_national.rename(columns={
    'item_code': 'national_item_code',
    'bsp': 'national_bsp',
    'bsp_per_unit': 'national_bsp_per_unit',
    'city_srp': 'national_city_srp',
    'pack': 'national_pack'
})

# Join National Brand prices to Best Choice items
df_bc_national = pd.merge(
    df_bc_linked,
    df_national,
    on=['national_item_code', 'division', 'quarter'],
    how='left'
)

# Calculate price gaps using UNIT prices (normalized)
df_bc_national['price_gap_unit_abs'] = df_bc_national['national_bsp_per_unit'] - df_bc_national['bsp_per_unit']
df_bc_national['price_gap_unit_pct'] = np.where(
    df_bc_national['national_bsp_per_unit'] > 0,
    (df_bc_national['national_bsp_per_unit'] - df_bc_national['bsp_per_unit']) / df_bc_national['national_bsp_per_unit'] * 100,
    np.nan
)

# Also keep the CASE-level gaps for reference
df_bc_national['price_gap_case_abs'] = df_bc_national['national_bsp'] - df_bc_national['bsp']
df_bc_national['price_gap_case_pct'] = np.where(
    df_bc_national['national_bsp'] > 0,
    (df_bc_national['national_bsp'] - df_bc_national['bsp']) / df_bc_national['national_bsp'] * 100,
    np.nan
)

# Gap vs 20% target (using unit prices)
df_bc_national['gap_vs_target'] = df_bc_national['price_gap_unit_pct'] - 20

# Legacy columns for backward compatibility
df_bc_national['price_gap_abs'] = df_bc_national['price_gap_unit_abs']
df_bc_national['price_gap_pct'] = df_bc_national['price_gap_unit_pct']

print(f"\n✓ BC-National comparison dataset: {len(df_bc_national):,} rows")
print(f"  Using UNIT prices (BSP/Pack) for accurate comparison")
print(f"  Display items excluded")

# =============================================================================
# CREATE CATEGORY SUMMARY
# =============================================================================

print("Creating category summary dataset...")

df_category_summary = df_merged.groupby(['category', 'division', 'quarter', 'brand']).agg({
    'item_code': 'count',
    'bsp': 'mean',
    'city_srp': 'mean',
    'list_cost': 'mean',
    'sales_dollars': 'sum',
    'sales_units': 'sum'
}).reset_index()

df_category_summary = df_category_summary.rename(columns={
    'item_code': 'item_count',
    'bsp': 'avg_bsp',
    'city_srp': 'avg_city_srp',
    'list_cost': 'avg_list_cost',
    'sales_dollars': 'total_sales_dollars',
    'sales_units': 'total_sales_units'
})

print(f"\n✓ Category summary: {len(df_category_summary):,} rows")

# =============================================================================
# SAVE ALL PREPARED DATASETS
# =============================================================================

print("Saving prepared datasets...")
print(f"Output directory: {OUTPUT_DIR}")
print()

datasets = {
    'product_master.csv': df_product_master,
    'pricing_long.csv': df_pricing_long,
    'sales_long.csv': df_sales_long,
    'pricing_sales_merged.csv': df_merged,
    'price_changes.csv': df_price_changes,
    'bc_national_comparison.csv': df_bc_national,
    'category_summary.csv': df_category_summary
}

for filename, df in datasets.items():
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(filepath, index=False)
    print(f"  ✓ {filename}: {len(df):,} rows")

print("\n" + "="*60)
print("DATA PREPARATION COMPLETE!")
print("="*60)

# =============================================================================
# FINAL DATA SUMMARY
# =============================================================================

print("="*60)
print("PREPARED DATA SUMMARY")
print("="*60)

print("\n1. PRODUCT MASTER")
print(f"   Total products: {len(df_product_master):,}")
print(f"   By brand:")
for brand, count in df_product_master['Brand Label Name'].value_counts().items():
    print(f"      {brand}: {count:,}")

print("\n2. PRICING LONG")
print(f"   Total rows: {len(df_pricing_long):,}")
print(f"   Divisions: {df_pricing_long['division'].nunique()}")
print(f"   Quarters: {df_pricing_long['quarter'].nunique()}")

print("\n3. SALES LONG")
print(f"   Total rows: {len(df_sales_long):,}")

print("\n4. MERGED PRICING + SALES")
print(f"   Total rows: {len(df_merged):,}")
print(f"   Rows with sales data: {df_merged['sales_dollars'].notna().sum():,}")

print("\n5. PRICE CHANGES")
print(f"   Total rows: {len(df_price_changes):,}")

print("\n6. BC-NATIONAL COMPARISON")
print(f"   Total rows: {len(df_bc_national):,}")
print(f"   Avg price gap: {df_bc_national['price_gap_pct'].mean():.1f}%")

print("\n" + "="*60)
print("Ready for analysis! Run the RQ notebooks next.")
print("="*60)
