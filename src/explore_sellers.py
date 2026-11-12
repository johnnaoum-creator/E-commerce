
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

file_path = DATA_DIR / "olist_sellers_dataset.csv"
df = pd.read_csv(file_path)

print("=== SELLERS DATASET REPORT ===")

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

print("\nDuplicate Seller IDs:")
print(df["seller_id"].duplicated().sum())

print("\nUnique Seller IDs:")
print(df["seller_id"].nunique())

print("\n=== ZIP CODE VALIDATION ===")
print("Zero ZIP Codes:",
      (df["seller_zip_code_prefix"] == 0).sum())

print("\n=== LOCATION ANALYSIS ===")
print("Unique Cities:", df["seller_city"].nunique())
print("Unique States:", df["seller_state"].nunique())

print("\nTop 10 Seller States:")
print(df["seller_state"].value_counts().head(10))
