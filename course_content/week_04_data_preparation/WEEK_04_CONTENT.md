# Week 4: Data Preparation & Transformation

## Overview
**Theme:** Building the Pipeline
**Duration:** Fourth week of semester
**Deliverables:** Completed Data Preparation Notebook, Cleaned Datasets (CSVs), Transformation Documentation

---

## Learning Objectives

By the end of this week, students will be able to:
1. Transform wide-format data to long-format (and explain why)
2. Understand data granularity and its implications for analysis
3. Normalize prices between different units (case vs unit level)
4. Build reproducible data pipelines with clear documentation
5. Merge datasets from multiple sources

---

## Content to Create

### Video 1: Wide-to-Long Transformation (12 min)
**Purpose:** The most important data transformation concept - with extensive visualization

**Script Outline:**

**[INTRO - 30 sec]**
"The AWG pricing file has 229 columns. That's not a data analysis problem - it's a data shape problem. Today we learn to reshape data, and why it matters."

---

**[SECTION 1: The Problem with Wide Data - 2 min]**

**Animation:** Show wide AWG data with columns scrolling off screen

"Look at this data. Each row is a product. But pricing columns stretch forever: KC_Q1_BSP, KC_Q2_BSP, SP_Q1_BSP... 216 pricing columns."

**Problems with Wide:**
1. **Can't filter by division or quarter**
   - "Give me Q3 prices" - which columns?
   - "Compare Kansas City to Oklahoma" - manual column selection

2. **Can't aggregate properly**
   - "Average price by division" - requires knowing all column names
   - Adding a new division? Change all your code

3. **Can't merge with sales easily**
   - Sales is by division (separate sheets)
   - How do you join with 216 columns?

**Animation:** Show failed operations with red X marks

---

**[SECTION 2: What is Granularity? - 2 min]**

**Animation:** Zoom from galaxy → planet → city → person

"Granularity is the level of detail in your data. What does one row represent?"

**Wide Format Granularity:**
- One row = One product (all divisions, all quarters)
- Grain: Product

**Long Format Granularity:**
- One row = One product × One division × One quarter
- Grain: Product-Division-Quarter

**Why Granularity Matters:**
```
Wide: Product A → [KC_Q1: $5, KC_Q2: $6, SP_Q1: $4, ...]
Long: Product A, KC, Q1 → $5
      Product A, KC, Q2 → $6
      Product A, SP, Q1 → $4
```

**Animation:** Single wide row exploding into multiple long rows

"Long format has more rows, fewer columns. Each row answers ONE question: What was the price of THIS product, in THIS division, in THIS quarter?"

---

**[SECTION 3: The Melt Operation - 3 min]**

**Animation:** Step-by-step melt visualization (CORE ANIMATION)

"Pandas calls this transformation `melt`. Think of it like melting a wide ice block into a tall, thin column of water."

**Before (Wide):**
```
| Item | Category | KC_Q1_BSP | KC_Q2_BSP | SP_Q1_BSP | SP_Q2_BSP |
|------|----------|-----------|-----------|-----------|-----------|
| A    | Cereal   | 24.00     | 24.50     | 23.50     | 24.00     |
| B    | Dairy    | 18.00     | 18.00     | 17.50     | 18.00     |
```

**Animation Sequence:**
1. Highlight ID columns (Item, Category) - "These stay as-is"
2. Highlight value columns (all BSP columns) - "These will melt"
3. Show column headers becoming row values
4. Show cells becoming individual rows

**After (Long):**
```
| Item | Category | Division | Quarter | BSP   |
|------|----------|----------|---------|-------|
| A    | Cereal   | KC       | Q1      | 24.00 |
| A    | Cereal   | KC       | Q2      | 24.50 |
| A    | Cereal   | SP       | Q1      | 23.50 |
| A    | Cereal   | SP       | Q2      | 24.00 |
| B    | Dairy    | KC       | Q1      | 18.00 |
| B    | Dairy    | KC       | Q2      | 18.00 |
| B    | Dairy    | SP       | Q1      | 17.50 |
| B    | Dairy    | SP       | Q2      | 18.00 |
```

**Animation:** Row count multiplying (2 rows → 8 rows)

---

