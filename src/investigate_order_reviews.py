import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

file_path = DATA_DIR / "olist_order_reviews_dataset.csv"
df = pd.read_csv(file_path)

# Inspect duplicated review IDs
duplicated_reviews = df[
    df.duplicated(subset=["review_id"], keep=False)
].sort_values("review_id")

print("=== DUPLICATED REVIEW IDs ===")
print("Rows involved:", len(duplicated_reviews))
print("Unique duplicated IDs:", duplicated_reviews["review_id"].nunique())

print("\nFirst 10 duplicated records:")
print(duplicated_reviews.head(10).to_string(index=False))

# Check whether duplicated IDs have different data
columns_to_compare = [
    "order_id",
    "review_score",
    "review_comment_title",
    "review_comment_message",
    "review_creation_date",
    "review_answer_timestamp"
]

print("\n=== DUPLICATE ID DETAILS ===")

for column in columns_to_compare:
    different_values = (
        duplicated_reviews.groupby("review_id")[column]
        .nunique(dropna=False)
    )

    print(
        f"{column}:",
        (different_values > 1).sum(),
        "duplicated IDs have different values"
    )

# Inspect orders with multiple reviews
multiple_reviews = df[
    df.duplicated(subset=["order_id"], keep=False)
].sort_values("order_id")

print("\n=== ORDERS WITH MULTIPLE REVIEWS ===")
print("Rows involved:", len(multiple_reviews))
print("Unique orders:", multiple_reviews["order_id"].nunique())

print("\nFirst 10 records:")
print(multiple_reviews.head(10).to_string(index=False))

print("\n=== REVIEW DATA VALIDATION ===")

# Check exact duplicate rows
print("Exact duplicate rows:", df.duplicated().sum())

# Check duplicate review-order combinations
print(
    "Duplicate review_id + order_id:",
    df.duplicated(
        subset=["review_id", "order_id"]
    ).sum()
)

# Check missing identifiers
print("Missing review_id:", df["review_id"].isna().sum())
print("Missing order_id:", df["order_id"].isna().sum())

# Check review score range
print("Invalid review scores:",
      (~df["review_score"].between(1, 5)).sum())

# Check review dates
date_columns = [
    "review_creation_date",
    "review_answer_timestamp"
]

for column in date_columns:
    converted = pd.to_datetime(df[column], errors="coerce")
    invalid = df[column].notna() & converted.isna()
    print(f"Invalid {column} values:", invalid.sum())
