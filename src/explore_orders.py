
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

file_path = DATA_DIR / "olist_orders_dataset.csv"

df = pd.read_csv(file_path)

print("=== ORDERS DATASET REPORT ===")

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate Order IDs:")
print(df["order_id"].duplicated().sum())

print("\nOrder Status Distribution:")
print(df["order_status"].value_counts())

# Check missing dates by order status
print("\n=== MISSING DATES BY ORDER STATUS ===")

date_columns = [
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date"
]

for column in date_columns:
    print(f"\n{column}:")
    print(
        df.groupby("order_status")[column]
        .apply(lambda x: x.isnull().sum())
    )

# Convert date columns to datetime
print("\n=== DATE TYPE CONVERSION ===")

for column in date_columns + [
    "order_purchase_timestamp",
    "order_estimated_delivery_date"
]:
    df[column] = pd.to_datetime(df[column], errors="coerce")

print(df.dtypes)

print("\n=== BUSINESS RULE VALIDATION ===")

# Rule 1: Delivered orders without delivery date
delivered_missing_date = df[
    (df["order_status"] == "delivered") &
    (df["order_delivered_customer_date"].isna())
]

print("\nDelivered orders without delivery date:")
print(len(delivered_missing_date))

# Rule 2: Delivery before purchase
invalid_dates = df[
    df["order_delivered_customer_date"] <
    df["order_purchase_timestamp"]
]

print("\nDelivery before purchase:")
print(len(invalid_dates))

# Rule 3: Orders delivered after estimated date
late_orders = df[
    (df["order_status"] == "delivered") &
    (df["order_delivered_customer_date"] >
     df["order_estimated_delivery_date"])
]

print("\nLate delivered orders:")
print(len(late_orders))
print("\n=== INVESTIGATE MISSING DELIVERY DATES ===")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(
    delivered_missing_date[
        [
            "order_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    ].to_string(index=False)
)
print("\n=== ORDERS DATA QUALITY SUMMARY ===")

print("Total Orders:", len(df))
print("Duplicate Order IDs:", df["order_id"].duplicated().sum())

print(
    "Delivered Orders Missing Delivery Date:",
    len(delivered_missing_date)
)

print("Late Delivered Orders:", len(late_orders))

print(
    "Invalid Delivery Before Purchase:",
    len(invalid_dates)
)

