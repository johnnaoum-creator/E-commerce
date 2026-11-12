
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

file_path = DATA_DIR / "olist_products_dataset.csv"
df = pd.read_csv(file_path)

# Columns with missing values
missing_columns = [
    "product_category_name",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty"
]

# Check whether the same 610 rows are missing all four fields
all_four_missing = df[missing_columns].isnull().all(axis=1)

print("=== MISSING PRODUCT INFORMATION ===")
print("Rows missing all four fields:", all_four_missing.sum())

print("\nRows missing some but not all four fields:",
      (df[missing_columns].isnull().any(axis=1) & ~all_four_missing).sum())

# Inspect products with missing weight or dimensions
dimension_columns = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

missing_dimensions = df[dimension_columns].isnull().any(axis=1)

print("\n=== PRODUCTS WITH MISSING WEIGHT OR DIMENSIONS ===")
print("Number of affected products:", missing_dimensions.sum())

print(df.loc[missing_dimensions].to_string(index=False))

# Inspect products with zero weight
zero_weight = df["product_weight_g"].eq(0)

print("\n=== PRODUCTS WITH ZERO WEIGHT ===")
print("Number of products:", zero_weight.sum())

print(df.loc[zero_weight].to_string(index=False))

# Check overlap between missing dimensions and zero weight
print("\n=== OVERLAP CHECK ===")
print(
    "Products with missing dimensions AND zero weight:",
    (missing_dimensions & zero_weight).sum()
)
