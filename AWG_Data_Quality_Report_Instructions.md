# AWG Brands Pricing & Sales Data Quality Report - Task Instructions

## Objective
Create a comprehensive Jupyter Notebook (.ipynb) that audits the AWG Brands pricing and sales data for the U of I Spring 2026 project. This report will be reviewed by the project lead before sharing with AWG stakeholders.

---

## Project Context

### Background
AWG Brands (Associated Wholesale Grocers) is analyzing their private label brands (Best Choice and Always Save) pricing strategy compared to national brand equivalents. The goal is to evaluate:
1. Price gaps between Best Choice and National Brands (target ~20%)
2. How cost changes flow through from suppliers to stores to consumers
3. Impact of price changes on sales (elasticity)
4. Cross-brand effects between Best Choice and Always Save

### Key Stakeholders
- **Tyler Olinger & Kate Favrow** (AWG) - Project sponsors
- **Prof. Ashish Khandelwal & Jeremy Samuel** (U of I) - Academic leads

### Data Files Location
```
/mnt/project/Product_Details__Pricing_by_quarter_by_division_12_19_25.xlsx
/mnt/project/Sales_Data_by_Quarter__U_of_I_Project_12_19_25.xlsx
```

### Supporting Documents (for context)
```
/mnt/project/U_of_I_Project_Spring_2026__1_.docx  (Project requirements)
/mnt/project/AWG-MSBA_Spring_Project_Discussion.docx  (Meeting transcript)
```

---

## Data Structure Overview

### Pricing File Structure
- **Header row**: Row 3 (0-indexed) - use `header=3` when reading
- **Product columns (1-13)**: Item Code, Item Unit UPC Code, Case UPC Code, Size, Pack (Units per Case), Item Name, Inventory Department, Category, Sub Category, Brand Label Name, Brand Name, Item Long Description, National Comparison Item Code
- **Pricing columns (14+)**: 9 divisions × 4 quarters × 6 price fields = 216 columns

**Divisions**: KC (Kansas City), SP (Springfield), OK (Oklahoma), NA (Nashville), GC (Gulf Coast), NE (Nebraska), GL (Great Lakes), HN (Hernando), UM (Upper Midwest)

**Quarter Mapping**:
| Suffix | Quarter | Period |
|--------|---------|--------|
| (none) | Q1 | Nov 2024 - Jan 2025 |
| .1 | Q2 | Feb 2025 - Apr 2025 |
| .2 | Q3 | May 2025 - Jul 2025 |
| .3 | Q4 | Aug 2025 - Oct 2025 |

**Price Fields per Quarter**: LIST COST, BSP, SRP UNIT QUANTITY, CITY SRP, SRP UNIT QUANTITY (duplicate), RURAL SRP

### Sales File Structure
- **9 sheets**: One per division
- **Header row**: Row 2 (0-indexed) - use `header=2` when reading
- **IMPORTANT**: Sheet naming has typos:
  - "GO Division Sales" → Actually Nashville (NA)
  - "NO Division Sales" → Actually Nebraska (NE)
- **Sales columns**: $ SALES, BILLED CASE QUANTITY for each quarter (Q1-Q4)

### Brand Types
| Brand Label | Count | Description |
|-------------|-------|-------------|
| Best Choice | ~2,782 | Quality private label (comparable to national) |
| Always Save | ~470 | Value/opening price point brand |
| National Brand | ~1,067 | Name brands (Kraft, Bounty, etc.) |

**Note**: "Brand Label Name" column has trailing whitespace for "National Brand" - needs `.str.strip()`

---

## Report Requirements

### Notebook Structure

Create a Jupyter Notebook with the following sections:

---

### 1. Executive Summary (Markdown cell at top)
- Brief overview of data completeness status
- Key issues requiring attention (bulleted list)
- Recommendations summary

---

### 2. Setup & Data Loading
```python
# Required imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display, Markdown

# Set display options
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 100)

# Load data with correct headers
# Pricing: header=3
# Sales: header=2 per sheet
```

---

### 3. Data Structure Validation

#### 3.1 Column Inventory
- List all columns in pricing file with data types
- Verify 13 product columns + 216 pricing columns = 229 total
- Document the column naming pattern for each division/quarter

#### 3.2 Sales File Sheet Validation
- List all sheet names
- Verify sheet title matches expected division
- Flag the GO→NA and NO→NE naming issues
- Create a mapping dictionary for correct names

---

### 4. Data Completeness Analysis

#### 4.1 Product Attribute Completeness
Create a table showing for each product column:
- Column name
- Non-null count
- Percent populated
- Sample of null values (if any)

#### 4.2 Pricing Data Completeness

**By Division**: For each of the 9 divisions, calculate:
- % of items with Q1 pricing
- % of items with Q2 pricing
- % of items with Q3 pricing
- % of items with Q4 pricing
- % of items with ALL quarters
- % of items with NO pricing at all

Present as a heatmap visualization.

**By Brand**: Same analysis but grouped by brand (Best Choice, Always Save, National Brand)

**By Category**: Top 20 categories - what % have complete pricing data?

