# Week 6: Research Question 2 - Cost Pass-Through

## Overview
**Theme:** How Do Costs Flow to Prices?
**Duration:** Sixth week of semester
**Deliverables:** RQ2 Analysis Notebook, Pass-Through Rate Calculations, Brand Comparison

---

## Learning Objectives

By the end of this week, students will be able to:
1. Define and calculate cost pass-through rates
2. Analyze quarter-over-quarter price and cost changes
3. Use simple regression to estimate pass-through coefficients
4. Compare pass-through behavior across brands (NB, BC, AS)
5. Investigate asymmetric pass-through (costs up vs costs down)

---

## Research Question

**RQ2: When supplier costs change, how much of that change passes through to wholesale (BSP) and retail (SRP) prices?**

**Sub-questions:**
- What is the average pass-through rate for AWG products?
- Do national brands pass through more cost changes than private labels?
- Is pass-through symmetric (same for increases and decreases)?
- Does pass-through vary by category?
- Is there a lag between cost changes and price changes?

---

## Content to Create

### Video 1: Pass-Through Economics (8 min)
**Purpose:** Explain the concept and business implications

**Script Outline:**

**[INTRO - 30 sec]**
"When coffee beans get more expensive, does your coffee at the store cost more? That's pass-through - how costs flow through the supply chain to prices."

---

**[SECTION 1: What is Pass-Through? - 2 min]**

**Definition:**
"Pass-through measures what fraction of a cost change is reflected in a price change."

**Animation:** Supply chain with cost flowing through

```
Supplier Cost ↑$1.00
    ↓
AWG Cost (List Cost) ↑$1.00
    ↓ Pass-through to BSP
Wholesale Price (BSP) ↑$0.80  ← 80% pass-through
    ↓ Pass-through to SRP
Retail Price (SRP) ↑$0.60  ← 75% of BSP change
```

**Pass-Through Rate:**
```
Pass-Through = ΔPrice / ΔCost

If cost ↑$1 and price ↑$0.80:
Pass-Through = $0.80 / $1.00 = 0.80 (or 80%)
```

**Animation:** Division calculation with visual bars

---

**[SECTION 2: Why Pass-Through Varies - 2 min]**

**Full Pass-Through (100%):**
- Price changes exactly match cost changes
- Margins stay constant
- Common in competitive markets

