import json
from pathlib import Path
import csv

# Define input directory
input_dir = Path("data/raw/external")

# Read population data
with open(input_dir / "brazil_population_2016_2018.json", "r", encoding="utf-8") as file:
    population_data = json.load(file)

# Read GDP data
with open(input_dir / "brazil_gdp_2016_2018.json", "r", encoding="utf-8") as file:
    gdp_data = json.load(file)

# Read inflation data
with open(input_dir / "brazil_inflation_2016_2018.json", "r", encoding="utf-8") as file:
    inflation_data = json.load(file)

print("All JSON files loaded successfully!")

print("Population records:", len(population_data[1]))
print("GDP records:", len(gdp_data[1]))
print("Inflation records:", len(inflation_data[1]))
# Convert population records to dictionary
population = {
    record["date"]: record["value"]
    for record in population_data[1]
}

# Convert GDP records to dictionary
gdp = {
    record["date"]: record["value"]
    for record in gdp_data[1]
}

# Convert inflation records to dictionary
inflation = {
    record["date"]: record["value"]
    for record in inflation_data[1]
}

print("\nPopulation:", population)
print("GDP:", gdp)
print("Inflation:", inflation)
# Get all available years
years = sorted(population.keys())

# Combine all indicators by year
combined_data = []

for year in years:
    record = {
        "year": int(year),
        "population": population[year],
        "gdp": gdp.get(year),
        "inflation": inflation.get(year)
    }

    combined_data.append(record)

print("\nCombined Economic Data:")

for record in combined_data:
    print(record)


    # Save combined data to CSV
output_file = Path("data/processed/world_bank_brazil_economic_data.csv")

output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", newline="", encoding="utf-8") as file:
    fieldnames = ["year", "population", "gdp", "inflation"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(combined_data)

print(f"\nTransformed data saved to: {output_file}")