**[SECTION 4: Python Implementation - 2.5 min]**

**Animation:** Code appearing with output updating

```python
# Step 1: Identify ID columns (keep as-is)
id_cols = ['Item Code', 'Item Description', 'Category', 'Pack', 'Brand']

# Step 2: Identify value columns (to melt)
# All columns with pattern: Division_Quarter_PriceType
price_cols = [col for col in df.columns if '_Q' in col and '_BSP' in col]
print(f"Found {len(price_cols)} BSP columns to melt")
# Output: Found 36 BSP columns to melt (9 divisions × 4 quarters)

# Step 3: Melt!
long_df = pd.melt(
    df,
    id_vars=id_cols,           # Keep these as columns
    value_vars=price_cols,      # Melt these
    var_name='Division_Quarter', # New column for old headers
    value_name='BSP'            # New column for values
)

# Result: From ~4,300 rows to ~155,000 rows!
print(f"Wide: {len(df)} rows × {len(df.columns)} cols")
print(f"Long: {len(long_df)} rows × {len(long_df.columns)} cols")
```

**Animation:** Show dimension change visualization

```python
# Step 4: Parse the melted column
# 'KC_Q1_BSP' → Division='KC', Quarter='Q1'
long_df[['Division', 'Quarter', '_']] = long_df['Division_Quarter'].str.split('_', expand=True)
long_df = long_df.drop(columns=['Division_Quarter', '_'])

# Now we have clean Division and Quarter columns!
```

**Animation:** String splitting visualization

---

**[SECTION 5: When to Use Wide vs Long - 1.5 min]**

**Wide is good for:**
- Human viewing (spreadsheet-like)
- Side-by-side comparison of specific columns
- Some machine learning inputs

**Long is good for:**
- Filtering and grouping
- Aggregations across categories
- Merging with other data
- Most analysis operations
- Visualization libraries (ggplot, seaborn)

**Animation:** Two-column comparison chart

**Rule of thumb:** "If column names contain data (like 'Q1', 'Q2', 'KC', 'SP'), you probably need to melt."

---

**[OUTRO - 30 sec]**
"Wide to long is perhaps the most important transformation in data prep. Master this, and you can reshape any dataset. Next up: The critical discovery that changed everything."

---

### Video 2: The Unit Discovery (10 min) ⭐ CRITICAL
**Purpose:** Reveal the BSP/SRP unit mismatch - the most important lesson

**Script Outline:**

**[INTRO - 30 sec]**
"What I'm about to show you took hours to discover. It's subtle. It's easy to miss. And it completely changes the analysis. This is the kind of detective work that separates good analysts from great ones."

---

**[SECTION 1: The Mystery - 2 min]**

"We ran the price gap analysis. Best Choice should be 20% cheaper than National Brands."

**Animation:** Show initial results

**Initial Results:**
- Average price gap: 13.8%
- Negative gaps (BC MORE expensive): 3,005 items (9.7%)

"Wait. 10% of products have Best Choice priced HIGHER than the national brand? That doesn't make business sense."

**Animation:** Scatter plot showing many points below zero

"Something is wrong. But what?"

---

**[SECTION 2: The Investigation - 2 min]**

**Animation:** Detective magnifying glass searching

"Let's look at a specific product."

```
Product: CEREAL FROSTED FLAKES 15OZ
Pack: 12 units per case

Best Choice:
  BSP: $28.80
  SRP: $3.49

National Brand:
  BSP: $42.00
  SRP: $4.99
```

"If we calculate the price gap using BSP:
Gap = ($42.00 - $28.80) / $42.00 = 31.4%

Great! BC is 31% cheaper. But wait..."

**Animation:** Calculator showing the math

"Let's check the SRP ratio:
$3.49 / $4.99 = 70% (BC is 30% cheaper) ✓

But BSP ratio:
$28.80 / $42.00 = 69% (BC is 31% cheaper) ✓

These roughly match... OR DO THEY?"

---

**[SECTION 3: The Discovery - 2.5 min]**

**Animation:** Lightbulb moment

"Look at the numbers more carefully."