#### 4.3 Sales Data Completeness
Same structure as pricing but for sales:
- By Division (all 9 sheets)
- By Brand
- By Category

#### 4.4 Cross-File Alignment
- How many Item Codes appear in BOTH pricing and sales files?
- Items in pricing but NOT in sales (list sample)
- Items in sales but NOT in pricing (list sample)
- Recommend action for mismatches

---

### 5. Brand & Linkage Analysis

#### 5.1 Brand Distribution
- Count by Brand Label Name
- Visualization (bar chart)

#### 5.2 National Brand Linkage Validation
- How many Best Choice items have a National Comparison Item Code?
- How many of those linked codes actually exist as Item Codes in the data?
- What % of linked National Brand items have pricing data?
- Sample 10 linked pairs showing: BC Item, National Item, Category, both BSPs

#### 5.3 Categories with Multiple Brands
- Which categories have BOTH Best Choice AND Always Save?
- Which categories have all three brands (BC, AS, National)?
- This is critical for cross-brand elasticity analysis

---

### 6. Pricing Data Quality

#### 6.1 Price Reasonableness Checks
- Any negative prices?
- Any zero prices?
- Any extremely high prices (outliers > 3 std dev)?
- List Cost vs BSP relationship: Is List Cost always ≤ BSP?
- BSP vs SRP relationship: Is BSP always ≤ SRP?

#### 6.2 Price Consistency Across Divisions
- Per the meeting, List Cost should be SAME across divisions
- Verify this - show items where List Cost differs between divisions
- SRP CAN vary by division - show the variation range

#### 6.3 Quarter-over-Quarter Price Changes
For each price type (List Cost, BSP, City SRP):
- What % of items had a price change Q1→Q2?
- What % had a change Q2→Q3?
- What % had a change Q3→Q4?
- What % had ANY change during the year?
- Distribution of change magnitude (histogram)

---

### 7. Sales Data Quality

#### 7.1 Sales Reasonableness Checks
- Any negative sales?
- Any zero sales items (could be new/discontinued)?
- Distribution of sales values (histogram by brand)

#### 7.2 Sales vs Pricing Alignment
- For items with sales, what % have corresponding pricing?
- Calculate implied unit price ($ Sales / Billed Quantity) and compare to SRP

---

### 8. Key Categories Deep Dive

Based on the meeting transcript, these categories were specifically mentioned:
- **Coffee & Creamers** (tariff-sensitive)
- **Oils/Shortenings** ("vegetable oil moved a lot")
- **Chocolate/Baking** (Hershey's example)

For each:
- Item count by brand
- Pricing completeness
- Sales volume summary
- Any price changes observed?

---

### 9. Issues Summary Table

Create a consolidated table:
| Issue ID | Issue Description | Severity | Affected Records | Recommended Action |
|----------|------------------|----------|------------------|-------------------|
| 1 | Missing pricing data | High | ~23% of items | Clarify with AWG |
| 2 | Sheet name typos | Low | 2 sheets | Map in code |
| ... | ... | ... | ... | ... |

---

### 10. Recommendations

#### For AWG (Data Clarification Needed)
- List specific questions to ask AWG about data gaps

#### For Data Preparation
- Steps to clean and prepare data for analysis

#### For Analysis Phase
- Which analyses are feasible given data quality?
- Any analyses at risk due to data gaps?

---

### 11. Appendix

#### A. Column Reference
Full list of all columns with descriptions

#### B. Division Mapping
Correct mapping of division codes to names

#### C. Sample Data Preview
First 5 rows of each dataset

---

## Technical Requirements

### Code Quality
- Use clear variable names
- Add comments explaining logic
- Use functions for repeated operations
- Handle errors gracefully (try/except for file reading)

### Visualizations
- Use consistent color scheme
- All charts should have titles, axis labels
- Use appropriate chart types:
  - Heatmaps for completeness matrices
  - Bar charts for counts
  - Histograms for distributions
  - Box plots for outlier detection

### Output Format
- Notebook should run end-to-end without errors
- Use Markdown cells to explain findings
- Format numbers appropriately (percentages, currency)
- Use tables (DataFrame.style) for better readability

---

## Deliverable

Save the completed notebook as:
```
/mnt/user-data/outputs/AWG_Data_Quality_Report.ipynb
```

The notebook should be:
1. Fully executable (all cells run without error)
2. Well-documented with Markdown explanations
3. Include all visualizations inline
4. Conclude with clear, actionable recommendations

---

## Additional Notes

### From Meeting Transcript (Key Points)
1. **90-day cost change notification** - Price shouldn't change more than once per quarter
2. **List Cost same across divisions, SRP may vary** - Verify this
3. **20% price gap target** - BC should be ~20% below National (but we're seeing 40-60%)
4. **No tariff flag in data** - Students will need to detect changes by comparing quarters
5. **Category-level variation** - Coffee, oil, chocolate mentioned as volatile categories

### Known Issues to Document
1. ~23% of items have no pricing in KC division
2. Brand Label Name "National Brand" has trailing whitespace
3. Sales sheet names "GO" and "NO" are typos
4. Some duplicate column names (SRP UNIT QUANTITY appears twice)
