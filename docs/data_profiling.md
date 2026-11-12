# Olist E-Commerce Dataset — Data Profiling Report

## 1. Project Overview

This report documents the initial exploration and profiling of the Olist Brazilian E-Commerce dataset.

The purpose of this stage is to understand the structure, size, data types, missing values, duplicates, and initial data quality observations for each source file.

**Important:** This stage is for inspection only. No source data has been modified, cleaned, or deleted. All original CSV files are preserved in `data/raw`.

## 2. Dataset Inventory

The project contains nine source CSV files:

| Dataset | Rows | Columns |
|---|---:|---:|
| Customers | 99,441 | 5 |
| Orders | 99,441 | 8 |
| Order Items | 112,650 | 7 |
| Order Payments | 103,886 | 5 |
| Order Reviews | 99,224 | 7 |
| Products | 32,951 | 9 |
| Sellers | 3,095 | 4 |
| Geolocation | 1,000,163 | 5 |
| Category Translation | 71 | 2 |

## 3. Individual Dataset Profiling

### 3.1 Customers

**File:** `olist_customers_dataset.csv`

- Shape: 99,441 rows × 5 columns.
- Columns: `customer_id`, `customer_unique_id`, `customer_zip_code_prefix`, `customer_city`, `customer_state`.
- Missing values: None.
- Duplicate rows: 0.
- Duplicate `customer_id` values: 0.
- Unique `customer_unique_id` values: 96,096.

**Observation:** `customer_id` and `customer_unique_id` represent different identifiers. The latter has fewer unique values than the number of records.

### 3.2 Orders

**File:** `olist_orders_dataset.csv`

- Shape: 99,441 rows × 8 columns.
- Missing values:
  - `order_approved_at`: 160.
  - `order_delivered_carrier_date`: 1,783.
  - `order_delivered_customer_date`: 2,965.
- Duplicate rows: 0.
- Duplicate `order_id` values: 0.

**Order status distribution:**

| Status | Count |
|---|---:|
| delivered | 96,478 |
| shipped | 1,107 |
| canceled | 625 |
| unavailable | 609 |
| invoiced | 314 |
| processing | 301 |
| created | 5 |
| approved | 2 |

**Validation observations:**
- 8 delivered orders have no customer delivery timestamp.
- No orders were found with a delivery date earlier than the purchase date.
- 7,826 delivered orders have a delivery timestamp later than the estimated delivery date.

These findings require consideration during data quality validation. Late deliveries are business observations and are not automatically data errors.

### 3.3 Order Items

**File:** `olist_order_items_dataset.csv`

- Shape: 112,650 rows × 7 columns.
- Missing values: None.
- Duplicate rows: 0.
- Duplicate composite keys (`order_id`, `order_item_id`): 0.
- Unique orders: 98,666.
- Non-positive prices: 0.
- Negative freight values: 0.
- Invalid shipping dates after conversion: 0.

**Observation:** An order can contain multiple items. Therefore, `order_id` alone should not be treated as a unique row identifier in this dataset.

### 3.4 Order Payments

**File:** `olist_order_payments_dataset.csv`

- Shape: 103,886 rows × 5 columns.
- Missing values: None.
- Duplicate rows: 0.
- Duplicate composite keys (`order_id`, `payment_sequential`): 0.
- Unique orders: 99,440.

**Payment type distribution:**

| Payment Type | Count |
|---|---:|
| credit_card | 76,795 |
| boleto | 19,784 |
| voucher | 5,775 |
| debit_card | 1,529 |
| not_defined | 3 |

**Validation observations:**
- 9 records have a payment value of zero.
- 2 records have zero installments despite having positive credit card payment values.
- The 3 `not_defined` payment records also have zero payment values.

These records are flagged for further review. No automatic correction or deletion has been performed.

### 3.5 Order Reviews

**File:** `olist_order_reviews_dataset.csv`

- Shape: 99,224 rows × 7 columns.
- Missing review titles: 87,656.
- Missing review messages: 58,247.
- Other columns: No missing values.
- Duplicate complete rows: 0.
- Review score values outside the 1–5 range: 0.
- Unique orders: 98,673.