```
Pack: 12 units per case

BSP: $28.80 per CASE (12 units)
SRP: $3.49 per UNIT (1 unit)

If BSP is per case:
  Unit BSP = $28.80 / 12 = $2.40 per unit

Compare to SRP: $3.49

$3.49 > $2.40 ✓ Makes sense! (retail > wholesale)
```

**Animation:** Division animation showing case → units

"Now let's check if SRP makes sense as retail markup:"
```
Unit BSP (wholesale): $2.40
Unit SRP (retail): $3.49
Markup: ($3.49 - $2.40) / $2.40 = 45%

That's a typical grocery retail markup! ✓
```

**Animation:** Markup percentage bar filling up

**THE REVELATION:**
- **BSP is a CASE price** (wholesale, 12 units)
- **SRP is a UNIT price** (retail, 1 unit)
- **We were comparing apples to oranges!**

**Animation:** Apple and orange transforming, then both becoming apples (normalized)

---

**[SECTION 4: The Fix - 2 min]**

"To compare properly, we need everything at the SAME UNIT level."

**Normalization Formula:**
```python
# Convert case prices to unit prices
df['BSP_per_unit'] = df['BSP'] / df['Pack']
df['List_Cost_per_unit'] = df['List_Cost'] / df['Pack']

# SRP is already per unit - no change needed
```

**Animation:** Show formulas with visual division

**Before Normalization:**
| Item | Pack | BSP (case) | National BSP | Gap |
|------|------|------------|--------------|-----|
| A | 12 | $28.80 | $42.00 | 31.4% |
| B | 6 | $15.00 | $21.00 | 28.6% |

**After Normalization:**
| Item | Pack | BSP_unit | National BSP_unit | Gap |
|------|------|----------|-------------------|-----|
| A | 12 | $2.40 | $3.50 | 31.4% |
| B | 6 | $2.50 | $3.50 | 28.6% |

"The percentages might be similar, but now we're comparing unit to unit, which is correct."

---

**[SECTION 5: The Impact - 1.5 min]**

**Animation:** Before/After comparison with dramatic reveal

| Metric | Before | After |
|--------|--------|-------|
| Average Price Gap | 13.8% | **32.3%** |
| Negative Gaps | 3,005 (9.7%) | **40 (0.1%)** |

"32% average gap - well above the 20% target!"
"Only 40 genuinely problematic items, not 3,000!"

**Animation:** Histogram morphing from before to after

"The unit mismatch was hiding the truth. Best Choice IS competitively priced. We just couldn't see it with mismatched units."

---

**[OUTRO - 30 sec]**
"This discovery changed everything. Always ask: What UNIT is this number in? Don't assume. Verify. The data doesn't lie, but it can be misinterpreted."

**Animation:** "ALWAYS CHECK YOUR UNITS" appearing in bold

---

### Video 3: Data Pipeline Best Practices (8 min)
**Purpose:** Teach reproducible, documented data preparation

**Script Outline:**

**[INTRO - 30 sec]**
"You've done the hard work of cleaning data. Now, how do you make sure you can do it again? And that others can understand what you did?"

---

**[SECTION 1: Why Pipelines Matter - 1.5 min]**

**Scenario 1: The Nightmare**
"It's 2am before the presentation. You need to re-run the analysis with updated data. You open your notebook... and it's chaos."
- Cells run out of order
- Magic numbers everywhere
- Which file is the right one?
- Did I drop those rows before or after the merge?

**Animation:** Messy notebook with cells scattered, red errors

**Scenario 2: The Dream**
"The client sends updated data. You change ONE file path, click 'Run All', and everything works."
- Clear sections
- Configuration at the top
- Intermediate saves
- Documented decisions

**Animation:** Clean notebook, green checkmarks flowing down

---

**[SECTION 2: Pipeline Structure - 2.5 min]**

**The Standard Pipeline:**

```
RAW DATA → LOAD → VALIDATE → TRANSFORM → SAVE → ANALYZE
```

**Animation:** Flowchart with data flowing through stages

**Implementation:**