**Partial Pass-Through (<100%):**
- Company absorbs some cost increases
- Margins shrink when costs rise
- May indicate brand strength (can't raise prices)

**Over Pass-Through (>100%):**
- Price increases more than cost
- Margins expand when costs rise
- May indicate opportunistic pricing

**Animation:** Three scenarios with margin bars

**Factors Affecting Pass-Through:**
- Competition intensity
- Brand strength
- Customer price sensitivity
- Contract terms
- Strategic pricing decisions

---

**[SECTION 3: AWG Context - 2 min]**

**For AWG:**
- List Cost = What AWG pays suppliers
- BSP = What stores pay AWG
- SRP = What consumers pay stores

**Questions:**
1. When List Cost changes, how much reaches BSP?
2. When BSP changes, how much reaches SRP?
3. Does this differ for National Brands vs Best Choice vs Always Save?

**Animation:** Three-brand comparison diagram

**Hypothesis:**
- National Brands: High pass-through (brand power)
- Best Choice: Moderate (balanced strategy)
- Always Save: Low (price commitment)

---

**[SECTION 4: Measuring Pass-Through - 1.5 min]**

**Simple Calculation:**
```python
# Quarter-over-quarter changes
df['Cost_Change'] = df.groupby('Item Code')['List_Cost'].diff()
df['Price_Change'] = df.groupby('Item Code')['BSP'].diff()

# Pass-through for each observation
df['Pass_Through'] = df['Price_Change'] / df['Cost_Change']
```

**Problem:** What if cost didn't change? (Division by zero)

**Better Approach: Regression**
```
ΔPrice = α + β × ΔCost + ε

β = Pass-Through Rate
```

**Animation:** Scatter plot with regression line

---

**[OUTRO - 30 sec]**
"Pass-through reveals pricing strategy. Let's calculate it for AWG."

---

### Video 2: Calculating Pass-Through Rates (10 min)
**Purpose:** Step-by-step calculation methodology

**Script Outline:**

**[INTRO - 30 sec]**
"Let's turn theory into numbers. We'll calculate pass-through using quarter-over-quarter changes."

---

**[SECTION 1: Preparing the Data - 2 min]**

```python
# Start with long-format pricing data
pricing = pd.read_csv('prepared_data_normalized/pricing_long.csv')

# Need columns: Item Code, Division, Quarter, List_Cost, BSP_per_unit, Brand

# Sort for proper differencing
pricing = pricing.sort_values(['Item Code', 'Division', 'Quarter'])

# Calculate changes within each Item-Division group
pricing['Cost_Change'] = pricing.groupby(['Item Code', 'Division'])['List_Cost_per_unit'].diff()
pricing['BSP_Change'] = pricing.groupby(['Item Code', 'Division'])['BSP_per_unit'].diff()

# First quarter for each group will be NaN (no previous quarter)
changes = pricing.dropna(subset=['Cost_Change', 'BSP_Change'])
print(f"Observations with changes: {len(changes)}")
```

**Animation:** Data transformation visualization

---

**[SECTION 2: Simple Ratio - 2 min]**

```python
# Filter to non-zero cost changes (avoid division by zero)
nonzero = changes[changes['Cost_Change'] != 0]

# Calculate pass-through ratio
nonzero['PT_Ratio'] = nonzero['BSP_Change'] / nonzero['Cost_Change']

# Summary statistics
print(f"Mean Pass-Through: {nonzero['PT_Ratio'].mean():.2f}")
print(f"Median Pass-Through: {nonzero['PT_Ratio'].median():.2f}")
```

**Problem:** Extreme outliers when cost changes are tiny

```python
# Check for extreme values
print(nonzero['PT_Ratio'].describe())
# May see values like 50 or -100 due to small denominators
```

**Solution:** Use regression instead

---

**[SECTION 3: Regression Approach - 3 min]**

```python
from scipy import stats

# Simple linear regression: BSP_Change = α + β × Cost_Change
slope, intercept, r_value, p_value, std_err = stats.linregress(
    changes['Cost_Change'],
    changes['BSP_Change']
)

print(f"Pass-Through Rate (β): {slope:.3f}")
print(f"R-squared: {r_value**2:.3f}")
print(f"P-value: {p_value:.4f}")
```

**Animation:** Scatter plot with regression line appearing

**Interpretation:**
- β = 0.40 means 40% pass-through
- R² tells us how much variation is explained
- P-value < 0.05 means statistically significant

**Alternative: statsmodels for more control**
```python
import statsmodels.api as sm

X = sm.add_constant(changes['Cost_Change'])
model = sm.OLS(changes['BSP_Change'], X).fit()
print(model.summary())
```

---

**[SECTION 4: By Brand - 2 min]**

```python
# Separate regression for each brand
brands = ['NB', 'BC', 'AS']
results = {}

for brand in brands:
    brand_data = changes[changes['Brand'] == brand]
    if len(brand_data) > 10:  # Need enough data
        slope, _, r_val, p_val, _ = stats.linregress(
            brand_data['Cost_Change'],
            brand_data['BSP_Change']
        )
        results[brand] = {
            'pass_through': slope,
            'r_squared': r_val**2,
            'n': len(brand_data)
        }

# Compare
for brand, res in results.items():
    print(f"{brand}: PT={res['pass_through']:.2f}, R²={res['r_squared']:.2f}, n={res['n']}")
```

**Animation:** Three regression lines on same plot, different colors

**Expected Pattern:**
- National Brand: ~1.00 (full pass-through)
- Best Choice: ~0.35 (partial)
- Always Save: ~0.20 (low)

---

**[OUTRO - 30 sec]**
"Regression gives us robust pass-through estimates. Now let's dig deeper into asymmetries and lags."

---

### Video 3: Regression Basics (10 min)
**Purpose:** Teach regression for students who need a refresher

**Script Outline:**

**[INTRO - 30 sec]**
"Regression is the workhorse of business analytics. Let's understand what it's doing and when to use it."

---

**[SECTION 1: The Idea - 2 min]**

**Goal:** Find the best line through scattered points

**Animation:** Scatter plot, then best-fit line appearing

**The Line:**
```
Y = α + β × X

Y = outcome (what we're predicting)
X = input (what we're using to predict)
α = intercept (Y when X=0)
β = slope (change in Y per unit change in X)
```

**For Pass-Through:**
```
Price_Change = α + β × Cost_Change

β = Pass-Through Rate (our answer!)
```

---

**[SECTION 2: Finding the Best Line - 2.5 min]**

**"Best" = Minimizes Errors**

**Animation:** Show residuals (vertical lines from points to line)

```
Error = Actual Y - Predicted Y
Residual = Each observation's error
```

**Least Squares:** Minimize sum of squared residuals

**Animation:** Squares drawn on residuals, total area minimized

**Why Squares?**
- Negative errors don't cancel positive
- Penalizes big errors more
- Has nice mathematical properties

---

**[SECTION 3: Interpreting Output - 3 min]**

```python
import statsmodels.api as sm

X = sm.add_constant(data['Cost_Change'])
model = sm.OLS(data['BSP_Change'], X).fit()
print(model.summary())
```

**Key Numbers:**

**Coefficient (β):**
- The slope
- "For each $1 cost increase, price increases by $β"
- Our pass-through rate

**Standard Error:**
- Uncertainty in coefficient estimate
- Smaller = more precise

**P-value:**
- Probability this result is due to chance
- < 0.05 = "statistically significant"
- < 0.01 = "highly significant"

**R-squared:**
- Fraction of variation explained (0 to 1)
- Higher = better fit
- 0.5 = "50% of price changes explained by cost changes"

**Animation:** Model summary with key numbers highlighted

---

**[SECTION 4: Assumptions and Cautions - 2 min]**

**Regression Assumptions:**
1. Linear relationship (check scatter plot)
2. Independent errors (no patterns in residuals)
3. Constant variance (no funnel shape)
4. Normality (for small samples)

**For Pass-Through Specifically:**
- Assumes immediate effect (no lag)
- Assumes constant rate across products
- May need category-specific regressions

**Animation:** Good vs bad residual plots

---

**[OUTRO - 30 sec]**
"Regression gives us a single number (β) to summarize the relationship. For pass-through, that number tells AWG how their pricing responds to costs."

---

### Video 4: Asymmetric Pass-Through (7 min)
**Purpose:** Test if prices rise faster than they fall

**Script Outline:**

**[INTRO - 30 sec]**
"Prices go up when costs rise. But do they come down when costs fall? Often, the answer is no - or at least, not as fast."

---

**[SECTION 1: The Asymmetry Question - 1.5 min]**

**Common Pattern (Rockets & Feathers):**
- Cost increases → Prices rise quickly (rockets)
- Cost decreases → Prices fall slowly (feathers)

**Animation:** Rocket going up, feather floating down

**Why?**
- Stickiness in pricing
- Opportunity to restore margins
- Customer inattention to price decreases

---

**[SECTION 2: Testing for Asymmetry - 2.5 min]**

```python
# Separate cost increases and decreases
increases = changes[changes['Cost_Change'] > 0]
decreases = changes[changes['Cost_Change'] < 0]

# Regression on increases
slope_up, _, _, _, _ = stats.linregress(
    increases['Cost_Change'],
    increases['BSP_Change']
)

# Regression on decreases
slope_down, _, _, _, _ = stats.linregress(
    decreases['Cost_Change'],
    decreases['BSP_Change']
)

print(f"Pass-through (cost increases): {slope_up:.2f}")
print(f"Pass-through (cost decreases): {slope_down:.2f}")
```

**Animation:** Two regression lines - one for increases (steep), one for decreases (flat)

**Interpretation:**
- If slope_up > slope_down: Asymmetric (rockets & feathers)
- If slope_up ≈ slope_down: Symmetric pass-through

---

**[SECTION 3: Statistical Test - 2 min]**

```python
# Formal test: Add interaction term
changes['Cost_Increase'] = (changes['Cost_Change'] > 0).astype(int)
changes['Cost_x_Increase'] = changes['Cost_Change'] * changes['Cost_Increase']

X = changes[['Cost_Change', 'Cost_x_Increase']]
X = sm.add_constant(X)
model = sm.OLS(changes['BSP_Change'], X).fit()
print(model.summary())
```

**Interpretation:**
- Coefficient on Cost_x_Increase = difference in pass-through
- If significant → evidence of asymmetry

---

**[SECTION 4: By Brand - 1.5 min]**

"Is asymmetry different for National Brands vs Private Labels?"

```python
# Compare asymmetry by brand
for brand in ['NB', 'BC', 'AS']:
    brand_data = changes[changes['Brand'] == brand]
    # Calculate up vs down pass-through
    # Report difference
```

**Hypothesis:**
- NB: Symmetric (competitive pressure)
- BC/AS: Asymmetric (margin recovery opportunity)

---

**[OUTRO - 30 sec]**
"Asymmetric pass-through is a real phenomenon. If AWG shows rockets and feathers, it's worth noting in recommendations."

---

## Notebooks to Create

### `week06_rq2_cost_passthrough_starter.ipynb`

**Structure:**
```python
# ============================================
# RQ2: COST PASS-THROUGH ANALYSIS
# How do costs flow to prices?
# ============================================

# === SECTION 1: SETUP ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

# === SECTION 2: LOAD DATA ===
pricing = pd.read_csv('prepared_data_normalized/pricing_long.csv')

# === SECTION 3: CALCULATE CHANGES ===
# TODO: Sort by Item Code, Division, Quarter
# TODO: Calculate Cost_Change (diff of List_Cost_per_unit)
# TODO: Calculate BSP_Change (diff of BSP_per_unit)
# TODO: Drop rows with NaN changes

# === SECTION 4: OVERALL PASS-THROUGH ===
# TODO: Regression of BSP_Change on Cost_Change
# TODO: Report β, R², p-value

# === SECTION 5: PASS-THROUGH BY BRAND ===
# TODO: Separate regressions for NB, BC, AS
# TODO: Compare coefficients

# === SECTION 6: ASYMMETRY ANALYSIS ===
# TODO: Separate increases vs decreases
# TODO: Test for rockets & feathers

# === SECTION 7: BY CATEGORY ===
# TODO: Pass-through by product category

# === SECTION 8: VISUALIZATIONS ===
# TODO: Scatter plots with regression lines
# TODO: Bar chart comparing brands
# TODO: Asymmetry visualization

# === SECTION 9: KEY FINDINGS ===
"""
## RQ2 Findings

### Overall Pass-Through
- List Cost → BSP: ____
- BSP → SRP: ____

### By Brand
- National Brand: ____
- Best Choice: ____
- Always Save: ____

### Asymmetry
- Cost increases: ____
- Cost decreases: ____
- Evidence of rockets & feathers? ____

### Recommendations
1.
2.
"""
```

---

## Animation Production Notes

### Video 1: Pass-Through Economics

**Animation 1: Supply Chain Flow (Manim)**
```python
class SupplyChainFlow(Scene):
    def construct(self):
        # Boxes: Supplier → AWG → Store → Consumer
        # Arrows with dollar amounts
        # Animate cost change flowing through
        # Show pass-through percentage at each step
```

**Animation 2: Pass-Through Scenarios**
```python
class PassThroughScenarios(Scene):
    def construct(self):
        # Three bars showing cost increase of $1
        # Three result bars showing price change
        # Label: Full (100%), Partial (50%), Over (120%)
        # Color code margins
```

### Video 3: Regression Basics

**Animation: Residuals (Manim)**
```python
class ResidualsAnimation(Scene):
    def construct(self):
        # Scatter plot
        # Draw regression line
        # Animate vertical lines (residuals) appearing
        # Show squares on residuals
        # Animate line rotating to minimize total square area
```

### Video 4: Asymmetry

**Animation: Rockets and Feathers**
```python
class RocketsFeathers(Scene):
    def construct(self):
        # Left: Cost going up (arrow), Price rocket going up fast
        # Right: Cost going down (arrow), Price feather floating slowly
        # Split screen comparison
```

---

## Production Checklist

- [ ] Video 1: Pass-Through Economics
  - [ ] Script finalized
  - [ ] Supply chain animation
  - [ ] Pass-through scenarios
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 2: Calculating Rates
  - [ ] Script finalized
  - [ ] Code walkthrough
  - [ ] Regression visualization
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 3: Regression Basics
  - [ ] Script finalized
  - [ ] Residuals animation
  - [ ] Output interpretation guide
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Video 4: Asymmetry
  - [ ] Script finalized
  - [ ] Rockets & feathers animation
  - [ ] Test methodology
  - [ ] Voice recorded
  - [ ] Final edit

- [ ] Notebooks
  - [ ] RQ2 starter notebook
  - [ ] Tested with AWG data

---

## Notes

Week 6 introduces econometric thinking. Key messages:
1. Pass-through is about relationships, not just numbers
2. Regression is a tool - understand what it's doing
3. Asymmetry is common and meaningful
4. Brand strategy reveals itself in pass-through rates
