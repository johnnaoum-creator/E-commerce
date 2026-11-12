
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

file_path = DATA_DIR / "olist_geolocation_dataset.csv"
df = pd.read_csv(file_path)

print("=== GEOLOCATION INVESTIGATION ===")

# 1. Inspect exact duplicate rows
print("\n=== EXACT DUPLICATES ===")

duplicates = df[df.duplicated(keep=False)]

print("Total rows involved in duplicate groups:", len(duplicates))
print("Number of duplicate groups:",
      df.duplicated().sum())

print("\nSample duplicate rows:")
print(duplicates.head(10).to_string(index=False))

# 2. Check ZIP codes associated with multiple coordinates
print("\n=== ZIP CODE COORDINATES ===")

coordinates_per_zip = (
    df.groupby("geolocation_zip_code_prefix")
    .apply(
        lambda group: group[
            ["geolocation_lat", "geolocation_lng"]
        ].drop_duplicates().shape[0]
    )
)

print("ZIP codes with more than one distinct coordinate:",
      (coordinates_per_zip > 1).sum())

print("\nTop 10 ZIP codes by number of distinct coordinates:")
print(coordinates_per_zip.sort_values(ascending=False).head(10))

# 3. Inspect coordinates outside approximate Brazil bounds
print("\n=== COORDINATES OUTSIDE APPROXIMATE BRAZIL BOUNDS ===")

brazil_bounds = (
    df["geolocation_lat"].between(-34, 6) &
    df["geolocation_lng"].between(-74, -34)
)

outside_brazil = df[~brazil_bounds].copy()

print("Number of rows outside approximate bounds:",
      len(outside_brazil))

print("\nOutside-bounds records:")
print(outside_brazil.to_string(index=False))

print("\nStates in outside-bounds records:")
print(outside_brazil["geolocation_state"].value_counts())

print("\n=== INVESTIGATION COMPLETED ===")
