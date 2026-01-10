# Week 11: Research Question 6 - Tariff Impact Analysis

## Overview
**Theme:** External Shocks & Pricing
**Duration:** Eleventh week of semester
**Deliverables:** RQ6 Analysis Notebook, Tariff-Sensitive Category Identification, Anomaly Report

---

## Learning Objectives

By the end of this week, students will be able to:
1. Identify tariff-sensitive product categories
2. Use difference-in-differences logic for impact analysis
3. Detect unusual price movements using z-scores
4. Distinguish correlation from causation

---

## Research Question

**RQ6: How have tariffs affected AWG's costs and pricing?**

**Sub-questions:**
- Which categories are tariff-sensitive? (coffee, oils, imported goods)
- Did tariff-sensitive categories show larger cost increases?
- Did price changes follow cost changes differently?
- Are there anomalous price movements suggesting tariff impact?

---

## Content to Create

### Video 1: Tariff Background (8 min)

**Key Topics:**
- What tariffs affected grocery in 2024-2025
- Tariff-sensitive categories for AWG:
  - Coffee (imported beans)
  - Cooking oils (some imported)
  - Chocolate (cocoa imports)
  - Canned goods (steel cans)
- Timeline of tariff implementation
- Expected impact: Higher costs → higher prices

**Animation Ideas:**
- World map showing import routes
- Timeline with tariff announcements
- Cost impact flowchart

---

### Video 2: Anomaly Detection Methods (10 min)

**Key Topics:**
- Z-score methodology: How many standard deviations from normal?
  ```
  z = (observed_change - mean_change) / std_change
  ```
- Identifying unusual price/cost movements
- Threshold: |z| > 2 = unusual, |z| > 3 = highly unusual
- Category-level vs product-level anomalies

**Code Example:**
```python
# Calculate z-scores for price changes by category
category_changes = pricing.groupby('Category')['Price_Change_Pct'].mean()
z_scores = (category_changes - category_changes.mean()) / category_changes.std()

# Flag anomalies
anomalies = z_scores[abs(z_scores) > 2]
```

**Animation Ideas:**
- Normal distribution with z-score regions
- Products moving into anomaly zones

---

### Video 3: Difference-in-Differences (10 min)

**Key Topics:**
- Comparing tariff-sensitive vs non-sensitive categories
- Treatment: Tariff-sensitive categories
- Control: Non-tariff-sensitive categories
- Compare: Did treatment group change more?

**Framework:**
```
DiD = (Tariff_After - Tariff_Before) - (NonTariff_After - NonTariff_Before)

If DiD > 0: Tariff categories increased more → tariff effect
```

**Code Example:**
```python
# Classify categories
tariff_sensitive = ['Coffee', 'Cooking Oil', 'Chocolate']
df['Tariff_Exposed'] = df['Category'].isin(tariff_sensitive)

# Compare changes
tariff_change = df[df['Tariff_Exposed']]['Cost_Change'].mean()
non_tariff_change = df[~df['Tariff_Exposed']]['Cost_Change'].mean()
print(f"Difference: {tariff_change - non_tariff_change:.2%}")
```

**Animation Ideas:**
- Parallel trends diagram
- Treatment vs control group comparison

---

### Video 4: Causal Inference Cautions (5 min)

**Key Topics:**
- Correlation ≠ Causation
- What we CAN say: "Tariff-sensitive categories had larger cost increases"
- What we CANNOT say definitively: "Tariffs caused these increases"
- Other factors: Supply chain issues, demand shifts, seasonality
- Appropriate language in recommendations

**Animation Ideas:**
- Spurious correlation examples
- Causation ladder (description → prediction → causal)

---

## Notebook: `week11_rq6_tariff_starter.ipynb`

**Sections:**
1. Setup and data loading
2. Classify tariff-sensitive categories
3. Compare cost changes: tariff-sensitive vs others
4. Z-score anomaly detection
5. Difference-in-differences analysis
6. Timeline visualization
7. Key findings and caveats

**Key Findings from Analysis:**
- Tariff-sensitive categories: 2.03% cost change vs 0.90% others
- Oral Hygiene category has unusual price changes (z=3.72)
- Evidence suggests tariff impact, but not conclusive proof

---

## Animation Production Notes

**Z-Score Distribution (Manim)**
```python
class ZScoreDistribution(Scene):
    def construct(self):
        # Normal distribution curve
        # Shade regions: -2 to 2 (normal), beyond (anomaly)
        # Animate data points falling into regions
```

**Difference-in-Differences (Manim)**
```python
class DiDAnimation(Scene):
    def construct(self):
        # Two lines: Treatment and Control
        # Before period: Lines at same level
        # After period: Treatment line jumps more
        # Highlight the difference-in-differences
```

---

## Production Checklist

- [ ] Video 1: Tariff Background
- [ ] Video 2: Anomaly Detection
- [ ] Video 3: Difference-in-Differences
- [ ] Video 4: Causal Inference Cautions
- [ ] Starter notebook
- [ ] Tariff timeline asset

---

## Notes

RQ6 is about detective work with limited data. Key messages:
1. We can detect patterns consistent with tariff impact
2. We cannot prove causation with observational data
3. Anomalies warrant further investigation
4. Appropriate hedging in conclusions is professional, not weak
