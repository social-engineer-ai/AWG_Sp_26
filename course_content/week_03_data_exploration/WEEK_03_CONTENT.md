# Week 3: Data Exploration & Quality Assessment

## Overview
**Theme:** Understanding the Data
**Duration:** Third week of semester
**Deliverables:** Data Quality Report, Data Dictionary Draft

---

## Learning Objectives

By the end of this week, students will be able to:
1. Load and navigate complex Excel files with multiple sheets and headers
2. Perform systematic data quality assessment (completeness, validity, consistency)
3. Document data structure and create a data dictionary
4. Identify potential data issues before they cause analysis problems
5. Use pandas for exploratory data analysis

---

## Content to Create

### Video 1: Data Files Walkthrough (10 min)
**Purpose:** Tour the actual AWG data files so students know what they're working with

**Script Outline:**

**[INTRO - 30 sec]**
"This week, we finally meet the data. AWG has provided two Excel files - one for pricing, one for sales. Let's understand their structure before we write any code."

**[SECTION 1: The Pricing File - 3 min]**
*File: `Product Details & Pricing by quarter by division 12.19.25.xlsx`*

**Animation:** Excel file opening, zoom to different areas

"This is a wide, complex file. Let's break it down."

**Structure Overview:**
- Header row: Row 3 (not row 1!)
- Products: ~4,319 rows
- Columns: 229 total

**Column Groups:**
1. **Product Identifiers (cols 1-13)**
   - Item Code (unique identifier)
   - Item Description
   - Category, Subcategory
   - Pack (units per case) ← Critical!
   - Brand (BC, AS, NB)
   - National_Item_Code (links BC to NB equivalent)

**Animation:** Highlight column groups with color coding

2. **Pricing by Division × Quarter (cols 14-229)**
   - 9 divisions × 4 quarters × 6 price fields = 216 columns
   - Pattern: `Division_Quarter_PriceType`
   - Example: `KC_Q1_List Cost`, `KC_Q1_BSP`, `KC_Q1_SRP`

**Price Fields:**
- **List Cost** - What AWG pays suppliers
- **BSP** - Base Selling Price (AWG to stores) ← CASE level!
- **SRP** - Suggested Retail Price (stores to consumers) ← UNIT level!
- **Deal**, **TPR**, **Retail** - Promotional prices

**Animation:** Zoom to column headers showing the pattern

**[SECTION 2: The Sales File - 2.5 min]**
*File: `Sales Data by Quarter - U of I Project 12.19.25.xlsx`*

**Structure Overview:**
- 9 sheets (one per division)
- Header row: Row 2
- Sheet names: KC, SP, OK, GO, GC, NO, GL, HN, UM
  - **Note:** GO should be NA, NO should be NE (typos in source)

**Columns per sheet:**
- Item Code
- $ SALES (Q1), $ SALES.1 (Q2), $ SALES.2 (Q3), $ SALES.3 (Q4)
- UNITS (Q1), UNITS.1 (Q2), UNITS.2 (Q3), UNITS.3 (Q4)

**Animation:** Show multiple sheet tabs, then column structure

**[SECTION 3: Key Relationships - 1.5 min]**

**Animation:** Entity-relationship diagram

```
Product (Item Code) ──┬── Pricing (by Division, Quarter)
                      │
                      └── Sales (by Division, Quarter)

Best Choice Item ────────── National_Item_Code ────── National Brand Item
```

"The magic is in `National_Item_Code`. It tells us which Best Choice product competes with which national brand. This enables all our price gap analysis."

**[SECTION 4: Why This Matters - 1 min]**
"Before you touch the data, you need to understand:
1. Where is the header row?
2. What does each column mean?
3. How do files connect?
4. What are the potential gotchas?"

"The biggest gotcha? We'll reveal it next week. For now, explore and document."

**[OUTRO - 30 sec]**
"Your mission: Open these files, explore them, and document what you find. Create a data dictionary. Note anything that looks wrong. This detective work is essential."

---

### Video 2: Data Quality Checklist (7 min)
**Purpose:** Systematic approach to data quality assessment

**Script Outline:**

**[INTRO - 30 sec]**
"Clean data is a myth. Real data has problems. Your job is to find them before they find you."

**[SECTION 1: The 5 Dimensions of Data Quality - 2 min]**

