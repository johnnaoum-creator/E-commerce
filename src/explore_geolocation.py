
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

file_path = DATA_DIR / "olist_geolocation_dataset.csv"
df = pd.read_csv(file_path)

print("=== GEOLOCATION DATASET REPORT ===")

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

# ZIP code analysis
print("\n=== ZIP CODE ANALYSIS ===")

print("Unique ZIP Code Prefixes:",
      df["geolocation_zip_code_prefix"].nunique())

print("Unique Cities:",
      df["geolocation_city"].nunique())

print("Unique States:",
      df["geolocation_state"].nunique())

# Coordinate validation
print("\n=== COORDINATE VALIDATION ===")

print("\nLatitude Summary:")
print(df["geolocation_lat"].describe())

print("\nLongitude Summary:")
print(df["geolocation_lng"].describe())

print("\nInvalid Latitude Values:",
      ((df["geolocation_lat"] < -90) |
       (df["geolocation_lat"] > 90)).sum())

print("\nInvalid Longitude Values:",
      ((df["geolocation_lng"] < -180) |
       (df["geolocation_lng"] > 180)).sum())

# Brazil approximate coordinate bounds
brazil_bounds = (
    df["geolocation_lat"].between(-34, 6) &
    df["geolocation_lng"].between(-74, -34)
)

print("\nCoordinates Outside Approximate Brazil Bounds:",
      (~brazil_bounds).sum())
