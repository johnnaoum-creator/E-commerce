
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

# Load dataset
file_path = DATA_DIR / "olist_order_reviews_dataset.csv"
df = pd.read_csv(file_path)

print("=== ORDER REVIEWS DATASET REPORT ===")

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


print("\n=== REVIEW SCORE DISTRIBUTION ===")
print(df["review_score"].value_counts().sort_index())


print("\n=== REVIEW SCORE VALIDATION ===")

print("Scores Below 1:", (df["review_score"] < 1).sum())
print("Scores Above 5:", (df["review_score"] > 5).sum())


print("\n=== KEY VALIDATION ===")

print("Unique Orders:", df["order_id"].nunique())

print("Duplicate Review IDs:", df["review_id"].duplicated().sum())

print("Orders with Multiple Reviews:",
      (df["order_id"].value_counts() > 1).sum())


print("\n=== REVIEW COMMENT ANALYSIS ===")

print("Missing Review Titles:", df["review_comment_title"].isnull().sum())

print("Missing Review Messages:", df["review_comment_message"].isnull().sum())
