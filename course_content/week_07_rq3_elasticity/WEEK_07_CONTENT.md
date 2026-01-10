# Week 7: Research Question 3 - Price Elasticity

## Overview
**Theme:** How Sensitive is Demand?
**Duration:** Seventh week of semester
**Deliverables:** RQ3 Analysis Notebook, Elasticity Estimates by Category, Recommendations

---

## Learning Objectives

By the end of this week, students will be able to:
1. Define and interpret price elasticity of demand
2. Calculate elasticity using arc elasticity and log-log regression
3. Classify products as elastic or inelastic
4. Identify business implications of elasticity estimates
5. Recognize limitations and endogeneity concerns

---

## Research Question

**RQ3: How sensitive is demand to price changes? Which categories are elastic vs inelastic?**

**Sub-questions:**
- What is the average price elasticity across AWG products?
- Which categories are most/least price sensitive?
- Does elasticity differ by brand (NB vs BC vs AS)?
- Can AWG use elasticity to optimize pricing?

---

## Content to Create

### Video 1: Elasticity Concepts (8 min)
**Purpose:** Economic foundation of price elasticity

**Script Outline:**

**[INTRO - 30 sec]**
"If AWG raises the price of cereal by 10%, what happens to sales? The answer depends on elasticity - how sensitive customers are to price changes."

---

**[SECTION 1: Definition - 2 min]**

**Price Elasticity of Demand:**
```
Elasticity (ε) = % Change in Quantity / % Change in Price
```

**Animation:** Two gauges - price change and quantity change

**Example:**
```
Price increases 10%
Quantity decreases 20%

ε = -20% / 10% = -2.0
```

**Interpretation:**
- Negative sign: Higher price → lower demand (law of demand)
- Magnitude matters: How big is the response?

---

**[SECTION 2: Elastic vs Inelastic - 2 min]**

**Animation:** Two demand curves with different slopes

**Elastic (|ε| > 1):**
- Quantity changes MORE than price
- Customers are very price sensitive
- Examples: Luxury goods, many substitutes

**Inelastic (|ε| < 1):**
- Quantity changes LESS than price
- Customers aren't very price sensitive
- Examples: Necessities, few substitutes, habits

**Unit Elastic (|ε| = 1):**
- Quantity changes exactly as much as price
- Revenue unchanged when price changes

**Animation:** Revenue rectangles showing elastic vs inelastic effects

---

**[SECTION 3: Revenue Implications - 2 min]**

**Key Insight:** Elasticity tells you what happens to revenue

```
Revenue = Price × Quantity

If demand is ELASTIC (|ε| > 1):
  - Price ↑ → Revenue ↓ (lose too many customers)
  - Price ↓ → Revenue ↑ (gain more than enough customers)

If demand is INELASTIC (|ε| < 1):
  - Price ↑ → Revenue ↑ (don't lose many customers)
  - Price ↓ → Revenue ↓ (don't gain enough customers)
```

**Animation:** Revenue calculation before/after price change

**For AWG:**
- Inelastic categories: Can support higher prices
- Elastic categories: Be careful with price increases

---

**[SECTION 4: Factors Affecting Elasticity - 1.5 min]**

**Animation:** Factors appearing with examples

1. **Substitutes:** More substitutes → more elastic
   - Generic cereal has NB substitute → elastic
   - Unique product → inelastic

2. **Necessity:** Necessities → inelastic
   - Baby formula → inelastic
   - Gourmet snacks → elastic

3. **Time:** Longer time → more elastic
   - Can find alternatives, change habits

4. **Budget Share:** Higher share → more elastic
   - Big purchases scrutinized more

---

**[OUTRO - 30 sec]**
"Elasticity is one of the most useful concepts in pricing. Let's calculate it for AWG products."

---

### Video 2: Calculating Elasticity (10 min)
**Purpose:** Methods for estimating elasticity from data

**Script Outline:**

**[INTRO - 30 sec]**
"There are multiple ways to calculate elasticity. We'll cover two: arc elasticity and regression."

---

**[SECTION 1: Arc Elasticity - 2.5 min]**

**Problem with Simple Formula:**
- % change depends on starting point
- 10 → 12 is +20%, but 12 → 10 is -17%

**Arc Elasticity (Midpoint Formula):**
```
ε = [(Q2-Q1)/((Q2+Q1)/2)] / [(P2-P1)/((P2+P1)/2)]
```

**Animation:** Formula breakdown with visual

```python
def arc_elasticity(p1, p2, q1, q2):
    pct_q = (q2 - q1) / ((q2 + q1) / 2)
    pct_p = (p2 - p1) / ((p2 + p1) / 2)
    return pct_q / pct_p

# Example
p1, p2 = 3.99, 4.29  # Price change
q1, q2 = 1000, 900   # Quantity change
e = arc_elasticity(p1, p2, q1, q2)
print(f"Arc Elasticity: {e:.2f}")
```

