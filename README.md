# E-commerce
# E-Commerce Data Engineering Project

## Project Overview

This project focuses on building a data engineering pipeline using the Brazilian E-Commerce Public Dataset by Olist.

The first stage covers data ingestion, data exploration, quality validation, standardization, and preparation of raw data for downstream processing.

External economic data is also collected from the World Bank API to enrich the project.

## Data Sources

### Olist Dataset
- Customers
- Orders
- Order Items
- Order Payments
- Order Reviews
- Products
- Sellers
- Geolocation
- Product Category Translation

### World Bank API
Brazilian economic indicators (2016–2018):
- Population
- GDP (current US$)
- Annual Inflation Rate (%)

## Technologies

- Python
- Pandas
- Requests
- REST APIs
- Git & GitHub

## Project Structure

```text
E-commerce/
├── data/
│   ├── raw/
│   │   └── external/
│   ├── staging/
│   └── processed/
├── docs/
├── src/
├── .gitignore
└── README.md
```

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd E-commerce
```

Install the required Python packages:

```bash
pip install pandas requests
```

Place the nine original Olist CSV files inside:

```text
data/raw/
```

The original Olist CSV files are not included in this repository.

## Pipeline Execution

Run the following scripts from the project root directory:

### 1. Extract External Data

```bash
python src/extract_world_bank.py
```

Retrieves Brazil's population, GDP, and inflation indicators from the World Bank API and saves the responses as JSON files.

### 2. Transform External Data

```bash
python src/transform_world_bank.py
```

Transforms the extracted JSON data into a structured CSV file.

### 3. Prepare Olist Data

```bash
python src/prepare_olist_staging.py
```

This step:
- Loads the Olist datasets.
- Standardizes column names and data types.
- Handles whitespace and empty values.
- Preserves identifiers and ZIP code formatting.
- Parses date columns.
- Validates configured keys and duplicate records.
- Translates product category names into English where available.
- Generates staging datasets and a validation report.

## Outputs

- Prepared Olist staging datasets.
- Data validation report.
- World Bank economic data in CSV format.

Generated CSV files and original Olist CSV datasets are excluded from Git.

## Data Quality Notes

- Missing values are retained when they represent legitimate missing information.
- Exact duplicate geolocation records are reported and preserved.
- Review records are validated using the composite key (`review_id`, `order_id`).
- Products without available English category translations are retained.
- No records are arbitrarily deleted during preparation.

For more details, check the documentation in the `docs/` directory.