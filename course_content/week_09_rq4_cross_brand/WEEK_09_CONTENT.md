# Week 9: Research Question 4 - Cross-Brand Effects

## Overview
**Theme:** Best Choice vs Always Save Dynamics
**Duration:** Ninth week of semester
**Deliverables:** RQ4 Analysis Notebook, Cross-Elasticity Estimates, Brand Strategy Insights

---

## Learning Objectives

By the end of this week, students will be able to:
1. Define and calculate cross-price elasticity
2. Determine if BC and AS are substitutes or complements
3. Analyze price positioning between AWG's own brands
4. Recommend brand portfolio strategy

---

## Research Question

**RQ4: Do Best Choice and Always Save compete with each other or serve different customer segments?**

**Sub-questions:**
- What is the price gap between BC and AS for similar products?
- Does changing BC price affect AS sales (and vice versa)?
- Are they substitutes (compete) or complements (different segments)?
- Is there cannibalization risk?

---

## Content to Create

### Video 1: Cross-Elasticity Concepts (8 min)

**Key Topics:**
- Definition: % change in Quantity_A / % change in Price_B
- Substitutes: Positive cross-elasticity (raise BC price → AS sales increase)
- Complements: Negative cross-elasticity (rare in this context)
- Independent: Near-zero cross-elasticity (different customer segments)

**Animation Ideas:**
- Two products on shelf, customer switching between them
- Cross-elasticity matrix visualization

---

### Video 2: Calculating Cross-Effects (10 min)

**Key Topics:**
- Data preparation: Need BC and AS prices for same categories
- Regression: AS_Sales_Change = f(BC_Price_Change)
- Handling: Only categories with both BC and AS versions
- Interpretation: What does cross-elasticity of 0.1 mean?

**Code Example:**
```python
# For each category with both BC and AS
# Regress AS quantity change on BC price change
# Low cross-elasticity → independent demand
```

---

### Video 3: AWG Brand Strategy (7 min)

**Key Topics:**
- Why have two private labels? (Good/Better positioning)
- BC vs AS price positioning (typical gap ~34%)
- Target customer segments
- Risk of cannibalization vs market coverage

**Animation Ideas:**
- Market segmentation pyramid
- Price ladder visualization (NB → BC → AS)

---

## Notebook: `week09_rq4_cross_brand_starter.ipynb`

**Sections:**
1. Setup and data loading
2. Identify categories with both BC and AS products
3. Calculate BC-AS price gap by category
4. Cross-elasticity estimation
5. Substitution pattern analysis
6. Brand strategy implications

**Key Findings to Explore:**
- BC-AS median gap: ~34%
- Cross-elasticity near zero (independent demand)
- Suggests different customer segments

---

## Animation Production Notes

**Cross-Elasticity Matrix (Manim)**
- 2x2 grid: BC Price Change vs AS Sales Change
- Quadrants: Substitutes (++), Complements (+-), Independent (~0)

**Brand Ladder**
- National Brand (top, premium)
- Best Choice (middle, quality value)
- Always Save (bottom, budget)
- Animate customer segments targeting each

---

## Production Checklist

- [ ] Video 1: Cross-Elasticity Concepts
- [ ] Video 2: Calculating Cross-Effects
- [ ] Video 3: Brand Strategy
- [ ] Starter notebook
- [ ] Key visualizations

---

## Notes

RQ4 is simpler than RQ1-3 but strategically important. Key insight: BC and AS appear to serve different customers, minimizing cannibalization. This validates AWG's two-brand strategy.
