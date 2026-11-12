# Data Ingestion & Preparation – Handoff

## 1. Role Scope

This stage covers data ingestion, cleaning, validation, standardization, and preparation of Olist data for downstream processing.

## 2. Data Sources

### Olist Dataset

The project uses nine original CSV files:

- Customers
- Orders
- Order Items
- Order Payments
- Order Reviews
- Products
- Sellers
- Geolocation
- Product Category Translation

Original Olist files are stored under `data/raw/` and are preserved without modification.

### External API – World Bank

An external source was integrated using the World Bank API to retrieve Brazil's economic indicators for 2016–2018:

- Population
- GDP (current US$)
- Annual Inflation

Extraction script: `src/extract_world_bank.py`

Original API responses are stored as JSON files in `data/raw/external/`.

Transformation script: `src/transform_world_bank.py`

The combined output is saved as:

`data/processed/world_bank_brazil_economic_data.csv`

## 3. Cleaning & Standardization

The staging pipeline is implemented in:

`src/prepare_olist_staging.py`

The pipeline performs the following operations:

- Reads source CSVs while preserving IDs and ZIP code prefixes as strings.
- Standardizes column names.
- Removes leading and trailing whitespace from text values.
- Converts empty strings to missing values.
- Converts date columns to datetime.
- Converts designated numeric columns to numeric types.
- Standardizes Brazilian ZIP code prefixes to five digits.
- Adds English product category names using the translation dataset.

## 4. Validation

The pipeline generates a validation report:

`data/staging/validation_report.csv`

The report includes:

- Raw and staging row counts.
- Missing values.
- Missing key values.
- Duplicate key rows.
- Exact duplicate rows.
- Invalid review scores.

### Important Findings

- All nine Olist tables retain their original row counts after staging.
- No missing primary/composite key values were detected by the configured checks.
- No duplicate configured keys were detected, including the composite key `(review_id, order_id)`.
- Geolocation contains 261,831 exact duplicate rows; these are reported but retained.
- Orders contain missing delivery-related timestamps. These values were preserved rather than arbitrarily filled.
- Review title and message fields contain missing values and were preserved.
- 623 products have no English category value: 610 have no original category, while 13 belong to categories without an English translation.
- Duplicate `review_id` values were investigated separately. The composite `(review_id, order_id)` key is used in staging because the same review ID can appear with different order IDs.

No rows were arbitrarily deleted, and missing values were not filled with invented values.

## 5. Output Structure

```text
src/
├── extract_world_bank.py
├── transform_world_bank.py
├── prepare_olist_staging.py
└── investigate_order_reviews.py

data/
├── raw/
│   └── external/
│       ├── brazil_population_2016_2018.json
│       ├── brazil_gdp_2016_2018.json
│       └── brazil_inflation_2016_2018.json
├── staging/
│   ├── olist_customers_staging.csv
│   ├── olist_orders_staging.csv
│   ├── olist_order_items_staging.csv
│   ├── olist_order_payments_staging.csv
│   ├── olist_order_reviews_staging.csv
│   ├── olist_products_staging.csv
│   ├── olist_sellers_staging.csv
│   ├── olist_geolocation_staging.csv
│   ├── olist_category_translation_staging.csv
│   └── validation_report.csv
└── processed/
    └── world_bank_brazil_economic_data.csv

docs/
├── DAY_02_EXTERNAL_API.md
└── DATA_PREPARATION_HANDOFF.md
```

Generated staging and processed CSV files are excluded from Git and can be recreated using the scripts.

## 6. How to Run

Run these commands from the project root:

```powershell
# Extract external data (requires internet connection)
.\.venv\Scripts\python.exe .\src\extract_world_bank.py

# Transform external data
.\.venv\Scripts\python.exe .\src\transform_world_bank.py

# Prepare and validate all Olist tables
.\.venv\Scripts\python.exe .\src\prepare_olist_staging.py
```

The staging pipeline reads the original Olist CSV files from `data/raw/`.

## 7. Handoff Notes

The staging outputs are ready for the next project stage.

The next team members should review the validation report and decide how to handle business-specific cases, such as missing delivery timestamps, duplicate review IDs, and geolocation duplicates, according to the downstream requirements.

The original raw data should remain unchanged.