---

**[SECTION 2: Log-Log Regression - 3 min]**

**Mathematical Foundation:**
```
ln(Q) = α + β × ln(P) + ε

β = Elasticity!
```

**Why Log-Log?**
- Coefficient IS the elasticity (no extra calculation)
- Handles non-linear relationships
- More robust to outliers

**Animation:** Scatter plot transforming with log scale

```python
import numpy as np
from scipy import stats

# Take logs of price and quantity
log_price = np.log(df['Price'])
log_quantity = np.log(df['Quantity'])

# Regression
slope, intercept, r_value, p_value, std_err = stats.linregress(
    log_price, log_quantity
)

print(f"Elasticity: {slope:.2f}")
print(f"R-squared: {r_value**2:.2f}")
```

---

**[SECTION 3: Implementation for AWG - 3 min]**

```python
# Using pricing and sales data
merged = pd.read_csv('prepared_data_normalized/pricing_sales_merged.csv')

# Calculate percent changes (Q-over-Q)
merged = merged.sort_values(['Item Code', 'Division', 'Quarter'])
merged['Price_Pct_Change'] = merged.groupby(['Item Code', 'Division'])['SRP'].pct_change()
merged['Qty_Pct_Change'] = merged.groupby(['Item Code', 'Division'])['Units'].pct_change()

# Filter valid observations
valid = merged.dropna(subset=['Price_Pct_Change', 'Qty_Pct_Change'])
valid = valid[valid['Price_Pct_Change'] != 0]  # Need price change

# Simple elasticity
valid['Elasticity'] = valid['Qty_Pct_Change'] / valid['Price_Pct_Change']

# By category
category_elasticity = valid.groupby('Category')['Elasticity'].median()
```

---

**[SECTION 4: Handling Challenges - 1.5 min]**

**Challenge 1: Extreme Values**
- Small price changes → huge calculated elasticity
- Solution: Use median, winsorize, or regression

**Challenge 2: Endogeneity**
- Price affects quantity, but quantity might affect price
- Solution: Beyond this course, but acknowledge

**Challenge 3: Zero Sales**
- Can't calculate % change or log
- Solution: Add small constant or exclude

---

**[OUTRO - 30 sec]**
"Elasticity estimation requires care. Multiple methods provide robustness."

---

### Video 3: Interpreting Elasticity (7 min)
**Purpose:** Turn estimates into business insights

**Script Outline:**

**[INTRO - 30 sec]**
"You've calculated elasticity. Now what does -0.5 actually mean for AWG?"

---

**[SECTION 1: Reading the Number - 2 min]**

```
Elasticity = -0.5

Interpretation:
"A 10% price increase leads to a 5% decrease in quantity sold"

Or:
"A 1% price increase leads to a 0.5% decrease in quantity sold"
```

**Animation:** Price-quantity see-saw

**Magnitude Guide:**
| Elasticity | Interpretation |
|------------|----------------|
| -0.2 | Very inelastic (demand barely changes) |
| -0.5 | Inelastic (quantity drops less than price rises) |
| -1.0 | Unit elastic (revenue unchanged) |
| -2.0 | Elastic (quantity drops more than price rises) |
| -5.0 | Very elastic (customers flee at price increase) |

---

**[SECTION 2: AWG Findings - 2 min]**

**From Our Analysis:**
- Overall median elasticity: -0.28 (inelastic)
- Most categories: Between -0.1 and -0.8

**Most Elastic Categories (price sensitive):**
- Soup: -5.00
- Canned Vegetables: -2.30

**Most Inelastic Categories:**
- Baby Care: -0.05
- Pet Food: -0.15

**Animation:** Bar chart sorted by elasticity

---

**[SECTION 3: Strategic Implications - 2 min]**

**For Inelastic Products:**
- Can raise prices without losing much volume
- Revenue increases with price
- Margin improvement opportunity

**For Elastic Products:**
- Price increases hurt revenue
- Consider promotions/price reductions
- Competitive positioning matters more

**Animation:** Decision tree based on elasticity

**For AWG Specifically:**
- Inelastic staples: Opportunity to improve margins
- Elastic categories: Focus on cost efficiency, not price increases

---

**[SECTION 4: Caveats - 1 min]**

1. **Elasticity changes:** Not constant over price range
2. **Cross-effects:** Raising one price affects other products
3. **Competition:** Elasticity depends on what competitors do
4. **Time period:** Short-run vs long-run differ

---

**[OUTRO - 30 sec]**
"Elasticity is a guide, not gospel. Combined with RQ1 and RQ2, it shapes pricing strategy."

---