```python
# ============================================
# SECTION 1: CONFIGURATION
# ============================================
# All paths and parameters in ONE place
RAW_PRICING_FILE = 'data/raw/Product Details & Pricing...xlsx'
RAW_SALES_FILE = 'data/raw/Sales Data by Quarter...xlsx'
OUTPUT_DIR = 'data/processed/'
PRICING_HEADER_ROW = 2
SALES_HEADER_ROW = 1

# ============================================
# SECTION 2: LOAD RAW DATA
# ============================================
pricing_raw = pd.read_excel(RAW_PRICING_FILE, header=PRICING_HEADER_ROW)
print(f"Loaded pricing: {pricing_raw.shape}")

# ============================================
# SECTION 3: VALIDATE
# ============================================
assert len(pricing_raw) > 0, "Pricing file is empty!"
assert 'Item Code' in pricing_raw.columns, "Missing Item Code column!"

# ============================================
# SECTION 4: TRANSFORM
# ============================================
# 4a: Reshape wide to long
pricing_long = reshape_pricing(pricing_raw)

# 4b: Normalize units
pricing_long['BSP_per_unit'] = pricing_long['BSP'] / pricing_long['Pack']

# ============================================
# SECTION 5: SAVE INTERMEDIATE
# ============================================
pricing_long.to_csv(f'{OUTPUT_DIR}/pricing_long.csv', index=False)
print(f"Saved: {OUTPUT_DIR}/pricing_long.csv")
```

**Animation:** Code sections highlighting as each is discussed

---

**[SECTION 3: Key Principles - 2.5 min]**

**Principle 1: Single Source of Truth**
- Raw data is NEVER modified
- All transformations in code, not Excel
- Version control your notebooks

**Animation:** Hierarchy diagram showing raw data protected

**Principle 2: Configuration at the Top**
- File paths
- Parameters (header rows, thresholds)
- Easy to update, hard to miss

**Animation:** Config section highlighted at top of notebook

**Principle 3: Save Intermediate Outputs**
- After major transformations, save to CSV
- If step 5 fails, don't re-run steps 1-4
- Easier debugging

**Animation:** Checkpoints along pipeline

**Principle 4: Document Your Decisions**
```python
# Drop rows where Pack is missing or zero
# DECISION: These products can't be normalized (no unit conversion possible)
# IMPACT: Removes 47 rows (1.1%)
df = df[df['Pack'] > 0]
```

**Animation:** Comment example with decision/impact format

**Principle 5: Use Functions for Reusable Logic**
```python
def normalize_to_unit_price(df, price_col, pack_col):
    """Convert case-level price to unit-level price."""
    return df[price_col] / df[pack_col]
```

---

**[SECTION 4: Your Pipeline - 1 min]**

**Animation:** AWG-specific pipeline diagram

```
RAW FILES
    ↓
LOAD (pricing: header=2, sales: header=1, all sheets)
    ↓
RESHAPE (melt pricing columns)
    ↓
NORMALIZE (BSP/Pack, List Cost/Pack)
    ↓
MERGE (pricing + sales by Item Code, Division, Quarter)
    ↓
VALIDATE (check for duplicates, missing, impossible values)
    ↓
SAVE (pricing_long.csv, sales_long.csv, merged.csv)
    ↓
READY FOR ANALYSIS
```

**[OUTRO - 30 sec]**
"A good pipeline is boring. It just works, every time. Build yours this week."

---

### Video 4: Merging Datasets (8 min)
**Purpose:** Teach dataset joining with real AWG examples

**Script Outline:**

**[INTRO - 30 sec]**
"We have pricing data. We have sales data. Now we need to combine them. This is where merge - or join - operations come in."

---

**[SECTION 1: Why Merge? - 1 min]**

**Animation:** Two tables coming together

"Pricing tells us what things cost. Sales tells us how much sold. Together, we can answer: Did lower prices drive higher sales? Did cost increases affect demand?"

**The Challenge:**
- Pricing: One file, all divisions
- Sales: Nine files, one per division
- Different structures, same products

---

**[SECTION 2: Merge Concepts - 2 min]**

**Animation:** Venn diagram style merge visualization

**Types of Merges:**

**Inner Join (intersection)**
- Only rows that exist in BOTH datasets
- Safe, but might lose data

**Left Join**
- All rows from left dataset
- Matching rows from right (or NaN if no match)
- Keep all pricing, add sales where available

**Right Join**
- Opposite of left

**Outer Join (union)**
- All rows from both datasets
- Most inclusive, might have lots of NaNs

