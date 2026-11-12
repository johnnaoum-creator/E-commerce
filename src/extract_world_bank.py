import requests
import json
from pathlib import Path

# World Bank API base URL
base_url = "https://api.worldbank.org/v2/country/BR/indicator/"

# Indicators we need
indicators = {
    "population": "SP.POP.TOTL",
    "gdp": "NY.GDP.MKTP.CD",
    "inflation": "FP.CPI.TOTL.ZG"
}

# Output directory
output_dir = Path("data/raw/external")
output_dir.mkdir(parents=True, exist_ok=True)

# Extract each indicator
for name, code in indicators.items():

    url = base_url + code

    params = {
        "format": "json",
        "date": "2016:2018"
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    # Save raw response
    output_file = output_dir / f"brazil_{name}_2016_2018.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"\n{name.upper()}:")

    # Display extracted records
    records = data[1]

    for record in records:
        print(f"Year: {record['date']}, Value: {record['value']}")

    print(f"Saved to: {output_file}")