# AWG Brands Data Analysis - Complete Findings Report

## Executive Summary

This document summarizes the data quality analysis and key findings from the AWG Brands pricing and sales data analysis for the University of Illinois Spring 2026 project.

### Critical Discovery: Price Unit Mismatch

**The most significant finding is that BSP (Base Selling Price) is a CASE-level price, while SRP (Suggested Retail Price) and National Brand comparisons were being made at the UNIT level.** This caused substantial apparent data quality issues that were resolved once prices were normalized to unit level using the `Pack (Units per Case)` variable.

---

## 1. Data Quality Issues - Before vs After Normalization

### 1.1 Price Gap Analysis (RQ1)

| Metric | Before (Case BSP) | After (Unit BSP) | Impact |
|--------|-------------------|------------------|--------|
| Average Price Gap | 13.8% | **32.3%** | +18.5 points |
| Median Price Gap | 29.5% | **30.9%** | +1.4 points |
| Status vs 20% Target | Below target | **Above target** | Reversal |
| Negative Gaps | 3,005 (9.7%) | **40 (0.1%)** | -98.7% reduction |
| Extreme Gaps (>60%) | 2,017 | **790** | -60.8% reduction |

### 1.2 Key Insight

The original analysis suggested Best Choice was priced too HIGH relative to National Brands (only 13.8% gap vs 20% target). After normalization, we find Best Choice is actually priced APPROPRIATELY LOW (32.3% gap), exceeding the 20% target.

---

## 2. Data Structure Findings

### 2.1 Price Fields and Their Units

| Field | Unit Level | Description |
|-------|------------|-------------|
| **List Cost** | CASE | AWG's cost per case |
| **BSP** | CASE | Base Selling Price per case |
| **City SRP** | UNIT | Suggested Retail Price per unit |
| **Rural SRP** | UNIT | Suggested Retail Price per unit (rural) |
| **Pack (Units per Case)** | - | Number of units in a case |

### 2.2 Normalization Formula

```
Unit BSP = BSP / Pack (Units per Case)
Unit List Cost = List Cost / Pack (Units per Case)
```

### 2.3 Validation

After normalization:
- **76.4%** of items have Unit BSP/SRP ratio between 0.5-1.0 (expected range)
- **Median ratio: 0.71** (wholesale is ~71% of retail - typical markup)
- Only **0.4%** of items are display/promotional (SRP < $0.10)

---

## 3. Remaining Data Quality Issues

### 3.1 Issues Resolved by Normalization: 2,628 rows
These appeared as negative price gaps (BC > National) but were caused by comparing different pack sizes.

### 3.2 Issues Remaining After Normalization: 67 rows
These are genuine anomalies requiring client review:

| Issue Type | Count | Example |
|------------|-------|---------|
| Negative gaps (BC still > National) | 40 | Personal Cleansing items |
| Extreme high gaps (>80%) | 27 | Cough & Cold, Pain Remedies |

### 3.3 List Cost Inconsistency (Separate Issue)

**43.8% of items have varying List Cost across divisions.**

This is unexpected - List Cost should typically be uniform. Possible explanations:
- Regional supplier pricing
- Freight cost differences
- Data entry errors
- Intentional regional pricing strategy

**Recommendation:** Clarify with client whether this is intentional.

---

## 4. Research Question Findings

### RQ1: Price Gap Analysis
- **Finding:** Average gap is 32.3%, above the 20% target
- **Implication:** Best Choice products are competitively priced
- **Categories with largest gaps:** Cough & Cold (62.9%), Pain Remedies (58.4%)
- **Categories near target:** Frozen Baked Goods (20.5%), Fruit Dried (19.5%)

### RQ2: Cost Pass-Through
- **Finding:** Average pass-through rate is 0.40 (partial)
- **Brand differences:**
  - National Brand: 1.05 (full pass-through)
  - Best Choice: 0.35 (absorbs ~65% of cost changes)
  - Always Save: 0.19 (absorbs ~81% of cost changes)