**Animation:** Each join type shown with sample tables

---

**[SECTION 3: AWG Merge Strategy - 2.5 min]**

**Step 1: Prepare Sales Data**
```python
# Sales is in 9 separate sheets, need to combine
all_sales = pd.read_excel(sales_file, sheet_name=None, header=1)

# Stack all sheets, add Division column
sales_list = []
for division, df in all_sales.items():
    df['Division'] = division
    sales_list.append(df)

sales_combined = pd.concat(sales_list, ignore_index=True)
```

**Animation:** 9 sheets stacking into one

**Step 2: Reshape Sales to Long**
```python
# Sales columns: $ SALES, $ SALES.1, $ SALES.2, $ SALES.3
# Need to melt to get Quarter as a row variable
sales_long = pd.melt(
    sales_combined,
    id_vars=['Item Code', 'Division'],
    value_vars=['$ SALES', '$ SALES.1', '$ SALES.2', '$ SALES.3'],
    var_name='Quarter_raw',
    value_name='Dollar_Sales'
)

# Map column names to quarters
quarter_map = {'$ SALES': 'Q1', '$ SALES.1': 'Q2', '$ SALES.2': 'Q3', '$ SALES.3': 'Q4'}
sales_long['Quarter'] = sales_long['Quarter_raw'].map(quarter_map)
```

**Animation:** Column names becoming row values

**Step 3: Merge Pricing + Sales**
```python
# Both datasets now have: Item Code, Division, Quarter
# Merge on these three columns
merged = pd.merge(
    pricing_long,
    sales_long,
    on=['Item Code', 'Division', 'Quarter'],
    how='left'  # Keep all pricing, add sales where available
)

# Check the result
print(f"Pricing rows: {len(pricing_long)}")
print(f"Sales rows: {len(sales_long)}")
print(f"Merged rows: {len(merged)}")
print(f"Missing sales: {merged['Dollar_Sales'].isnull().sum()}")
```

**Animation:** Two tables merging with matching keys highlighted

---

**[SECTION 4: Handling Merge Issues - 2 min]**

**Issue 1: Non-matching Keys**
```python
# Find pricing items with no sales
no_sales = pricing_long[~pricing_long['Item Code'].isin(sales_long['Item Code'])]
print(f"Products with no sales data: {no_sales['Item Code'].nunique()}")
```

**Issue 2: Duplicates After Merge**
```python
# Check for unexpected row multiplication
before = len(pricing_long)
after = len(merged)
if after > before:
    print(f"WARNING: Row multiplication! {before} → {after}")
    # Usually means duplicates in one of the datasets
```

**Animation:** Warning sign with row count check

**Issue 3: Division Name Mismatches**
```python
# Sales uses GO instead of NA, NO instead of NE
# Fix BEFORE merging
division_fix = {'GO': 'NA', 'NO': 'NE'}
sales_long['Division'] = sales_long['Division'].replace(division_fix)
```

**Animation:** String replacement visualization

---

**[OUTRO - 30 sec]**
"Merging is where data comes alive. With pricing and sales together, you can finally answer the business questions. Your merged dataset is the foundation for everything that follows."

---

## Notebooks to Create

### `week04_data_preparation_starter.ipynb`
Complete data preparation notebook with TODO sections

**See separate file for full notebook content (too long to include inline)**

Key sections:
1. Configuration
2. Load Raw Data
3. Explore Structure
4. Reshape Pricing (Wide to Long)
5. Normalize Unit Prices ← Critical!
6. Load and Combine Sales
7. Merge Pricing + Sales
8. Validate Final Dataset
9. Save Outputs

---

## Animation Production Notes - DETAILED

### Video 1: Wide-to-Long (Manim)

**Animation 1: Wide Data Scroll**
```python
class WideDataScroll(Scene):
    def construct(self):
        # Create wide table header
        cols = ["Item", "Cat", "KC_Q1", "KC_Q2", "SP_Q1", "SP_Q2", "OK_Q1", "..."]
        table = self.create_table(cols, rows=3)

        # Animate scrolling to show many columns
        self.play(table.animate.shift(LEFT * 10), run_time=5)

        # Show "229 columns!" text
        text = Text("229 columns!", color=RED).scale(2)
        self.play(Write(text))
```

