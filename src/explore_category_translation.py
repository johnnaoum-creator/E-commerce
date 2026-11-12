
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

translation_path = DATA_DIR / "product_category_name_translation.csv"
products_path = DATA_DIR / "olist_products_dataset.csv"

translation = pd.read_csv(translation_path)
products = pd.read_csv(products_path)

print("=== CATEGORY TRANSLATION DATASET REPORT ===")

print("\nDataset Shape:")
print(translation.shape)

print("\nColumns:")
print(translation.columns.tolist())

print("\nFirst 5 Rows:")
print(translation.head())

print("\nData Types:")
print(translation.dtypes)

print("\nMissing Values:")
print(translation.isnull().sum())

print("\nDuplicate Rows:")
print(translation.duplicated().sum())

print("\nDuplicate Category Names:")
print(
    translation["product_category_name"].duplicated().sum()
)

print("\nUnique Portuguese Categories:")
print(translation["product_category_name"].nunique())

print("\nUnique English Categories:")
print(translation["product_category_name_english"].nunique())

# Compare categories with products dataset
print("\n=== PRODUCTS CATEGORY COMPARISON ===")

product_categories = set(
    products["product_category_name"].dropna().unique()
)

translated_categories = set(
    translation["product_category_name"].dropna().unique()
)

missing_translation = product_categories - translated_categories
unused_translations = translated_categories - product_categories

print("Unique categories in products:", len(product_categories))
print("Unique categories in translation:", len(translated_categories))

print("\nProduct categories without translation:")
print(len(missing_translation))
print(sorted(missing_translation))

print("\nTranslation categories not found in products:")
print(len(unused_translations))
print(sorted(unused_translations))

print("\n=== INVESTIGATION COMPLETED ===")
