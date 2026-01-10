# AWG Spring 2026 Project - Session Notes

**Last Updated:** January 2, 2026
**Project:** University of Illinois Spring 2026 - AWG Brands Pricing Analysis

---

## Project Overview

Analysis of AWG (Associated Wholesale Grocers) private label brands pricing and sales data to answer 6 research questions about price gaps, cost pass-through, elasticity, cross-brand effects, geographic variation, and tariff impact.

---

## Critical Discovery

**BSP (Base Selling Price) is a CASE-level price, while SRP (Suggested Retail Price) is a UNIT-level price.**

This caused initial analysis to show incorrect results:
- Before normalization: 13.8% average price gap, 3,005 negative gaps (9.7%)
- After normalization: 32.3% average price gap, 40 negative gaps (0.1%)

**Normalization Formula:**
```
Unit BSP = BSP / Pack (Units per Case)
Unit List Cost = List Cost / Pack (Units per Case)
```

---

## Files Created

### Notebooks
| File | Purpose |
|------|---------|
| `00_Data_Preparation.ipynb` | Central data prep with unit normalization |
| `RQ1_Price_Gap_Analysis.ipynb` | Price gap vs 20% target |
| `RQ2_Cost_Pass_Through.ipynb` | Cost change transmission |
| `RQ3_Price_Elasticity.ipynb` | Demand elasticity |
| `RQ4_Cross_Brand_Effects.ipynb` | BC vs AS interactions |
| `RQ5_Geographic_Variation.ipynb` | Division-level analysis |
| `RQ6_Tariff_Impact.ipynb` | Tariff effect analysis |
| `Data_Quality_Findings_Notebook.ipynb` | Interactive walkthrough of findings |

### Data Outputs
| Directory | Purpose |
|-----------|---------|
| `prepared_data/` | Original case-level BSP analysis |
| `prepared_data_normalized/` | Normalized unit-level BSP analysis |

### Client Deliverables
| File | Purpose |
|------|---------|
| `Client_Review_Data_Quality_Issues.xlsx` | Excel with 4 sheets for client review |
| `AWG_Data_Analysis_Findings.md` | Complete findings documentation |
| `Data_Quality_Issues_Updated.csv` | Issues summary CSV |

### Supporting Scripts
| File | Purpose |
|------|---------|
| `create_client_review_files.py` | Generates client review Excel |
| `Analysis_Plan.md` | Comprehensive analysis plan |

---

## Excel File Structure (Client_Review_Data_Quality_Issues.xlsx)

1. **Summary** - Overview of issues
2. **Resolved_Issues_GREEN** - 2,628 rows fixed by normalization
3. **Remaining_Issues_RED** - 67 rows needing client review
   - Includes complete product info: BC & National item codes, names, categories, pack sizes
4. **Statistics_Comparison** - Before/after metrics

---

## Key Findings Summary

### RQ1: Price Gap
- Average gap: 32.3% (above 20% target)
- Best Choice is competitively priced

### RQ2: Cost Pass-Through
- Average: 0.40 (partial pass-through)
- National Brand: 1.05 | Best Choice: 0.35 | Always Save: 0.19

### RQ3: Price Elasticity
- Overall demand inelastic (median -0.28)
- Most elastic: Soup (-5.00)

### RQ4: Cross-Brand Effects
- BC-AS gap median: 34.3% (BC higher than AS)
- Cross-elasticity near zero (independent demand)

### RQ5: Geographic Variation
- BSP variation low (1.9% CV)
- Rural prices 3.1% higher
- **Issue:** 43.8% of items have varying List Cost across divisions

### RQ6: Tariff Impact
- Tariff-sensitive categories: 2.03% cost change vs 0.90% others
- Oral Hygiene category has unusual price changes (z=3.72)

---

## Outstanding Issues for Client

1. **40 remaining negative price gaps** - BC genuinely priced higher than National
2. **43.8% List Cost variation** - Should be uniform, needs clarification
3. **Confirm price unit assumptions** - BSP=case, SRP=unit

---

## Data Sources

- **Pricing:** `Product Details & Pricing by quarter by division 12.19.25.xlsx`
  - Header row: 3, Products: 4,319, Columns: 229

- **Sales:** `Sales Data by Quarter - U of I Project 12.19.25.xlsx`
  - Header row: 2, Sheets: 9 (one per division)
  - Sheet corrections: GO->NA, NO->NE

---

## Technical Notes

### Quarter Column Mapping (Sales File)
- `$ SALES` = Q1
- `$ SALES.1` = Q2
- `$ SALES.2` = Q3
- `$ SALES.3` = Q4

### Known Code Fixes Applied
1. Sales melting: Changed from "Q1"/"Q2" pattern to suffix pattern
2. Rural SRP: Added space normalization for double spaces
3. Made code robust to check if columns exist before using

---

## Next Steps (When Resuming)

1. Review client feedback on Excel file
2. Clarify List Cost variation with client
3. Confirm BSP/SRP unit assumptions
4. Finalize analysis with any client-requested changes
5. Prepare final presentation/report

---

## Session History

- **Session 1 (Jan 2, 2026):** Created all notebooks, discovered price unit mismatch, implemented normalization, created client review files with complete product information

---

*This file serves as persistent memory for continuing the project in future sessions.*