**Animation 2: Granularity Zoom**
```python
class GranularityZoom(Scene):
    def construct(self):
        # Wide format: one row = entire product
        wide_row = self.create_row("Product A: [KC_Q1, KC_Q2, SP_Q1, SP_Q2, ...]")
        self.play(Create(wide_row))

        # Explode into multiple rows
        long_rows = VGroup(*[
            self.create_row(f"Product A, {div}, {qtr}")
            for div in ["KC", "SP", "OK"]
            for qtr in ["Q1", "Q2"]
        ])

        self.play(
            wide_row.animate.scale(0.5).to_edge(UP),
            *[Create(row) for row in long_rows]
        )
```

**Animation 3: The Melt (MAIN ANIMATION)**
```python
class MeltAnimation(Scene):
    def construct(self):
        # Before table (wide)
        before_data = [
            ["Item", "Cat", "KC_Q1", "KC_Q2", "SP_Q1"],
            ["A", "Cereal", "24.00", "24.50", "23.50"],
            ["B", "Dairy", "18.00", "18.00", "17.50"],
        ]
        before_table = self.create_table(before_data)

        # Highlight ID columns (stay)
        id_highlight = SurroundingRectangle(before_table.get_columns()[:2], color=BLUE)
        self.play(Create(id_highlight))
        self.play(Write(Text("These stay as columns").next_to(id_highlight, UP)))

        # Highlight value columns (melt)
        value_highlight = SurroundingRectangle(before_table.get_columns()[2:], color=ORANGE)
        self.play(Create(value_highlight))
        self.play(Write(Text("These become ROWS").next_to(value_highlight, UP)))

        # THE MELT
        # Animate column headers becoming cell values
        # Animate data cells moving to new positions
        # Show row count increasing: 2 → 6

        # After table (long)
        after_data = [
            ["Item", "Cat", "Div", "Qtr", "BSP"],
            ["A", "Cereal", "KC", "Q1", "24.00"],
            ["A", "Cereal", "KC", "Q2", "24.50"],
            ["A", "Cereal", "SP", "Q1", "23.50"],
            ["B", "Dairy", "KC", "Q1", "18.00"],
            ["B", "Dairy", "KC", "Q2", "18.00"],
            ["B", "Dairy", "SP", "Q1", "17.50"],
        ]

        # Transition animation
        self.play(Transform(before_table, after_table))
```

---

### Video 2: Unit Discovery (Manim)

**Animation 1: The Mystery Scatter**
```python
class MysteryScatter(Scene):
    def construct(self):
        # Create axes for price gap
        axes = Axes(
            x_range=[0, 100, 10],
            y_range=[-50, 50, 10],
            axis_config={"include_numbers": True}
        )
        axes.add_labels(x_label="Product", y_label="Price Gap %")

        # Plot points, many below zero (red)
        # Target line at 20%
        target_line = axes.get_horizontal_line(axes.c2p(100, 20), color=GREEN)
        zero_line = axes.get_horizontal_line(axes.c2p(100, 0), color=YELLOW)

        # Highlight negative region
        negative_region = axes.get_area(
            axes.plot(lambda x: 0),
            x_range=[0, 100],
            bounded_graph=axes.plot(lambda x: -50),
            color=RED,
            opacity=0.3
        )

        # "9.7% of products!" label in red region
```

**Animation 2: The Case vs Unit Reveal**
```python
class CaseUnitReveal(Scene):
    def construct(self):
        # Product info
        product = Text("FROSTED FLAKES 15OZ\nPack: 12 units per case")

        # Show BSP as a CASE (12 boxes)
        case_visual = VGroup(*[
            self.create_box() for _ in range(12)
        ]).arrange_in_grid(3, 4)
        case_label = Text("BSP: $28.80\n(12 units)").next_to(case_visual, DOWN)

        # Show SRP as ONE box
        unit_visual = self.create_box().scale(1.5)
        unit_label = Text("SRP: $3.49\n(1 unit)").next_to(unit_visual, DOWN)

        # Animate comparison - they look equal but aren't!

        # Now show the DIVISION
        # 12 boxes → divide into 12 → get unit price $2.40
        division_animation = AnimationGroup(
            case_visual.animate.arrange_in_grid(1, 12),
            Transform(case_label, Text("$28.80 ÷ 12 = $2.40/unit"))
        )

        # NOW compare: $2.40 vs $3.49 - makes sense!
```

