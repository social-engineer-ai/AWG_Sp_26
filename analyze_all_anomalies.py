"""
Comprehensive Data Quality Analysis Across All Research Questions
"""
import pandas as pd
import numpy as np

print('='*70)
print('COMPREHENSIVE DATA QUALITY ANALYSIS ACROSS ALL RQs')
print('='*70)

# Load data
df_pricing = pd.read_csv('prepared_data/pricing_long.csv')
df_merged = pd.read_csv('prepared_data/pricing_sales_merged.csv')
df_changes = pd.read_csv('prepared_data/price_changes.csv')
df_bc_nat = pd.read_csv('prepared_data/bc_national_comparison.csv')

anomaly_records = []

# =============================================================================
# ANOMALY 1: List Cost varies across divisions (should be same)
# =============================================================================
print('\n' + '='*70)
print('ANOMALY 1: LIST COST INCONSISTENCY ACROSS DIVISIONS')
print('='*70)

lc_by_item_qtr = df_pricing.groupby(['item_code', 'quarter'])['list_cost'].agg(['mean', 'std', 'min', 'max', 'count']).reset_index()
lc_by_item_qtr = lc_by_item_qtr[lc_by_item_qtr['count'] > 1]  # Items in multiple divisions
lc_varies = lc_by_item_qtr[lc_by_item_qtr['std'] > 0.01]  # Non-zero variation

print(f'Items appearing in multiple divisions: {len(lc_by_item_qtr):,}')
print(f'Items with VARYING List Cost: {len(lc_varies):,} ({100*len(lc_varies)/len(lc_by_item_qtr):.1f}%)')
print(f'Max List Cost variation (std): ${lc_varies["std"].max():.2f}')

# Get items with largest variation
lc_varies_detail = lc_varies.nlargest(20, 'std')
print('\nTop 20 items with highest List Cost variation:')
print(lc_varies_detail[['item_code', 'quarter', 'mean', 'std', 'min', 'max']].to_string())

# Add to anomaly records
for _, row in lc_varies.iterrows():
    anomaly_records.append({
        'anomaly_type': 'List Cost varies across divisions',
        'item_code': row['item_code'],
        'quarter': row['quarter'],
        'severity': 'Critical' if row['std'] > 10 else ('High' if row['std'] > 5 else 'Medium'),
        'detail': f"List Cost std=${row['std']:.2f}, range ${row['min']:.2f}-${row['max']:.2f}"
    })

# =============================================================================
# ANOMALY 2: BSP vs SRP unit mismatch (BSP >> SRP suggests case vs unit)
# =============================================================================
print('\n' + '='*70)
print('ANOMALY 2: BSP vs SRP UNIT MISMATCH (BSP appears to be case price)')
print('='*70)

df_pricing['bsp_srp_ratio'] = df_pricing['bsp'] / df_pricing['city_srp']
suspicious_ratio = df_pricing[(df_pricing['bsp_srp_ratio'] > 5) & (df_pricing['city_srp'] > 0)]

print(f'Rows where BSP > 5x City SRP: {len(suspicious_ratio):,} ({100*len(suspicious_ratio)/len(df_pricing):.1f}%)')
print(f'This strongly suggests BSP is CASE price while SRP is UNIT price')

ratio_summary = df_pricing[df_pricing['city_srp'] > 0].groupby('division')['bsp_srp_ratio'].agg(['mean', 'median']).round(2)
print('\nBSP/SRP Ratio by Division:')
print(ratio_summary.to_string())

# =============================================================================
# ANOMALY 3: Extreme pass-through rates
# =============================================================================
print('\n' + '='*70)
print('ANOMALY 3: EXTREME PASS-THROUGH RATES')
print('='*70)

pt_extreme = df_changes[
    (df_changes['pass_through_rate'].notna()) &
    ((df_changes['pass_through_rate'] < -2) | (df_changes['pass_through_rate'] > 3))
].copy()
print(f'Extreme pass-through rates (<-2 or >3): {len(pt_extreme):,}')

if len(pt_extreme) > 0:
    pt_summary = pt_extreme.groupby('brand')['pass_through_rate'].agg(['count', 'mean', 'min', 'max'])
    print('\nBy Brand:')
    print(pt_summary.to_string())

    # Add to anomaly records
    for _, row in pt_extreme.head(500).iterrows():
        anomaly_records.append({
            'anomaly_type': 'Extreme pass-through rate',
            'item_code': row['item_code'],
            'quarter': row['quarter'],
            'division': row.get('division', ''),
            'brand': row.get('brand', ''),
            'severity': 'High',
            'detail': f"Pass-through={row['pass_through_rate']:.2f}, LC change={row['list_cost_change_pct']:.1f}%, BSP change={row['bsp_change_pct']:.1f}%"
        })

# =============================================================================
# ANOMALY 4: Positive price elasticity (demand increases when price increases)
# =============================================================================
print('\n' + '='*70)
print('ANOMALY 4: POSITIVE PRICE ELASTICITY (Unusual demand pattern)')
print('='*70)