**Key observations:**
- 814 duplicate occurrences of `review_id` were detected.
- These occurrences belong to 789 duplicated `review_id` groups, involving 1,603 rows.
- The same `review_id` can be associated with multiple orders in the source data.
- 547 orders have multiple review records.

Missing review text may occur when customers submit a rating without writing a comment.

The uniqueness of `review_id` requires further investigation before defining the table's key.

### 3.6 Products

**File:** `olist_products_dataset.csv`

- Shape: 32,951 rows × 9 columns.
- Duplicate rows: 0.
- Duplicate `product_id` values: 0.
- Unique products: 32,951.
- Unique product categories: 73.

**Missing values:**

| Column | Missing Count |
|---|---:|
| product_category_name | 610 |
| product_name_lenght | 610 |
| product_description_lenght | 610 |
| product_photos_qty | 610 |
| product_weight_g | 2 |
| product_length_cm | 2 |
| product_height_cm | 2 |
| product_width_cm | 2 |

**Additional observations:**
- All 610 records missing descriptive information are missing the same four descriptive fields.
- 2 products have missing weight and dimension information.
- 4 products have a weight of zero.
- No negative values were detected in the checked numeric fields.

These records will be retained and reviewed during the preparation stage.

### 3.7 Sellers

**File:** `olist_sellers_dataset.csv`

- Shape: 3,095 rows × 4 columns.
- Missing values: None.
- Duplicate rows: 0.
- Duplicate `seller_id` values: 0.
- Unique sellers: 3,095.
- Unique cities: 611.
- Unique states: 23.
- Zero ZIP code prefixes: 0.

**Top seller states:**

| State | Seller Count |
|---|---:|
| SP | 1,849 |
| PR | 349 |
| MG | 244 |
| SC | 190 |
| RJ | 171 |
| RS | 129 |
| GO | 40 |
| DF | 30 |
| ES | 23 |
| BA | 19 |

No critical issues were identified in the initial checks.

### 3.8 Geolocation

**File:** `olist_geolocation_dataset.csv`

- Shape: 1,000,163 rows × 5 columns.
- Missing values: None.
- Exact duplicate rows: 261,831.
- Rows involved in duplicate groups: 390,005.
- Unique ZIP code prefixes: 19,015.
- Unique cities: 8,011.
- Unique states: 27.

**Coordinate validation:**
- Invalid latitude values outside the -90 to 90 range: 0.
- Invalid longitude values outside the -180 to 180 range: 0.
- 42 records fall outside the approximate Brazil coordinate bounds used in the initial check.

**Additional observations:**
- 17,781 ZIP code prefixes have more than one distinct coordinate.
- Multiple coordinates for a ZIP code are not automatically considered invalid.
- The 42 outside-bounds records require further geographic validation. The approximate bounds are a screening check, not a definitive test of data correctness.

No rows have been removed.

### 3.9 Category Translation

**File:** `product_category_name_translation.csv`

- Shape: 71 rows × 2 columns.
- Missing values: None.
- Duplicate rows: 0.
- Duplicate Portuguese category names: 0.
- Unique Portuguese categories: 71.
- Unique English categories: 71.

**Comparison with Products:**
- Products contains 73 unique categories.
- The translation file contains 71 categories.
- 2 product categories have no translation:
  - `pc_gamer`
  - `portateis_cozinha_e_preparadores_de_alimentos`
- No translation categories were found that are absent from Products.

The two untranslated categories will be retained without inventing translations.

## 4. Conclusion

The initial profiling of all nine source datasets has been completed.

The exploration identified missing values, duplicate records, unusual numeric values, key uniqueness concerns, and geographic validation observations.

These findings will guide the next stages:

1. Validate primary and foreign key relationships between datasets.
2. Define data quality and cleaning rules.
3. Prepare cleaned data separately while preserving the original raw files.
4. Document and test the ingestion and transformation process.

**Current status:** Initial profiling completed. No cleaning or modification of raw source data has been performed.