**Animation 3: Before/After Histogram**
```python
class BeforeAfterHistogram(Scene):
    def construct(self):
        # Before histogram - wide distribution, many negative
        before_data = [...]  # Actual price gap data before normalization
        before_hist = self.create_histogram(before_data, title="Before Normalization")

        # Key stats on before
        before_stats = VGroup(
            Text("Avg: 13.8%"),
            Text("Negative: 3,005 (9.7%)", color=RED)
        ).arrange(DOWN).next_to(before_hist, RIGHT)

        # Transition
        self.wait(2)

        # After histogram - shifted right, almost no negative
        after_data = [...]  # Actual price gap data after normalization
        after_hist = self.create_histogram(after_data, title="After Normalization")

        # Morph animation
        self.play(Transform(before_hist, after_hist))

        # Key stats on after
        after_stats = VGroup(
            Text("Avg: 32.3%", color=GREEN),
            Text("Negative: 40 (0.1%)", color=GREEN)
        )
```

---

### Video 4: Merging (Manim)

**Animation: Keys Matching**
```python
class MergeAnimation(Scene):
    def construct(self):
        # Left table (Pricing)
        pricing = self.create_table([
            ["ItemCode", "Div", "Qtr", "BSP"],
            ["A", "KC", "Q1", "24.00"],
            ["A", "KC", "Q2", "24.50"],
            ["B", "KC", "Q1", "18.00"],
        ])

        # Right table (Sales)
        sales = self.create_table([
            ["ItemCode", "Div", "Qtr", "Sales"],
            ["A", "KC", "Q1", "5000"],
            ["A", "KC", "Q2", "4800"],
            ["C", "KC", "Q1", "3000"],  # No match!
        ])

        # Position side by side
        pricing.to_edge(LEFT)
        sales.to_edge(RIGHT)

        # Animate matching keys with lines
        # A-KC-Q1 matches → draw line, turn green
        # A-KC-Q2 matches → draw line, turn green
        # B-KC-Q1 no match in sales → stay alone
        # C-KC-Q1 no match in pricing → excluded (inner join)

        # Show resulting merged table
        merged = self.create_table([
            ["ItemCode", "Div", "Qtr", "BSP", "Sales"],
            ["A", "KC", "Q1", "24.00", "5000"],
            ["A", "KC", "Q2", "24.50", "4800"],
            ["B", "KC", "Q1", "18.00", "NaN"],  # Left join keeps this
        ])
```

---

## Production Checklist

- [ ] Video 1: Wide-to-Long
  - [ ] Script finalized
  - [ ] Wide data scroll animation
  - [ ] Granularity zoom animation
  - [ ] Melt animation (main)
  - [ ] Python code examples
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 2: Unit Discovery ⭐
  - [ ] Script finalized
  - [ ] Mystery scatter plot
  - [ ] Case vs unit reveal (main)
  - [ ] Before/after histogram morph
  - [ ] "Check Your Units" conclusion
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 3: Pipeline Best Practices
  - [ ] Script finalized
  - [ ] Pipeline flowchart animation
  - [ ] Code section highlights
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 4: Merging
  - [ ] Script finalized
  - [ ] Merge types Venn diagrams
  - [ ] Keys matching animation
  - [ ] AWG-specific examples
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Notebooks
  - [ ] Data preparation starter notebook
  - [ ] Tested with actual AWG data
  - [ ] Outputs saved correctly

- [ ] Manim Scenes
  - [ ] MeltAnimation class
  - [ ] CaseUnitReveal class
  - [ ] BeforeAfterHistogram class
  - [ ] MergeAnimation class

---

## Notes

Week 4 is THE critical week. The unit discovery is the signature lesson - it shows:
1. Real data has hidden assumptions
2. Domain knowledge matters (what IS a BSP?)
3. Always verify units before comparing
4. One insight can change everything

The Manim animations for this week should be polished and reusable for future courses.