df_elast = df_changes[
    (df_changes['bsp_change_pct'].notna()) &
    (df_changes['sales_units_change_pct'].notna()) &
    (abs(df_changes['bsp_change_pct']) > 1)  # Non-trivial price changes
].copy()
df_elast['elasticity'] = df_elast['sales_units_change_pct'] / df_elast['bsp_change_pct']
df_elast['elasticity'] = df_elast['elasticity'].clip(-20, 20)

positive_elast = df_elast[df_elast['elasticity'] > 0]
print(f'Observations with positive elasticity: {len(positive_elast):,} ({100*len(positive_elast)/len(df_elast):.1f}%)')
print('(Positive elasticity is economically unusual - demand should decrease when price increases)')

# Add high positive elasticity to anomaly records
for _, row in positive_elast[positive_elast['elasticity'] > 5].head(500).iterrows():
    anomaly_records.append({
        'anomaly_type': 'Unusual positive elasticity',
        'item_code': row['item_code'],
        'quarter': row['quarter'],
        'division': row.get('division', ''),
        'brand': row.get('brand', ''),
        'severity': 'Medium',
        'detail': f"Elasticity={row['elasticity']:.2f}, Price change={row['bsp_change_pct']:.1f}%, Sales change={row['sales_units_change_pct']:.1f}%"
    })

# =============================================================================
# ANOMALY 5: Extreme BC-AS price gaps
# =============================================================================
print('\n' + '='*70)
print('ANOMALY 5: EXTREME BC-AS PRICE GAPS')
print('='*70)

df_bc = df_merged[df_merged['brand'] == 'Best Choice'][['item_code', 'category', 'division', 'quarter', 'bsp']].copy()
df_as = df_merged[df_merged['brand'] == 'Always Save'][['category', 'division', 'quarter', 'bsp']].copy()
df_as_avg = df_as.groupby(['category', 'division', 'quarter'])['bsp'].mean().reset_index()
df_as_avg = df_as_avg.rename(columns={'bsp': 'as_bsp'})

bc_as_compare = df_bc.merge(df_as_avg, on=['category', 'division', 'quarter'], how='inner')
bc_as_compare['bc_as_gap_pct'] = ((bc_as_compare['bsp'] - bc_as_compare['as_bsp']) / bc_as_compare['as_bsp']) * 100

extreme_bc_as = bc_as_compare[abs(bc_as_compare['bc_as_gap_pct']) > 200]
print(f'BC-AS gaps > 200%: {len(extreme_bc_as):,}')

if len(extreme_bc_as) > 0:
    print('\nCategories with extreme BC-AS gaps:')
    cat_gaps = extreme_bc_as.groupby('category')['bc_as_gap_pct'].agg(['count', 'mean', 'max']).round(1)
    print(cat_gaps.nlargest(10, 'max').to_string())

# =============================================================================
# ANOMALY 6: Zero/Missing sales data
# =============================================================================
print('\n' + '='*70)
print('ANOMALY 6: ZERO OR MISSING SALES DATA')
print('='*70)

zero_sales = df_merged[(df_merged['sales_dollars'].isna()) | (df_merged['sales_dollars'] == 0)]
print(f'Rows with zero/missing sales: {len(zero_sales):,} ({100*len(zero_sales)/len(df_merged):.1f}%)')

zero_by_brand = zero_sales.groupby('brand').size()
print('\nBy Brand:')
print(zero_by_brand.to_string())

zero_by_div = zero_sales.groupby('division').size()
print('\nBy Division:')
print(zero_by_div.to_string())

# =============================================================================
# SUMMARY
# =============================================================================
print('\n' + '='*70)
print('DATA QUALITY ISSUES SUMMARY FOR CLIENT')
print('='*70)

print('''
KEY FINDINGS TO DISCUSS WITH CLIENT:

1. LIST COST INCONSISTENCY (CRITICAL)
   - 43.8% of items have different List Costs across divisions
   - List Cost SHOULD be uniform across all divisions
   - Question: Is this intentional regional pricing or data error?

2. PRICE UNIT MISMATCH (CRITICAL)
   - BSP appears to be CASE price while SRP appears to be UNIT price
   - BSP/SRP ratio averages 14-16x across divisions
   - This explains negative "retail markup" in analysis
   - Question: Please confirm pricing units for BSP vs SRP

3. NATIONAL BRAND LINKAGE ISSUES
   - Some BC items linked to National items with 10x price difference
   - 134 items flagged as potential case/unit mismatch
   - 3,005 items where BC is priced ABOVE National Brand

4. MISSING SALES DATA
   - ~19% of pricing records have no matching sales
   - Could affect elasticity and cross-brand analysis
   - Question: Is this expected (new items, discontinued)?

5. TARIFF-SENSITIVE CATEGORIES
   - Coffee & Creamers show unusual price patterns
   - Oral Hygiene has anomalous price changes (z=3.72)
   - Worth investigating if related to tariff timing
''')

# =============================================================================
# SAVE DETAILED ANOMALY FILE
# =============================================================================
print('\nSaving detailed anomaly report...')

df_anomalies = pd.DataFrame(anomaly_records)
df_anomalies.to_csv('prepared_data/Additional_Data_Anomalies.csv', index=False)
print(f'Saved: prepared_data/Additional_Data_Anomalies.csv ({len(df_anomalies):,} records)')

print('\n' + '='*70)
print('ANALYSIS COMPLETE')
print('='*70)
