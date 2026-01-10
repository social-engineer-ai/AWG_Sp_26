# Week 10: Research Question 5 - Geographic Variation

## Overview
**Theme:** Regional Pricing Differences
**Duration:** Tenth week of semester
**Deliverables:** RQ5 Analysis Notebook, Division Comparison, Urban/Rural Analysis

---

## Learning Objectives

By the end of this week, students will be able to:
1. Analyze price variation across geographic regions
2. Calculate coefficient of variation for pricing consistency
3. Compare urban vs rural pricing strategies
4. Identify regional pricing anomalies

---

## Research Question

**RQ5: Does AWG's pricing strategy vary across its 9 divisions? Should it?**

**Sub-questions:**
- How much does BSP vary across divisions for the same product?
- Does List Cost (supplier pricing) vary? (It shouldn't much)
- Are there urban vs rural price differences?
- Which divisions have higher/lower markups?

---

## Content to Create

### Video 1: AWG Division Overview (7 min)

**Key Topics:**
- AWG's 9 divisions: KC, SP, OK, NA, GC, NE, GL, HN, UM
- Geographic coverage map
- Division characteristics (size, market type)
- Why pricing might vary regionally

**Animation Ideas:**
- US map with division territories
- Division profile cards appearing

**Division Reference:**
| Code | Full Name | Characteristics |
|------|-----------|-----------------|
| KC | Kansas City | HQ, urban core |
| SP | Springfield | Mixed urban/rural |
| OK | Oklahoma | Regional market |
| NA | (verify) | |
| GC | Gulf Coast? | |
| NE | Nebraska/Northeast? | |
| GL | Great Lakes? | |
| HN | (verify) | |
| UM | Upper Midwest? | |

---

### Video 2: Analyzing Geographic Variation (10 min)

**Key Topics:**
- Measuring variation: Coefficient of Variation (CV)
  - CV = Standard Deviation / Mean × 100
  - Low CV (<5%): Consistent pricing
  - High CV (>10%): Significant variation
- Per-product CV across divisions
- Expected: List Cost low CV, BSP/SRP higher CV

**Code Example:**
```python
# Calculate CV for each product across divisions
product_cv = pricing.groupby('Item Code').agg({
    'List_Cost': lambda x: x.std() / x.mean() * 100,
    'BSP': lambda x: x.std() / x.mean() * 100,
    'SRP': lambda x: x.std() / x.mean() * 100
})
```

---

### Video 3: Urban vs Rural Pricing (8 min)

**Key Topics:**
- Classifying divisions as urban/rural (or mixed)
- Compare average prices between types
- Cost-to-serve differences (logistics, store density)
- Competitive environment differences

**Key Finding from Analysis:**
- Rural prices ~3.1% higher than urban
- Consistent with higher distribution costs

**Animation Ideas:**
- Urban vs rural store comparison
- Cost breakdown visualization

---

### Video 4: The List Cost Puzzle (7 min)

**Key Topics:**
- Finding: 43.8% of items have varying List Cost across divisions
- This is unexpected (supplier price should be uniform)
- Possible explanations:
  - Regional supplier deals
  - Different pack sizes (data issue)
  - Timing differences
- Question for client

**Animation Ideas:**
- Expectation vs reality comparison
- Puzzle pieces with possible explanations

---

## Notebook: `week10_rq5_geographic_starter.ipynb`

**Sections:**
1. Setup and data loading
2. Division-level summary statistics
3. Coefficient of variation analysis
4. Urban/rural classification and comparison
5. Division price index (relative to KC)
6. List Cost consistency check
7. Anomaly identification

---

## Animation Production Notes

**Division Map (Manim/Motion Graphics)**
- US map outline
- 9 regions filling with colors
- Labels and stats appearing

**CV Visualization**
- Products sorted by CV
- Color gradient: Green (consistent) to Red (variable)

---

## Production Checklist

- [ ] Video 1: Division Overview
- [ ] Video 2: Geographic Variation Analysis
- [ ] Video 3: Urban vs Rural
- [ ] Video 4: List Cost Puzzle
- [ ] Starter notebook
- [ ] Division map asset

---

## Notes

RQ5 often reveals data quality issues (like List Cost variation). Key insights:
1. BSP variation is low (1.9% CV) - relatively uniform pricing
2. Urban/rural differences exist but are small
3. List Cost variation is a red flag for client discussion
