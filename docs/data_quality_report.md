# Olist E-Commerce Dataset — Data Quality Report

## 1. Purpose

This report documents the data quality issues and observations identified during the initial profiling of the Olist Brazilian E-Commerce dataset.

The purpose is to record potential issues, assess their impact, and define recommendations for the next data preparation stage.

**Important:** No cleaning, deletion, or modification has been applied to the original CSV files. All findings below are based on the initial exploration and validation checks.

## 2. Summary of Findings

| Dataset | Finding | Severity / Status |
|---|---|---|
| Customers | No missing values or duplicate IDs found | No issue identified in initial checks |
| Orders | Missing timestamps in several records | Requires review |
| Orders | 8 delivered orders missing customer delivery timestamps | Requires review |
| Orders | 7,826 deliveries later than estimated dates | Business observation |
| Order Items | No issues in tested fields or composite key | No issue identified in initial checks |
| Order Payments | 9 zero payment values | Requires review |
| Order Payments | 2 zero installment values with positive credit card payments | Suspicious values |
| Order Reviews | Duplicate review IDs across different orders | Key uniqueness concern |
| Order Reviews | Missing review titles and messages | Source data observation |
| Products | 610 products missing four descriptive fields | Missing information |
| Products | 2 products missing weight and dimensions | Missing shipping attributes |
| Products | 4 products with zero weight | Requires review |
| Sellers | No issues found in initial checks | No issue identified |
| Geolocation | 261,831 exact duplicate rows | High-priority review |
| Geolocation | 42 records outside approximate Brazil bounds | Geographic validation required |
| Geolocation | 17,781 ZIP codes have multiple distinct coordinates | Requires investigation |
| Category Translation | 2 product categories have no English translation | Mapping gap |

## 3. Detailed Findings and Recommendations

### 3.1 Orders

**Findings:**
- 160 missing `order_approved_at` values.
- 1,783 missing `order_delivered_carrier_date` values.
- 2,965 missing `order_delivered_customer_date` values.
- 8 orders marked as `delivered` have no customer delivery timestamp.
- 7,826 delivered orders have actual delivery dates later than estimated delivery dates.

**Recommendations:**
- Investigate missing timestamps in relation to `order_status`.
- Preserve missing values when no reliable replacement is available.
- Do not treat late deliveries as data errors automatically; they represent potentially useful business information.

### 3.2 Order Payments

**Findings:**
- 9 records have `payment_value = 0`.
- 3 of these records have `payment_type = not_defined`.
- 2 credit card records have zero installments but positive payment values.

**Recommendations:**
- Investigate zero payment values and payment types.
- Review zero installment records before deciding whether they need correction.
- Do not delete or replace these values without an agreed business rule.

### 3.3 Order Reviews

**Findings:**
- 87,656 missing review titles.
- 58,247 missing review messages.
- 789 duplicated `review_id` groups involving 1,603