- **Asymmetry:** Cost increases pass through more (0.47) than decreases (0.13)

### RQ3: Price Elasticity
- **Finding:** Overall demand is inelastic (median elasticity -0.28)
- **Most elastic category:** Soup (-5.00 median elasticity)
- **Implication:** Moderate price increases unlikely to significantly impact sales

### RQ4: Cross-Brand Effects
- **Finding:** BC-AS gap median is 34.3% (BC priced higher than AS)
- **Cross-elasticity:** Near zero (-0.01), suggesting independent demand
- **Implication:** BC and AS price changes don't significantly cannibalize each other

### RQ5: Geographic Variation
- **Finding:** BSP variation across divisions is low (1.9% CV)
- **City-Rural gap:** Rural prices 3.1% higher on average
- **Issue:** List Cost variation (43.8%) needs clarification

### RQ6: Tariff Impact
- **Finding:** Tariff-sensitive categories show 2.03% cost change vs 0.90% for others
- **Timing:** Q3-Q4 showed most large price increases (11.2% of items)
- **Anomaly:** Oral Hygiene category has unusual price changes (z=3.72)

---

## 5. Files Created for Client Review

### 5.1 Excel File with Highlighting
**File:** `Client_Review_Data_Quality_Issues.xlsx`

| Sheet | Description | Row Count |
|-------|-------------|-----------|
| Summary | Overview of issues | - |
| Resolved_Issues_GREEN | Issues fixed by normalization | 2,628 |
| Remaining_Issues_RED | Issues needing review | 67 |
| Statistics_Comparison | Before/after metrics | - |

### 5.2 Data Files

| File | Location | Description |
|------|----------|-------------|
| Original data | `prepared_data/` | Case-level BSP analysis |
| Normalized data | `prepared_data_normalized/` | Unit-level BSP analysis |
| Issues summary | `Data_Quality_Issues_Updated.csv` | All flagged issues |

---

## 6. Recommendations for Client Discussion

### 6.1 Confirm Price Units
- **Question:** Is BSP always a case price and SRP always a unit price?
- **Impact:** All price gap and comparison analyses depend on this

### 6.2 Review Remaining Anomalies
- **67 items** still show unusual pricing after normalization
- Most are Personal Cleansing items with BC > National
- May indicate data entry errors or intentional premium pricing

### 6.3 Clarify List Cost Variation
- **43.8%** of items have different List Cost by division
- Is this intentional regional pricing or data quality issue?

### 6.4 Approve Normalization Approach
- **Proposed formula:** Unit Price = Case Price / Pack
- **Validation:** 76.4% of items show expected wholesale-retail relationship
- **Request:** Client approval before using normalized data for final analysis

---

## 7. Technical Notes

### 7.1 Data Sources
- **Pricing file:** `Product Details & Pricing by quarter by division 12.19.25.xlsx`
  - Header row: 3
  - Products: 4,319
  - Columns: 229 (13 product + 216 pricing)

- **Sales file:** `Sales Data by Quarter - U of I Project 12.19.25.xlsx`
  - Header row: 2
  - Sheets: 9 (one per division)
  - Sheet name corrections: GO->NA, NO->NE

### 7.2 Quarter Column Mapping
Sales file uses suffix pattern:
- `$ SALES` = Q1
- `$ SALES.1` = Q2
- `$ SALES.2` = Q3
- `$ SALES.3` = Q4

### 7.3 Display Items Excluded
Items with `City SRP < $0.10` are flagged as display/promotional items and excluded from price comparisons (0.4% of data).

---

## 8. Next Steps

1. **Client meeting** to review highlighted Excel file
2. **Confirm** price unit assumptions (BSP=case, SRP=unit)
3. **Approve** normalization approach
4. **Clarify** List Cost variation across divisions
5. **Finalize** analysis with approved data transformations

---

*Report generated: January 2, 2026*
*Prepared for: University of Illinois Spring 2026 Project*
