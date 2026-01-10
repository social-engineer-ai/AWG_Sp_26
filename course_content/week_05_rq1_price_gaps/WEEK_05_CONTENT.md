# Week 5: Research Question 1 - Price Gap Analysis

## Overview
**Theme:** Are AWG Brands Competitively Priced?
**Duration:** Fifth week of semester
**Deliverables:** RQ1 Analysis Notebook, Price Gap Summary by Category, Visualizations

---

## Learning Objectives

By the end of this week, students will be able to:
1. Calculate and interpret price gaps between private label and national brands
2. Aggregate analysis across products, categories, divisions, and time
3. Assess performance against a business target (20% gap)
4. Create effective visualizations for price comparisons
5. Identify outliers and anomalies requiring further investigation

---

## Research Question

**RQ1: Are AWG private label brands (Best Choice, Always Save) priced competitively against national brand equivalents?**

**Sub-questions:**
- What is the average price gap? Does it meet the 20% target?
- How does the gap vary by product category?
- How does the gap vary by division (geography)?
- Has the gap changed over the 4 quarters of data?
- Which products have negative gaps (BC more expensive than NB)?

---

## Content to Create

### Video 1: Price Gap Methodology (10 min)
**Purpose:** Teach the math and logic of price gap calculation

**Script Outline:**

**[INTRO - 30 sec]**
"AWG wants Best Choice to be about 20% cheaper than national brands. But is it? This week, we answer that question with data."

---

**[SECTION 1: What is a Price Gap? - 2 min]**

**Definition:**
"The price gap measures how much cheaper (or more expensive) one product is compared to another."

**Formula:**
```
Price Gap % = (National Brand Price - Best Choice Price) / National Brand Price × 100
```

**Animation:** Number line showing two prices, gap between them

**Example:**
```
National Brand Cereal: $4.99
Best Choice Cereal: $3.99

Gap = ($4.99 - $3.99) / $4.99 × 100 = 20.0%
```

**Interpretation:**
- Positive gap: BC is cheaper than NB (good!)
- Negative gap: BC is more expensive than NB (investigate!)
- Gap = 20%: BC is exactly 20% cheaper (target!)

**Animation:** Gauge showing gap with green zone at 20%+

---

**[SECTION 2: Which Price to Use? - 2 min]**

**Available Prices:**
- List Cost (supplier to AWG)
- BSP (AWG to stores) - wholesale
- SRP (stores to consumers) - retail

**For Price Gap Analysis:**
"We use **SRP** - the price consumers actually see and compare."

**Why SRP?**
- Consumers compare shelf prices
- This is the competitive battleground
- BSP matters to retailers, but SRP matters to shoppers

**Animation:** Supply chain showing where each price applies

**Important Reminder:**
"Remember Week 4: SRP is already per-unit. No normalization needed for SRP."

---

**[SECTION 3: Linking Products - 2 min]**

**The Challenge:**
"To compare Best Choice cereal to National Brand cereal, we need to know which products are equivalent."

**The Solution: National_Item_Code**
```
Best Choice Item Code: 123456
National_Item_Code: 789012 → Links to National Brand equivalent
```

**Animation:** Two product cards connecting via link

**The Join:**
```python
# Get Best Choice products with their national brand links
bc_products = df[df['Brand'] == 'BC'][['Item Code', 'National_Item_Code', 'SRP', ...]]

# Get National Brand products
nb_products = df[df['Brand'] == 'NB'][['Item Code', 'SRP', ...]]

# Join BC to NB using the link
comparison = bc_products.merge(
    nb_products,
    left_on='National_Item_Code',
    right_on='Item Code',
    suffixes=('_BC', '_NB')
)
```

**Animation:** Tables merging on key

---

**[SECTION 4: Calculating the Gap - 2 min]**

**Animation:** Code with live output

```python
# Calculate price gap for each matched pair
comparison['Price_Gap_Pct'] = (
    (comparison['SRP_NB'] - comparison['SRP_BC']) / comparison['SRP_NB'] * 100
)

# Summary statistics
print(f"Average Gap: {comparison['Price_Gap_Pct'].mean():.1f}%")
print(f"Median Gap: {comparison['Price_Gap_Pct'].median():.1f}%")
print(f"Min Gap: {comparison['Price_Gap_Pct'].min():.1f}%")
print(f"Max Gap: {comparison['Price_Gap_Pct'].max():.1f}%")

# How many meet the 20% target?
meets_target = (comparison['Price_Gap_Pct'] >= 20).mean() * 100
print(f"Products meeting 20% target: {meets_target:.1f}%")
```

**Animation:** Statistics appearing with visual bars

---

