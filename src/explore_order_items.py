import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

file_path = DATA_DIR / "olist_order_items_dataset.csv"

df = pd.read_csv(file_path)

print("=== ORDER ITEMS DATASET REPORT ===")

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
print("\n=== KEY VALIDATION ===")

print(
    "Duplicate Order + Item ID:",
    df.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()
)

print("Unique Orders:", df["order_id"].nunique())


print("\n=== NUMERIC VALIDATION ===")

print("Price <= 0:", (df["price"] <= 0).sum())

print("Freight < 0:", (df["freight_value"] < 0).sum())

print("\nPrice Summary:")
print(df[["price", "freight_value"]].describe())


print("\n=== DATE VALIDATION ===")

df["shipping_limit_date"] = pd.to_datetime(
    df["shipping_limit_date"],
    errors="coerce"
)

print(
    "Invalid Shipping Dates:",
    df["shipping_limit_date"].isna().sum()
)