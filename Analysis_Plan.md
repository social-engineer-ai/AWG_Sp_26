# AWG Brands Pricing & Sales Analysis Plan

## University of Illinois - Spring 2026 Project

---

## Table of Contents

1. [Research Questions Overview](#1-research-questions-overview)
2. [Detailed Analysis Framework](#2-detailed-analysis-framework)
3. [Data Preparation Summary](#3-data-preparation-summary)
4. [Analysis Execution Sequence](#4-analysis-execution-sequence)

---

## 1. Research Questions Overview

| # | Research Question | Primary Focus |
|---|-------------------|---------------|
| RQ1 | What is the price gap between Best Choice and National Brand products? | Pricing Strategy |
| RQ2 | How do supplier cost changes flow through to store and consumer prices? | Cost Pass-Through |
| RQ3 | How do price changes affect sales volume? | Price Elasticity |
| RQ4 | What are the cross-brand effects between Best Choice and Always Save? | Brand Cannibalization |
| RQ5 | How do prices and price gaps vary across geographic divisions? | Geographic Strategy |
| RQ6 | Which categories experienced significant price changes (potential tariff impact)? | Tariff Detection |

---

## 2. Detailed Analysis Framework

---

### RQ1: Price Gap Analysis (Best Choice vs National Brand)

#### 1.1 Research Question
**What is the price gap between Best Choice and National Brand products, and how does it compare to the target 20% gap?**

#### 1.2 Granularity

| Level | Description |
|-------|-------------|
| **Primary** | Product Level |
| **Aggregation** | Category, Sub-Category, Division |

#### 1.3 Sub-Dimensions

| Dimension | Values/Segments |
|-----------|-----------------|
| **Product** | Individual Item Codes with valid National Comparison linkage |
| **Category** | ~50+ categories (e.g., Canned Vegetables, Coffee, Oils) |
| **Sub-Category** | Detailed product groupings within categories |
| **Division** | KC, SP, OK, NA, GC, NE, GL, HN, UM |
| **Time** | Q1, Q2, Q3, Q4 |

#### 1.4 Metrics Needed

| Metric | Formula | Unit |
|--------|---------|------|
| BC BSP | Best Choice Base Selling Price | $ |
| National BSP | National Brand Base Selling Price | $ |
| Absolute Price Gap | National BSP - BC BSP | $ |
| **Percentage Price Gap** | (National BSP - BC BSP) / National BSP × 100 | % |
| Gap vs Target | Percentage Price Gap - 20% | % points |
| City SRP Gap | (National City SRP - BC City SRP) / National City SRP × 100 | % |

#### 1.5 Analyses

| Analysis | Description | Output |
|----------|-------------|--------|
| **A1.1** | Distribution of price gaps across all linked products | Histogram, summary statistics |
| **A1.2** | Price gap by category | Bar chart, ranked table |
| **A1.3** | Price gap by division | Comparison table, heatmap |
| **A1.4** | Price gap trend over quarters | Line chart (Q1→Q4) |
| **A1.5** | Identification of outliers (gaps >40% or <10%) | Flagged item list |

#### 1.6 Data Preparation

**Row Granularity:** One row per Product × Division × Quarter

| Column | Source | Description |
|--------|--------|-------------|
| `item_code` | Pricing File | Best Choice Item Code |
| `item_name` | Pricing File | Product name |
| `category` | Pricing File | Category |
| `sub_category` | Pricing File | Sub-category |
| `national_item_code` | Pricing File | Linked National Brand Item Code |
| `division` | Derived | Division code (KC, SP, etc.) |
| `quarter` | Derived | Q1, Q2, Q3, Q4 |
| `bc_bsp` | Pricing File | Best Choice BSP |
| `national_bsp` | Pricing File (lookup) | National Brand BSP |
| `price_gap_pct` | Calculated | Percentage price gap |

**Preparation Steps:**
```
1. Filter to Best Choice items with valid National Comparison Item Code
2. Join National Brand pricing using National Comparison Item Code
3. Melt wide pricing data to long format (Division × Quarter)
4. Calculate price gap metrics
5. Filter to rows where both BC and National prices exist
```

---

### RQ2: Cost Pass-Through Analysis

#### 2.1 Research Question
**How do supplier cost changes (List Cost) flow through to wholesale prices (BSP) and retail prices (SRP)?**

#### 2.2 Granularity

| Level | Description |
|-------|-------------|
| **Primary** | Product Level |
| **Aggregation** | Category, Brand, Division |

#### 2.3 Sub-Dimensions

| Dimension | Values/Segments |
|-----------|-----------------|
| **Product** | All items with List Cost and BSP data |
| **Brand** | Best Choice, Always Save, National Brand |
| **Category** | Product categories |
| **Division** | 9 AWG divisions |
| **Time Period** | Quarter-over-quarter transitions (Q1→Q2, Q2→Q3, Q3→Q4) |

#### 2.4 Metrics Needed

| Metric | Formula | Unit |
|--------|---------|------|
| List Cost | Supplier cost to AWG | $ |
| BSP | AWG price to retailers | $ |
| City SRP | Suggested retail price (city) | $ |
| List Cost Change | List Cost(Qt) - List Cost(Qt-1) | $ |
| List Cost Change % | (List Cost Change / List Cost(Qt-1)) × 100 | % |
| BSP Change | BSP(Qt) - BSP(Qt-1) | $ |
| BSP Change % | (BSP Change / BSP(Qt-1)) × 100 | % |
| **Pass-Through Rate** | BSP Change / List Cost Change | Ratio |
| **Pass-Through %** | (BSP Change % / List Cost Change %) × 100 | % |

#### 2.5 Analyses

| Analysis | Description | Output |
|----------|-------------|--------|
| **A2.1** | Overall pass-through rate distribution | Histogram, summary stats |
| **A2.2** | Pass-through rate by brand | Comparison bar chart |
| **A2.3** | Pass-through rate by category | Ranked table |
| **A2.4** | Pass-through timing analysis | Lag analysis (same quarter vs delayed) |
| **A2.5** | Asymmetric pass-through | Compare pass-through for cost increases vs decreases |

#### 2.6 Data Preparation

**Row Granularity:** One row per Product × Division × Quarter Transition

| Column | Source | Description |
|--------|--------|-------------|
| `item_code` | Pricing File | Item identifier |
| `item_name` | Pricing File | Product name |
| `brand` | Pricing File | Brand Label Name |
| `category` | Pricing File | Category |
| `division` | Derived | Division code |
| `period` | Derived | Transition period (Q1→Q2, Q2→Q3, Q3→Q4) |
| `list_cost_before` | Pricing File | List Cost at start of period |
| `list_cost_after` | Pricing File | List Cost at end of period |
| `list_cost_change` | Calculated | Absolute change |
| `list_cost_change_pct` | Calculated | Percentage change |
| `bsp_before` | Pricing File | BSP at start of period |
| `bsp_after` | Pricing File | BSP at end of period |
| `bsp_change` | Calculated | Absolute change |
| `bsp_change_pct` | Calculated | Percentage change |
| `pass_through_rate` | Calculated | BSP change / List Cost change |

**Preparation Steps:**
```
1. Melt pricing data to long format
2. Create lagged values for List Cost, BSP, SRP
3. Calculate period-over-period changes
4. Filter to items with non-zero cost changes
5. Calculate pass-through metrics
```

---

### RQ3: Price Elasticity Analysis

#### 3.1 Research Question
**How do price changes affect sales volume? What is the price elasticity of demand for AWG brands?**

#### 3.2 Granularity

| Level | Description |
|-------|-------------|
| **Primary** | Product × Division Level |
| **Aggregation** | Category, Brand |

#### 3.3 Sub-Dimensions

| Dimension | Values/Segments |
|-----------|-----------------|
| **Product** | Items with both pricing and sales data |
| **Brand** | Best Choice, Always Save, National Brand |
| **Category** | Product categories |
| **Division** | 9 AWG divisions |
| **Time** | Quarter-over-quarter |
| **Price Change Direction** | Increase, Decrease, No Change |

#### 3.4 Metrics Needed

| Metric | Formula | Unit |
|--------|---------|------|
| Price (BSP or SRP) | Selling price | $ |
| Sales ($) | Dollar sales | $ |
| Sales (Units) | Billed Case Quantity | Cases |
| Price Change % | (Price(Qt) - Price(Qt-1)) / Price(Qt-1) × 100 | % |
| Sales Change % | (Sales(Qt) - Sales(Qt-1)) / Sales(Qt-1) × 100 | % |
| **Price Elasticity** | Sales Change % / Price Change % | Ratio |
| **Arc Elasticity** | [(Q2-Q1)/(Q2+Q1)] / [(P2-P1)/(P2+P1)] | Ratio |

#### 3.5 Analyses

| Analysis | Description | Output |
|----------|-------------|--------|
| **A3.1** | Overall elasticity distribution | Histogram, summary statistics |
| **A3.2** | Elasticity by brand | Comparison (BC vs AS vs National) |
| **A3.3** | Elasticity by category | Identify elastic vs inelastic categories |
| **A3.4** | Elasticity by price change magnitude | Small (<5%) vs Large (>10%) changes |
| **A3.5** | Regression analysis | Price → Sales relationship with controls |

#### 3.6 Data Preparation

**Row Granularity:** One row per Product × Division × Quarter

| Column | Source | Description |
|--------|--------|-------------|
| `item_code` | Both Files | Item identifier (join key) |
| `item_name` | Pricing File | Product name |
| `brand` | Pricing File | Brand Label Name |
| `category` | Pricing File | Category |
| `division` | Both Files | Division code |
| `quarter` | Derived | Q1, Q2, Q3, Q4 |
| `bsp` | Pricing File | Base Selling Price |
| `city_srp` | Pricing File | City SRP |
| `sales_dollars` | Sales File | $ Sales |
| `sales_units` | Sales File | Billed Case Quantity |
| `price_change_pct` | Calculated | QoQ price change |
| `sales_change_pct` | Calculated | QoQ sales change |
| `elasticity` | Calculated | Sales change % / Price change % |

**Preparation Steps:**
```
1. Merge pricing and sales data on Item Code + Division
2. Reshape to long format (by quarter)
3. Calculate QoQ changes for price and sales
4. Filter to items with price changes (avoid division by zero)
5. Calculate elasticity metrics
6. Remove outliers (elasticity > |10|)
```

---

### RQ4: Cross-Brand Effects Analysis

#### 4.1 Research Question
**What are the cross-brand effects between Best Choice and Always Save? Does a price change in one brand affect sales of the other?**

#### 4.2 Granularity

| Level | Description |
|-------|-------------|
| **Primary** | Category × Division Level |
| **Aggregation** | Overall brand-level |

#### 4.3 Sub-Dimensions

| Dimension | Values/Segments |
|-----------|-----------------|
| **Category** | Categories with BOTH Best Choice AND Always Save products |
| **Division** | 9 AWG divisions |
| **Brand Pair** | BC ↔ AS interaction |
| **Time** | Quarter-over-quarter |
| **Price Relationship** | BC price vs AS price |

#### 4.4 Metrics Needed

| Metric | Formula | Unit |
|--------|---------|------|
| BC Category Price | Average BSP of BC items in category | $ |
| AS Category Price | Average BSP of AS items in category | $ |
| BC Category Sales | Total sales of BC items in category | $ |
| AS Category Sales | Total sales of AS items in category | $ |
| BC-AS Price Gap | (BC Price - AS Price) / AS Price × 100 | % |
| **Cross-Elasticity (BC→AS)** | AS Sales Change % / BC Price Change % | Ratio |
| **Cross-Elasticity (AS→BC)** | BC Sales Change % / AS Price Change % | Ratio |

#### 4.5 Analyses

| Analysis | Description | Output |
|----------|-------------|--------|
| **A4.1** | Identify categories with both BC and AS | Category list with item counts |
| **A4.2** | BC-AS price gap by category | Distribution, ranked table |
| **A4.3** | Cross-elasticity estimation | Regression: AS sales ~ BC price (and vice versa) |
| **A4.4** | Substitution patterns | When BC price ↑, does AS sales ↑? |
| **A4.5** | Category-specific cross-effects | Which categories show strongest substitution? |

#### 4.6 Data Preparation

**Row Granularity:** One row per Category × Division × Quarter × Brand

| Column | Source | Description |
|--------|--------|-------------|
| `category` | Pricing File | Category name |
| `division` | Derived | Division code |
| `quarter` | Derived | Q1, Q2, Q3, Q4 |
| `brand` | Pricing File | BC or AS |
| `avg_bsp` | Calculated | Average BSP in category |
| `total_sales` | Calculated | Total $ sales in category |
| `total_units` | Calculated | Total units in category |
| `item_count` | Calculated | Number of items |

**Then pivot to wide format:**

| Column | Description |
|--------|-------------|
| `bc_avg_bsp` | Best Choice average price |
| `as_avg_bsp` | Always Save average price |
| `bc_sales` | Best Choice sales |
| `as_sales` | Always Save sales |
| `bc_as_price_gap` | Price difference |

**Preparation Steps:**
```
1. Filter to categories containing BOTH Best Choice AND Always Save
2. Merge pricing and sales data
3. Aggregate to Category × Division × Quarter × Brand level
4. Pivot to have BC and AS metrics side by side
5. Calculate cross-brand metrics and lags
```

---

### RQ5: Geographic Price Variation Analysis

#### 5.1 Research Question
**How do prices and pricing strategies vary across AWG's geographic divisions?**

#### 5.2 Granularity

| Level | Description |
|-------|-------------|
| **Primary** | Division Level |
| **Drill-down** | Product, Category |

#### 5.3 Sub-Dimensions

| Dimension | Values/Segments |
|-----------|-----------------|
| **Division** | KC, SP, OK, NA, GC, NE, GL, HN, UM |
| **Region** | Central (KC, SP), South (OK, GC), Southeast (NA, HN), North (NE, GL, UM) |
| **Price Type** | List Cost, BSP, City SRP, Rural SRP |
| **Brand** | Best Choice, Always Save, National Brand |

#### 5.4 Metrics Needed

| Metric | Formula | Unit |
|--------|---------|------|
| Avg BSP by Division | Mean BSP for division | $ |
| Avg SRP by Division | Mean SRP for division | $ |
| City-Rural SRP Gap | (Rural SRP - City SRP) / City SRP × 100 | % |
| Division Price Index | Division Avg Price / Overall Avg Price × 100 | Index |
| **Price Variation (CV)** | Std Dev / Mean across divisions | % |
| Markup % | (SRP - BSP) / BSP × 100 | % |

#### 5.5 Analyses

| Analysis | Description | Output |
|----------|-------------|--------|
| **A5.1** | Average price comparison across divisions | Bar chart, table |
| **A5.2** | Price variation (coefficient of variation) by product | Identify high-variation items |
| **A5.3** | List Cost consistency verification | Should be same across divisions |
| **A5.4** | City vs Rural SRP analysis | Gap analysis by division |
| **A5.5** | Markup analysis by division | BSP to SRP markup comparison |
| **A5.6** | Regional clustering | Group divisions by pricing patterns |

#### 5.6 Data Preparation

**Row Granularity:** One row per Product × Division (or aggregated to Division level)

| Column | Source | Description |
|--------|--------|-------------|
| `item_code` | Pricing File | Item identifier |
| `category` | Pricing File | Category |
| `brand` | Pricing File | Brand Label Name |
| `division` | Derived | Division code |
| `region` | Derived | Regional grouping |
| `list_cost` | Pricing File | List Cost (should be same) |
| `bsp` | Pricing File | BSP |
| `city_srp` | Pricing File | City SRP |
| `rural_srp` | Pricing File | Rural SRP |
| `bsp_markup` | Calculated | (BSP - List Cost) / List Cost |
| `srp_markup` | Calculated | (SRP - BSP) / BSP |

**Preparation Steps:**
```
1. Melt pricing data to long format by division
2. Add regional grouping
3. Calculate markup metrics
4. Aggregate as needed for division-level summaries
5. Calculate cross-division statistics (CV, range, etc.)
```

---

### RQ6: Tariff Impact Detection Analysis

#### 6.1 Research Question
**Which product categories experienced significant price changes that may indicate tariff impacts?**

#### 6.2 Granularity

| Level | Description |
|-------|-------------|
| **Primary** | Category Level |
| **Drill-down** | Product Level |

#### 6.3 Sub-Dimensions

| Dimension | Values/Segments |
|-----------|-----------------|
| **Category** | All categories, focus on tariff-sensitive (Coffee, Oils, Chocolate) |
| **Time Period** | Q1→Q2, Q2→Q3, Q3→Q4 |
| **Price Type** | List Cost (supplier), BSP (wholesale) |
| **Change Magnitude** | Small (<5%), Medium (5-10%), Large (>10%) |

#### 6.4 Metrics Needed

| Metric | Formula | Unit |
|--------|---------|------|
| List Cost Change % | QoQ percentage change | % |
| BSP Change % | QoQ percentage change | % |
| Category Avg Change | Mean change across items in category | % |
| % Items with Change | Items changed / Total items × 100 | % |
| **Change Magnitude** | Absolute value of change | % |
| **Anomaly Score** | (Category Change - Overall Avg) / Std Dev | Z-score |

#### 6.5 Analyses

| Analysis | Description | Output |
|----------|-------------|--------|
| **A6.1** | Overall price change distribution by quarter | Histogram per period |
| **A6.2** | Categories with largest price increases | Ranked table |
| **A6.3** | Timing analysis | Which quarter had most changes? |
| **A6.4** | Tariff-sensitive category deep dive | Coffee, Oils, Chocolate detailed analysis |
| **A6.5** | Anomaly detection | Flag unusual price movements |
| **A6.6** | Cost vs Retail price change comparison | Did cost increases reach consumers? |

#### 6.6 Data Preparation

**Row Granularity:** One row per Product × Quarter Transition

| Column | Source | Description |
|--------|--------|-------------|
| `item_code` | Pricing File | Item identifier |
| `item_name` | Pricing File | Product name |
| `category` | Pricing File | Category |
| `brand` | Pricing File | Brand Label Name |
| `period` | Derived | Q1→Q2, Q2→Q3, Q3→Q4 |
| `list_cost_change_pct` | Calculated | List Cost % change |
| `bsp_change_pct` | Calculated | BSP % change |
| `srp_change_pct` | Calculated | SRP % change |
| `change_flag` | Calculated | 1 if any price changed |
| `tariff_sensitive` | Derived | 1 if in sensitive category |

**Preparation Steps:**
```
1. Calculate QoQ changes for all price fields
2. Flag tariff-sensitive categories (Coffee, Oils, Chocolate, etc.)
3. Aggregate to category level for summary statistics
4. Calculate anomaly scores
5. Identify outlier categories/products
```

---

## 3. Data Preparation Summary

### 3.1 Master Data Tables Required

| Table Name | Grain | Key Columns | Row Count (Est.) |
|------------|-------|-------------|------------------|
| `product_master` | Item | Item Code, Name, Category, Brand, National Link | ~4,300 |
| `pricing_long` | Item × Division × Quarter | Item Code, Division, Quarter, List Cost, BSP, SRP | ~155,000 |
| `sales_long` | Item × Division × Quarter | Item Code, Division, Quarter, Sales $, Units | ~155,000 |
| `pricing_sales_merged` | Item × Division × Quarter | All pricing + sales columns | ~155,000 |
| `price_changes` | Item × Division × Period | Before/After prices, Change metrics | ~116,000 |
| `category_summary` | Category × Division × Quarter × Brand | Aggregated metrics | ~3,200 |

### 3.2 Data Transformation Pipeline

```
Step 1: Load & Clean
├── Load pricing file (header=3)
├── Load sales files (header=2, all sheets)
├── Clean brand labels (.str.strip())
└── Correct sheet names (GO→NA, NO→NE)

Step 2: Reshape Pricing
├── Separate product attributes (cols 1-13)
├── Melt pricing columns to long format
├── Parse Division, Quarter, Price Type from column names
└── Output: pricing_long table

Step 3: Reshape Sales
├── Stack all division sheets
├── Melt sales columns to long format
├── Parse Quarter from column names
└── Output: sales_long table

Step 4: Merge & Enrich
├── Join pricing_long + sales_long on Item Code, Division, Quarter
├── Join National Brand prices for linked items
├── Calculate derived metrics (gaps, changes, elasticity)
└── Output: pricing_sales_merged table

Step 5: Aggregate
├── Create category-level summaries
├── Create division-level summaries
├── Create time-series datasets
└── Output: Various summary tables
```

### 3.3 Key Join Relationships

```
pricing_file.Item Code  ──────────────────────> sales_file.Item Code
pricing_file.National Comparison Item Code ──> pricing_file.Item Code (self-join)
pricing_file.Division (parsed) ───────────────> sales_file.Division (corrected)
```

---

## 4. Analysis Execution Sequence

### Phase 1: Data Quality & Preparation (Week 1)
- [ ] Complete data quality report
- [ ] Clean and reshape all data
- [ ] Create master tables
- [ ] Validate joins and completeness

### Phase 2: Descriptive Analysis (Week 2)
- [ ] RQ1: Price gap analysis
- [ ] RQ5: Geographic variation analysis
- [ ] RQ6: Tariff detection (descriptive)

### Phase 3: Analytical Modeling (Weeks 3-4)
- [ ] RQ2: Cost pass-through analysis
- [ ] RQ3: Price elasticity estimation
- [ ] RQ4: Cross-brand effects

### Phase 4: Synthesis & Recommendations (Week 5)
- [ ] Integrate findings across analyses
- [ ] Develop pricing recommendations
- [ ] Prepare final presentation

---

## Appendix: Key Category Focus Areas

Based on project discussions, prioritize these categories:

| Category | Reason | Expected Analysis |
|----------|--------|-------------------|
| **Coffee & Creamers** | Tariff-sensitive | Price change detection, elasticity |
| **Oils/Shortenings** | High volatility noted | Pass-through, geographic variation |
| **Chocolate/Baking** | Hershey's example | Brand comparison, price gaps |
| **Canned Vegetables** | High volume | Elasticity, cross-brand effects |
| **Paper Products** | Staple category | Geographic variation |

---

*Document prepared for AWG Brands Pricing Analysis - U of I Spring 2026 Project*