**[SECTION 5: Aggregating Results - 1.5 min]**

**By Category:**
```python
category_gaps = comparison.groupby('Category')['Price_Gap_Pct'].agg(['mean', 'median', 'count'])
category_gaps.sort_values('mean', ascending=False)
```

**By Division:**
```python
division_gaps = comparison.groupby('Division')['Price_Gap_Pct'].mean()
```

**By Quarter:**
```python
quarter_gaps = comparison.groupby('Quarter')['Price_Gap_Pct'].mean()
```

**Animation:** Pivot table appearing with aggregated results

---

**[OUTRO - 30 sec]**
"The price gap analysis is your first business answer. Is Best Choice competitive? The data will tell you."

---

### Video 2: Linking BC to National Brands (7 min)
**Purpose:** Deep dive into the product matching process

**Script Outline:**

**[INTRO - 30 sec]**
"Not every Best Choice product has a national brand equivalent. Understanding the linkage is critical for accurate analysis."

---

**[SECTION 1: The Link Column - 1.5 min]**

**Animation:** Product table with National_Item_Code highlighted

```
| Item Code | Description | Brand | National_Item_Code |
|-----------|-------------|-------|-------------------|
| 100001 | BC CORN FLAKES 18OZ | BC | 200001 |
| 100002 | BC FROSTED FLAKES 15OZ | BC | 200002 |
| 100003 | AS CORN FLAKES 18OZ | AS | (empty) |
| 200001 | KELLOGGS CORN FLAKES 18OZ | NB | (empty) |
```

**Key Points:**
- Only BC products have National_Item_Code populated
- AS products may or may not have links
- NB products don't link to anything (they ARE the reference)

---

**[SECTION 2: Coverage Analysis - 2 min]**

```python
# How many BC products have a national brand link?
bc_items = df[df['Brand'] == 'BC']
has_link = bc_items['National_Item_Code'].notna().sum()
total_bc = len(bc_items)
print(f"BC items with NB link: {has_link}/{total_bc} ({has_link/total_bc*100:.1f}%)")

# Do all links resolve to actual NB products?
nb_item_codes = set(df[df['Brand'] == 'NB']['Item Code'])
bc_links = set(bc_items['National_Item_Code'].dropna())
valid_links = bc_links.intersection(nb_item_codes)
print(f"Valid links: {len(valid_links)}/{len(bc_links)}")
```

**Animation:** Venn diagram showing linkage coverage

---

**[SECTION 3: Handling Missing Links - 2 min]**

**Products without Links:**
- Some BC products are unique (no NB equivalent)
- Some links might be data entry errors
- Can't calculate gap without a comparison

**Options:**
1. **Exclude from gap analysis** - Most common
2. **Impute using category average** - Risky
3. **Flag for client clarification** - Best practice

```python
# Separate linked vs unlinked for analysis
linked_bc = bc_items[bc_items['National_Item_Code'].notna()]
unlinked_bc = bc_items[bc_items['National_Item_Code'].isna()]

print(f"Can analyze: {len(linked_bc)} products")
print(f"Cannot analyze (no link): {len(unlinked_bc)} products")
```

**Animation:** Products sorting into two bins

---

**[SECTION 4: Quality Checks - 1.5 min]**

**Check 1: Same category?**
```python
# Linked products should be in same category
merged = linked_bc.merge(nb_products, ...)
mismatched = merged[merged['Category_BC'] != merged['Category_NB']]
print(f"Category mismatches: {len(mismatched)}")
```

**Check 2: Same pack size?**
```python
# Comparing 12oz to 24oz isn't fair
mismatched_size = merged[merged['Size_BC'] != merged['Size_NB']]
```

**Animation:** Warning flags on mismatched products

---

**[OUTRO - 30 sec]**
"Clean linkages make clean analysis. Document any issues and flag them for the client."

---

### Video 3: Visualization Techniques (8 min)
**Purpose:** Create compelling visuals for price gap analysis

**Script Outline:**

**[INTRO - 30 sec]**
"Numbers tell the story. Visualizations make it memorable. Let's create charts that communicate price gaps effectively."

---

**[SECTION 1: Distribution - Histogram - 2 min]**

```python
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
plt.hist(comparison['Price_Gap_Pct'], bins=50, edgecolor='black', alpha=0.7)
plt.axvline(x=20, color='green', linestyle='--', label='20% Target')
plt.axvline(x=0, color='red', linestyle='--', label='Zero (BC = NB)')
plt.axvline(x=comparison['Price_Gap_Pct'].mean(), color='blue', label='Mean')
plt.xlabel('Price Gap (%)')
plt.ylabel('Number of Products')
plt.title('Distribution of Price Gaps: Best Choice vs National Brand')
plt.legend()
plt.show()
```

