
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

# Load dataset
file_path = DATA_DIR / "olist_products_dataset.csv"
df = pd.read_csv(file_path)

print("=== PRODUCTS DATASET REPORT ===")

# Basic information
print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Duplicates
print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate Product IDs:")
print(df["product_id"].duplicated().sum())

print("\nUnique Product IDs:")
print(df["product_id"].nunique())

# Numeric columns validation
numeric_columns = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

print("\n=== NUMERIC COLUMNS VALIDATION ===")

for column in numeric_columns:
    print(f"\n{column}")
    print("Negative Values:", (df[column] < 0).sum())
    print("Zero Values:", (df[column] == 0).sum())

# Category analysis
print("\n=== PRODUCT CATEGORY ANALYSIS ===")

print("Unique Categories:",
      df["product_category_name"].nunique())

print("\nTop 10 Categories:")
print(df["product_category_name"].value_counts().head(10))

print("\nMissing Categories:",
      df["product_category_name"].isnull().sum())