### Video 4: Category Differences (5 min)
**Purpose:** Deep dive into why categories differ

**Script Outline:**

**[INTRO - 30 sec]**
"Soup is elastic. Baby care is inelastic. Why?"

---

**[SECTION 1: High Elasticity Explained - 1.5 min]**

**Soup (ε = -5.0):**
- Many substitutes (different brands, fresh alternatives)
- Not a necessity (can skip soup)
- Easy to compare prices
- Private label vs national brand competition

**Canned Vegetables:**
- Fresh/frozen alternatives
- High substitutability across brands

**Animation:** Product with arrows pointing to substitutes

---

**[SECTION 2: Low Elasticity Explained - 1.5 min]**

**Baby Care (ε = -0.05):**
- Parents won't compromise on baby products
- Brand loyalty (trust)
- Specific needs (can't substitute)
- Small budget share (less scrutiny)

**Pet Food:**
- Pet owners loyal to brands that work
- Pets have dietary needs/preferences
- Emotional purchase

**Animation:** Customer thinking about necessities vs luxuries

---

**[SECTION 3: Implications - 1.5 min]**

**AWG Strategy by Category:**
```
Inelastic (Baby, Pet):
  → Premium pricing possible
  → Focus on quality messaging

Elastic (Soup, Canned Veg):
  → Competitive pricing critical
  → Promotions effective
  → Best Choice value proposition strongest here
```

---

**[OUTRO - 30 sec]**
"Category-level elasticity drives category-level strategy. One size doesn't fit all."

---

## Notebooks to Create

### `week07_rq3_elasticity_starter.ipynb`

```python
# ============================================
# RQ3: PRICE ELASTICITY ANALYSIS
# How sensitive is demand to price?
# ============================================

# === SETUP ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# === LOAD DATA ===
merged = pd.read_csv('prepared_data_normalized/pricing_sales_merged.csv')

# === CALCULATE CHANGES ===
# TODO: Sort by Item Code, Division, Quarter
# TODO: Calculate price and quantity percent changes

# === ARC ELASTICITY ===
# TODO: Calculate arc elasticity for each observation

# === REGRESSION ELASTICITY ===
# TODO: Log-log regression for overall elasticity

# === BY CATEGORY ===
# TODO: Estimate elasticity per category

# === BY BRAND ===
# TODO: Compare NB vs BC vs AS elasticity

# === VISUALIZATIONS ===
# TODO: Histogram of elasticity distribution
# TODO: Bar chart by category
# TODO: Demand curves for select products

# === KEY FINDINGS ===
"""
## RQ3 Findings

### Overall
- Median elasticity: ____
- Range: ____ to ____

### Most Elastic (Price Sensitive)
1. ____: ____
2. ____: ____

### Most Inelastic
1. ____: ____
2. ____: ____

### Recommendations
1.
2.
"""
```

---

## Animation Production Notes

### Video 1: Elasticity Concepts

**Animation: Demand Curves (Manim)**
```python
class DemandCurves(Scene):
    def construct(self):
        # Axes
        axes = Axes(x_range=[0, 100], y_range=[0, 10])

        # Elastic demand curve (flat)
        elastic = axes.plot(lambda x: 8 - 0.02*x, color=BLUE)
        elastic_label = Text("Elastic", color=BLUE)

        # Inelastic demand curve (steep)
        inelastic = axes.plot(lambda x: 8 - 0.1*x, color=RED)
        inelastic_label = Text("Inelastic", color=RED)

        # Show price change and different quantity responses
```

**Animation: Revenue Rectangles**
```python
class RevenueChange(Scene):
    def construct(self):
        # Show P×Q rectangle before
        # Animate price change
        # Show new P×Q rectangle
        # Compare sizes for elastic vs inelastic
```

---

## Production Checklist

- [ ] Video 1: Elasticity Concepts
  - [ ] Script finalized
  - [ ] Demand curve animations
  - [ ] Revenue rectangle animation
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 2: Calculating Elasticity
  - [ ] Script finalized
  - [ ] Arc elasticity walkthrough
  - [ ] Log-log regression explanation
  - [ ] Code examples
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 3: Interpreting Results
  - [ ] Script finalized
  - [ ] AWG findings visualization
  - [ ] Strategy implications
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 4: Category Differences
  - [ ] Script finalized
  - [ ] Category comparison chart
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Notebooks
  - [ ] RQ3 starter notebook
  - [ ] Tested with AWG data

---

## Notes

Week 7 completes the first set of research questions before mid-term. Key messages:
1. Elasticity connects price to demand
2. Categories differ - one strategy doesn't fit all
3. Inelastic ≠ "charge whatever you want" (competition still matters)
4. This informs RQ1 (which price gaps can be narrowed without losing sales?)