**Animation:** 5 pillars appearing one by one

1. **Completeness** - Are there missing values?
   - How many? Which columns? Random or systematic?

2. **Validity** - Do values make sense?
   - Negative prices? Future dates? Invalid codes?

3. **Accuracy** - Are values correct?
   - Harder to check without ground truth

4. **Consistency** - Do related values agree?
   - Does List Cost + Margin ≈ BSP?
   - Is the same product priced consistently?

5. **Uniqueness** - Are there duplicates?
   - Duplicate Item Codes? Duplicate rows?

**[SECTION 2: Systematic Exploration - 2.5 min]**

**For Each Column, Ask:**

**Animation:** Checklist appearing as discussed

```
□ What is the data type? (numeric, text, date)
□ How many missing values?
□ What are min, max, mean, median?
□ What are the unique values (for categorical)?
□ Does the distribution look reasonable?
□ Are there obvious outliers?
```

**Pandas Commands:**
```python
df.info()           # Data types, non-null counts
df.describe()       # Numeric summary
df.isnull().sum()   # Missing by column
df['col'].unique()  # Unique values
df['col'].value_counts()  # Frequency distribution
```

**Animation:** Code appearing with sample output

**[SECTION 3: AWG-Specific Checks - 1.5 min]**

**Price Sanity:**
- List Cost < BSP < SRP (usually)
- All prices positive
- No extreme values (>$1000 for grocery items?)

**Product Integrity:**
- Every Item Code should be unique
- Every BC item with National_Item_Code should match a real NB item
- Pack sizes should be reasonable (1-100 units)

