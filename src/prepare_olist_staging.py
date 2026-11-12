
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
STAGING_DIR = BASE_DIR / "data" / "staging"

STAGING_DIR.mkdir(parents=True, exist_ok=True)

# Primary keys / composite keys used for validation
TABLES = {
    "customers": {
        "file": "olist_customers_dataset.csv",
        "keys": ["customer_id"],
    },
    "orders": {
        "file": "olist_orders_dataset.csv",
        "keys": ["order_id"],
    },
    "order_items": {
        "file": "olist_order_items_dataset.csv",
        "keys": ["order_id", "order_item_id"],
    },
    "order_payments": {
        "file": "olist_order_payments_dataset.csv",
        "keys": ["order_id", "payment_sequential"],
    },
    "order_reviews": {
        "file": "olist_order_reviews_dataset.csv",
        "keys": ["review_id", "order_id"],
    },
    "products": {
        "file": "olist_products_dataset.csv",
        "keys": ["product_id"],
    },
    "sellers": {
        "file": "olist_sellers_dataset.csv",
        "keys": ["seller_id"],
    },
    "geolocation": {
        "file": "olist_geolocation_dataset.csv",
        "keys": [],
    },
    "category_translation": {
        "file": "product_category_name_translation.csv",
        "keys": ["product_category_name"],
    },
}

DATE_COLUMNS = {
    "orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_reviews": [
        "review_creation_date",
        "review_answer_timestamp",
    ],
}

NUMERIC_COLUMNS = {
    "order_items": [
        "order_item_id",
        "price",
        "freight_value",
    ],
    "order_payments": [
        "payment_sequential",
        "payment_installments",
        "payment_value",
    ],
    "order_reviews": ["review_score"],
    "products": [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
    "geolocation": [
        "geolocation_lat",
        "geolocation_lng",
    ],
}

validation_results = {}
prepared_tables = {}

for table_name, config in TABLES.items():

    file_path = RAW_DIR / config["file"]

    # Read as strings to preserve IDs and ZIP prefixes
    df = pd.read_csv(file_path, dtype="string")

    raw_rows = len(df)

    # Standardize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Standardize text values
    text_columns = df.select_dtypes(
        include=["string", "object"]
    ).columns

    for column in text_columns:
        df[column] = df[column].str.strip()
        df[column] = df[column].replace("", pd.NA)

    # Convert date columns
    for column in DATE_COLUMNS.get(table_name, []):
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    # Convert numeric columns
    for column in NUMERIC_COLUMNS.get(table_name, []):
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Standardize Brazilian ZIP code prefixes
    zip_columns = [
        column for column in df.columns
        if column.endswith("zip_code_prefix")
    ]

    for column in zip_columns:
        df[column] = df[column].str.zfill(5)

    # Validation checks
    keys = config["keys"]

    if keys:
        missing_key_rows = df[keys].isna().any(axis=1).sum()
        duplicate_key_rows = df.duplicated(
            subset=keys
        ).sum()
    else:
        missing_key_rows = 0
        duplicate_key_rows = 0

    exact_duplicate_rows = df.duplicated().sum()
    missing_values = int(df.isna().sum().sum())

    invalid_review_scores = 0

    if table_name == "order_reviews":
        invalid_review_scores = (
            ~df["review_score"].between(1, 5)
        ).sum()

    validation_results[table_name] = {
        "raw_rows": raw_rows,
        "staging_rows": len(df),
        "missing_values": missing_values,
        "missing_key_rows": int(missing_key_rows),
        "duplicate_key_rows": int(duplicate_key_rows),
        "exact_duplicate_rows": int(exact_duplicate_rows),
        "invalid_review_scores": int(invalid_review_scores),
    }

    prepared_tables[table_name] = df

# Add English category names to products
products = prepared_tables["products"]
translation = prepared_tables["category_translation"]

products = products.merge(
    translation[
        ["product_category_name", "product_category_name_english"]
    ],
    on="product_category_name",
    how="left",
    validate="many_to_one",
)

prepared_tables["products"] = products

# Save all staging tables
for table_name, df in prepared_tables.items():
    output_path = (
        STAGING_DIR / f"olist_{table_name}_staging.csv"
    )
    df.to_csv(output_path, index=False)

# Save validation report
report = pd.DataFrame.from_dict(
    validation_results,
    orient="index"
)
report.index.name = "table"

report_path = STAGING_DIR / "validation_report.csv"
report.to_csv(report_path)

print("=== OLIST STAGING PIPELINE ===")
print(report.to_string())
print("\nStaging files saved to:", STAGING_DIR)
print("Validation report:", report_path)