**Animation:** Histogram building bar by bar, reference lines appearing

**What to Look For:**
- Shape: Normal? Skewed? Bimodal?
- Center: Where's the average?
- Spread: How much variation?
- Outliers: Any extreme values?

---

**[SECTION 2: Category Comparison - Bar Chart - 2 min]**

```python
# Average gap by category
category_gaps = comparison.groupby('Category')['Price_Gap_Pct'].mean().sort_values()

plt.figure(figsize=(12, 8))
colors = ['red' if x < 20 else 'green' for x in category_gaps]
category_gaps.plot(kind='barh', color=colors)
plt.axvline(x=20, color='black', linestyle='--', label='20% Target')
plt.xlabel('Average Price Gap (%)')
plt.title('Price Gap by Category')
plt.tight_layout()
plt.show()
```

**Animation:** Bars growing, color coding appearing

**Design Choices:**
- Horizontal bars for readable category names
- Color coding: Green (≥20%), Red (<20%)
- Reference line at target

---

**[SECTION 3: Geographic Comparison - Heatmap - 2 min]**

```python
# Gap by Division and Category
pivot = comparison.pivot_table(
    values='Price_Gap_Pct',
    index='Category',
    columns='Division',
    aggfunc='mean'
)

plt.figure(figsize=(12, 10))
sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', center=20)
plt.title('Price Gap (%) by Category and Division')
plt.show()
```

**Animation:** Heatmap cells filling with colors

**Reading the Heatmap:**
- Green: Above target (good)
- Red: Below target (investigate)
- Patterns: Any divisions consistently high/low?

---

**[SECTION 4: Time Trend - Line Chart - 1.5 min]**

```python
# Gap over time by category
quarter_trends = comparison.groupby(['Quarter', 'Category'])['Price_Gap_Pct'].mean().unstack()

quarter_trends.plot(figsize=(10, 6), marker='o')
plt.axhline(y=20, color='black', linestyle='--', label='Target')
plt.xlabel('Quarter')
plt.ylabel('Price Gap (%)')
plt.title('Price Gap Trends by Category')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.show()
```

**Animation:** Lines drawing across quarters

---

**[OUTRO - 30 sec]**
"Good visualizations answer questions at a glance. Your charts should make the findings obvious."

---

### Video 4: Interpreting Results (5 min)
**Purpose:** Turn numbers into business insights

**Script Outline:**

**[INTRO - 30 sec]**
"You've calculated the gaps. Now what? Let's turn data into recommendations."

---

**[SECTION 1: Against the Target - 1.5 min]**

**Key Findings (from our analysis):**
- Average gap: 32.3% (exceeds 20% target!)
- Median gap: 31.5%
- 78% of products meet or exceed target

**Animation:** Scorecard with green checkmarks

**Interpretation:**
"Best Choice is competitively priced overall. The 20% target is being exceeded on average."

**But...**
"Averages hide variation. Let's dig deeper."

---

**[SECTION 2: Category Insights - 1.5 min]**

**Top Performers (highest gaps):**
- Paper Products: 42% gap
- Cleaning Supplies: 38% gap

**Underperformers (lowest gaps):**
- Oral Hygiene: 12% gap
- Personal Cleansing: 15% gap

**Animation:** Sorted bar chart with annotations

**Questions for Client:**
- Are underperforming categories intentionally priced closer to NB?
- Is there less price sensitivity in these categories?
- Are there supply cost issues?

---

**[SECTION 3: Outliers and Anomalies - 1.5 min]**

**Negative Gaps (BC > NB):**
- 40 products with negative gaps
- Concentrated in specific categories

**Animation:** Scatter plot with negative region highlighted

**What to Do:**
1. List the specific products
2. Check data quality (correct linkage?)
3. Flag for client review

```python
# Get negative gap products
negative_gaps = comparison[comparison['Price_Gap_Pct'] < 0]
negative_gaps[['Item Code', 'Description', 'Category', 'Price_Gap_Pct']]
```

---

**[OUTRO - 30 sec]**
"RQ1 answer: Yes, Best Choice is competitively priced overall. But there are opportunities in specific categories. That's the insight AWG needs."

---

## Notebooks to Create

### `week05_rq1_price_gap_starter.ipynb`