**Division Consistency:**
- Should List Cost be the same across divisions? (Supplier price)
- Should BSP vary? (AWG's regional pricing)

**[SECTION 4: Documenting Findings - 1 min]**

"Don't just find issues - document them."

**Animation:** Sample issue log

| Issue | Column(s) | Count | Severity | Notes |
|-------|-----------|-------|----------|-------|
| Missing SRP | *_SRP | 234 | Medium | Mostly AS products |
| Negative gap | Price_Gap | 3005 | High | Investigate! |

**[OUTRO - 30 sec]**
"By the end of this week, you should have a comprehensive data quality report. Every issue you find now is a problem you won't have later."

---

### Video 3: Colab/Jupyter Basics (8 min)
**Purpose:** For students new to notebooks - how to use Colab effectively

**Script Outline:**

**[INTRO - 30 sec]**
"If you've never used Jupyter notebooks, this video is for you. If you're experienced, feel free to skip ahead."

**[SECTION 1: What is a Notebook? - 1 min]**
- Interactive document: code + output + text
- Different from scripts: See results immediately
- Great for exploration and documentation

**Animation:** Compare script file vs notebook

**[SECTION 2: Cell Types - 1.5 min]**
- **Code cells:** Python code, run with Shift+Enter
- **Text cells:** Markdown for documentation
- Can mix freely: explain, then code, then explain results

**Animation:** Creating different cell types

**[SECTION 3: Running Code - 2 min]**
- Shift+Enter: Run cell, move to next
- Ctrl+Enter: Run cell, stay in place
- Runtime > Run all: Run entire notebook
- Order matters! Variables persist between cells
- Restart runtime if things get weird

**Animation:** Show execution flow with cell numbers

**[SECTION 4: Common Patterns - 2 min]**

**Pattern 1: Import at the top**
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

**Pattern 2: Load data once**
```python
df = pd.read_excel('file.xlsx', header=2)
```

**Pattern 3: Explore incrementally**
```python
df.head()
df.info()
df.describe()
```

**Pattern 4: Document as you go**
```markdown
## Finding 1: Missing Values
After exploring the data, I found 234 missing SRP values...
```

**[SECTION 5: Colab-Specific Tips - 1 min]**
- Mount Google Drive for data access
- Use `!pip install` for packages
- Enable GPU if needed (Runtime > Change runtime type)
- Auto-save is your friend
- Download as .ipynb or .py

**[OUTRO - 30 sec]**
"Notebooks are your thinking tool. Use them to explore, document, and share. Now let's put this into practice."

---

### Video 4: Common Pandas Operations (10 min)
**Purpose:** Essential pandas for data exploration

**Script Outline:**

**[INTRO - 30 sec]**
"Pandas is your data manipulation powerhouse. Here are the operations you'll use constantly."

**[SECTION 1: Loading Data - 2 min]**

**Animation:** Code with actual AWG file examples

```python
# Basic Excel load
df = pd.read_excel('Product Details & Pricing...xlsx')

# With header row specification
df = pd.read_excel('Product Details & Pricing...xlsx', header=2)

# Specific sheet
sales_kc = pd.read_excel('Sales Data...xlsx', sheet_name='KC', header=1)

# All sheets at once
all_sales = pd.read_excel('Sales Data...xlsx', sheet_name=None, header=1)
# Returns dict: {'KC': df1, 'SP': df2, ...}
```

**[SECTION 2: First Look - 2 min]**

```python
# Dimensions
df.shape  # (rows, columns)

# Column names
df.columns.tolist()

# First/last rows
df.head(10)
df.tail(5)

# Data types and nulls
df.info()

# Numeric summary
df.describe()

# Specific column
df['Column_Name'].describe()
df['Column_Name'].unique()
df['Column_Name'].value_counts()
```

**Animation:** Show output for each command using actual AWG data

**[SECTION 3: Selecting Data - 2 min]**

```python
# Single column
df['Item_Code']

# Multiple columns
df[['Item_Code', 'Item_Description', 'Category']]

# Rows by condition
df[df['Brand'] == 'BC']  # Only Best Choice
df[df['KC_Q1_BSP'] > 100]  # High-priced items

# Multiple conditions
df[(df['Brand'] == 'BC') & (df['Category'] == 'Cereal')]

# Specific rows and columns
df.loc[0:10, ['Item_Code', 'Category']]
df.iloc[0:10, 0:5]  # By position
```

**[SECTION 4: Missing Values - 1.5 min]**

```python
# Count missing per column
df.isnull().sum()

# Percent missing
df.isnull().sum() / len(df) * 100

# Rows with any missing
df[df.isnull().any(axis=1)]

# Drop missing (careful!)
df.dropna()  # All rows with any null
df.dropna(subset=['Important_Column'])  # Only if specific col is null

# Fill missing
df.fillna(0)
df['col'].fillna(df['col'].mean())
```

**[SECTION 5: Basic Aggregations - 2 min]**

```python
# Group and aggregate
df.groupby('Category')['KC_Q1_BSP'].mean()

# Multiple aggregations
df.groupby('Brand').agg({
    'KC_Q1_BSP': ['mean', 'std', 'count'],
    'KC_Q1_SRP': ['mean', 'std']
})

# Cross-tabulation
pd.crosstab(df['Brand'], df['Category'])

# Pivot table
df.pivot_table(
    values='KC_Q1_BSP',
    index='Category',
    columns='Brand',
    aggfunc='mean'
)
```

**[OUTRO - 30 sec]**
"These operations cover 80% of what you'll need for exploration. Practice them on the AWG data this week."

---

## Notebooks to Create

### `week03_data_exploration_starter.ipynb`
Starter notebook guiding students through systematic exploration

**Structure:**
```python
# === SECTION 1: SETUP ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Mount Google Drive (if using Colab)
# from google.colab import drive
# drive.mount('/content/drive')

# === SECTION 2: LOAD PRICING DATA ===
# TODO: Update path to your data location
pricing_file = 'Product Details & Pricing by quarter by division 12.19.25.xlsx'

# Note: Header is on row 3 (0-indexed: header=2)
pricing_df = pd.read_excel(pricing_file, header=2)

print(f"Pricing data shape: {pricing_df.shape}")
print(f"Columns: {len(pricing_df.columns)}")

# === SECTION 3: EXPLORE PRICING STRUCTURE ===
# Your task: Understand the column structure

# First 15 columns (product info)
print("Product columns:")
print(pricing_df.columns[:15].tolist())

# Sample of pricing columns
print("\nSample pricing columns:")
print(pricing_df.columns[15:30].tolist())

# TODO: Identify the pattern in column names
# What are the divisions? What are the quarters? What are the price types?

# === SECTION 4: LOAD SALES DATA ===
sales_file = 'Sales Data by Quarter - U of I Project 12.19.25.xlsx'

# Load all sheets
all_sales = pd.read_excel(sales_file, sheet_name=None, header=1)

print(f"Number of sheets: {len(all_sales)}")
print(f"Sheet names: {list(all_sales.keys())}")

# Explore one sheet
kc_sales = all_sales['KC']
print(f"\nKC Sales shape: {kc_sales.shape}")
print(f"KC Sales columns: {kc_sales.columns.tolist()}")

# === SECTION 5: DATA QUALITY CHECKS ===

# Check 1: Missing values in pricing
print("Missing values in pricing data:")
missing_pct = pricing_df.isnull().sum() / len(pricing_df) * 100
print(missing_pct[missing_pct > 0].sort_values(ascending=False).head(20))

# Check 2: Product column completeness
product_cols = ['Item Code', 'Item Description', 'Category', 'Pack', 'Brand']
for col in product_cols:
    # Find the actual column name (may vary)
    matching = [c for c in pricing_df.columns if col.lower() in c.lower()]
    if matching:
        actual_col = matching[0]
        missing = pricing_df[actual_col].isnull().sum()
        print(f"{actual_col}: {missing} missing ({missing/len(pricing_df)*100:.1f}%)")

# Check 3: Unique products
# TODO: Find the Item Code column and check uniqueness
# item_code_col = ???
# print(f"Unique items: {pricing_df[item_code_col].nunique()}")
# print(f"Duplicate items: {pricing_df[item_code_col].duplicated().sum()}")

# Check 4: Brand distribution
# TODO: Find Brand column and show value counts

# Check 5: Price sanity
# TODO: Check if prices are positive, reasonable ranges

# === SECTION 6: YOUR EXPLORATION ===
# Add your own exploration below

# What patterns do you notice?
# What seems unusual?
# What questions do you have for the client?

# === SECTION 7: DOCUMENT YOUR FINDINGS ===
"""
## Data Quality Report - Draft

### Pricing File
- Rows: ???
- Columns: ???
- Key findings:
  1.
  2.
  3.

### Sales File
- Sheets: ???
- Key findings:
  1.
  2.
  3.

### Questions for Client
1.
2.
3.

### Issues Found
| Issue | Severity | Notes |
|-------|----------|-------|
|       |          |       |
"""
```

---

## Documents to Create

### Data Dictionary Template
**File:** `data_dictionary_template.md`

```markdown
# AWG Data Dictionary

## Pricing File: Product Details & Pricing...

### Product Information Columns

| Column Name | Data Type | Description | Example | Notes |
|-------------|-----------|-------------|---------|-------|
| Item Code | String | Unique product identifier | "123456" | Primary key |
| Item Description | String | Product name | "CEREAL FROSTED FLAKES 15OZ" | |
| Category | String | Product category | "Cereal" | |
| Subcategory | String | Product subcategory | "Cold Cereal" | |
| Pack | Integer | Units per case | 12 | Critical for unit price calc |
| Brand | String | Brand identifier | "BC", "AS", "NB" | BC=Best Choice, AS=Always Save, NB=National Brand |
| National_Item_Code | String | Linked national brand item | "789012" | For BC items only |

### Pricing Columns (Pattern: Division_Quarter_PriceType)

| Price Type | Description | Level | Example |
|------------|-------------|-------|---------|
| List Cost | Supplier cost to AWG | Case | $24.00 |
| BSP | Base Selling Price (AWG to stores) | Case | $28.00 |
| SRP | Suggested Retail Price | Unit | $3.49 |
| Deal | Deal price | ? | |
| TPR | Temporary Price Reduction | ? | |
| Retail | Retail price | ? | |

### Divisions
| Code | Full Name | Region |
|------|-----------|--------|
| KC | Kansas City | Central |
| SP | Springfield | ? |
| OK | Oklahoma | ? |
| NA | ? | ? |
| GC | ? | ? |
| NE | ? | ? |
| GL | ? | ? |
| HN | ? | ? |
| UM | ? | ? |

---

## Sales File: Sales Data by Quarter...

### Columns

| Column Name | Data Type | Description | Example |
|-------------|-----------|-------------|---------|
| Item Code | String | Product identifier | "123456" |
| $ SALES | Float | Q1 dollar sales | 15234.50 |
| $ SALES.1 | Float | Q2 dollar sales | |
| $ SALES.2 | Float | Q3 dollar sales | |
| $ SALES.3 | Float | Q4 dollar sales | |
| UNITS | Integer | Q1 unit sales | 4521 |
| UNITS.1 | Integer | Q2 unit sales | |
| UNITS.2 | Integer | Q3 unit sales | |
| UNITS.3 | Integer | Q4 unit sales | |

### Sheets
One sheet per division (KC, SP, OK, GO*, GC, NO*, GL, HN, UM)
*Note: GO should be NA, NO should be NE (verify with client)
```

---

## Animation Production Notes

### Video 1: Data Files Walkthrough

**Key Animations (Manim recommended):**

1. **Excel Structure Reveal**
   - Start with blank grid
   - Highlight row 3 as header (not row 1)
   - Animate column count: 1... 50... 100... 229!
   - Show column groupings with color bands

2. **Column Pattern Animation**
   - Show formula: Division × Quarter × PriceType = 9 × 4 × 6 = 216
   - Animate expansion: KC_Q1_BSP → [KC, SP, OK...] × [Q1, Q2, Q3, Q4] × [List Cost, BSP, SRP...]
   - Color code: Divisions (blue), Quarters (green), Price Types (orange)

3. **Multi-Sheet Sales Visualization**
   - 9 tabs appearing
   - Same structure replicating across tabs
   - Highlight sheet name typos (GO → NA, NO → NE)

4. **Entity Relationship Diagram**
   - Product node in center
   - Pricing node connecting with "by Division, Quarter" label
   - Sales node connecting with "by Division, Quarter" label
   - BC-to-NB link animated

**Manim Code Concept:**
```python
class ExcelStructure(Scene):
    def construct(self):
        # Create grid representing Excel
        grid = self.create_grid(10, 15)
        self.play(Create(grid))

        # Highlight header row
        header_highlight = Rectangle(
            width=14, height=0.5, color=YELLOW
        ).move_to(grid[2])  # Row 3
        self.play(Create(header_highlight))

        # Show column count expanding
        counter = Integer(0).to_corner(UR)
        self.play(
            ChangeDecimalToValue(counter, 229),
            run_time=3
        )
```

### Video 2: Data Quality Checklist

**Key Animations:**

1. **Five Pillars**
   - 5 columns rising from bottom
   - Labels appearing: Completeness, Validity, Accuracy, Consistency, Uniqueness
   - Icons on each pillar

2. **Missing Value Heatmap**
   - Grid of cells
   - Missing values highlighted red
   - Pattern emerging (systematic vs random)

3. **Price Sanity Check**
   - Number line
   - List Cost < BSP < SRP shown as ranges
   - Anomaly (negative or inverted) flashing red

### Video 4: Pandas Operations

**Key Animations:**

1. **Code → Output Flow**
   - Left side: Code appearing line by line
   - Right side: DataFrame/output updating
   - Arrow showing transformation

2. **GroupBy Visualization**
   - Rows shuffling into groups
   - Aggregate values appearing above each group
   - Final summary table forming

**Screenshots to Capture:**
- Actual AWG pricing file header row
- Actual AWG sales file structure
- Sample output from each pandas command

---

## Production Checklist

- [ ] Video 1: Data Files Walkthrough
  - [ ] Script finalized
  - [ ] Excel structure animation (Manim)
  - [ ] Column pattern animation
  - [ ] ER diagram
  - [ ] Screen captures of actual files
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 2: Data Quality Checklist
  - [ ] Script finalized
  - [ ] Five pillars animation
  - [ ] Missing value visualization
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 3: Colab Basics
  - [ ] Script finalized
  - [ ] Screen recordings
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 4: Pandas Operations
  - [ ] Script finalized
  - [ ] Code/output animations
  - [ ] AWG-specific examples
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Notebooks
  - [ ] Exploration starter notebook
  - [ ] Tested with actual AWG data

- [ ] Documents
  - [ ] Data dictionary template

---

## Notes

Week 3 is where students first encounter real data complexity. Key messages:
1. Real data is messy - that's normal
2. Understanding structure before coding saves time
3. Document everything - future you will thank present you
4. The biggest issues hide in plain sight (foreshadow unit mismatch)

The goal is systematic exploration, not rushing to analysis.