**Structure:**
```python
# ============================================
# RQ1: PRICE GAP ANALYSIS
# Are AWG private labels competitively priced?
# ============================================

# === SECTION 1: SETUP ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load prepared data (from Week 4)
pricing = pd.read_csv('prepared_data_normalized/pricing_long.csv')

# === SECTION 2: FILTER TO RELEVANT DATA ===
# Get Best Choice products with national brand links
bc_data = pricing[pricing['Brand'] == 'BC'].copy()
# TODO: Check how many have National_Item_Code

# Get National Brand products
nb_data = pricing[pricing['Brand'] == 'NB'].copy()

# === SECTION 3: LINK BC TO NB ===
# TODO: Merge BC with NB using National_Item_Code

# === SECTION 4: CALCULATE PRICE GAP ===
# TODO: Calculate gap using SRP
# Formula: (NB_SRP - BC_SRP) / NB_SRP * 100

# === SECTION 5: SUMMARY STATISTICS ===
# TODO: Mean, median, std, min, max
# TODO: % meeting 20% target

# === SECTION 6: ANALYSIS BY CATEGORY ===
# TODO: Group by category, calculate average gap

# === SECTION 7: ANALYSIS BY DIVISION ===
# TODO: Group by division

# === SECTION 8: ANALYSIS BY QUARTER ===
# TODO: Group by quarter, look for trends

# === SECTION 9: VISUALIZATIONS ===
# TODO: Histogram of gaps
# TODO: Bar chart by category
# TODO: Heatmap by category × division
# TODO: Line chart over time

# === SECTION 10: OUTLIER ANALYSIS ===
# TODO: Identify negative gaps
# TODO: List products for client review

# === SECTION 11: KEY FINDINGS ===
"""
## RQ1 Findings

### Overall
- Average price gap: ____%
- Target (20%) met: Yes/No

### By Category
- Highest gap: ____ (___%)
- Lowest gap: ____ (___%)

### Anomalies
- Negative gaps: ___ products
- Recommend: ____

### Recommendations
1.
2.
3.
"""
```

---

## Animation Production Notes

### Video 1: Price Gap Methodology

**Animation 1: Gap Visualization (Manim)**
```python
class PriceGapVisualization(Scene):
    def construct(self):
        # Number line from $0 to $6
        number_line = NumberLine(x_range=[0, 6, 1], length=10)
        self.play(Create(number_line))

        # NB price point at $4.99
        nb_dot = Dot(number_line.n2p(4.99), color=RED)
        nb_label = Text("National Brand\n$4.99").scale(0.5).next_to(nb_dot, UP)

        # BC price point at $3.99
        bc_dot = Dot(number_line.n2p(3.99), color=GREEN)
        bc_label = Text("Best Choice\n$3.99").scale(0.5).next_to(bc_dot, DOWN)

        self.play(Create(nb_dot), Write(nb_label))
        self.play(Create(bc_dot), Write(bc_label))

        # Arrow showing gap
        gap_arrow = DoubleArrow(
            number_line.n2p(3.99),
            number_line.n2p(4.99),
            color=YELLOW
        )
        gap_label = Text("Gap: $1.00 = 20%").scale(0.6).next_to(gap_arrow, UP)

        self.play(Create(gap_arrow), Write(gap_label))
```

**Animation 2: Gap Gauge**
```python
class GapGauge(Scene):
    def construct(self):
        # Semi-circular gauge
        # Red zone: <0%
        # Yellow zone: 0-20%
        # Green zone: >20%

        # Needle pointing to calculated gap
        # Animate needle moving to different values
```

### Video 3: Visualizations

**Animation: Chart Building**
- Show data transforming into chart step by step
- Bars growing from zero
- Colors filling in based on thresholds
- Reference lines appearing with labels

---

## Production Checklist

- [ ] Video 1: Price Gap Methodology
  - [ ] Script finalized
  - [ ] Gap calculation animation
  - [ ] Formula walkthrough
  - [ ] Code examples
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 2: Linking Products
  - [ ] Script finalized
  - [ ] Link diagram animation
  - [ ] Coverage analysis visuals
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 3: Visualizations
  - [ ] Script finalized
  - [ ] Chart building animations
  - [ ] Code for each chart type
  - [ ] Design principles
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 4: Interpreting Results
  - [ ] Script finalized
  - [ ] Scorecard animation
  - [ ] Insights framework
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Notebooks
  - [ ] RQ1 starter notebook
  - [ ] Tested with AWG data
  - [ ] Sample outputs verified

---

## Notes

Week 5 is the first "answer" week. Students should feel the satisfaction of producing a real business insight. Key messages:
1. The method matters - proper calculation, proper linking
2. Aggregation reveals patterns - category, division, time
3. Visualization communicates - make insights obvious
4. Outliers are opportunities - negative gaps need investigation

This sets the pattern for RQ2-RQ6: methodology → calculation → aggregation → visualization → interpretation.
