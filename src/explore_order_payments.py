
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

file_path = DATA_DIR / "olist_order_payments_dataset.csv"
df = pd.read_csv(file_path)

print("=== PAYMENT INVESTIGATION ===")

print("\n1. Zero Payment Values:")
print(
    df[df["payment_value"] == 0].to_string(index=False)
)

print("\n2. Zero Payment Installments:")
print(
    df[df["payment_installments"] == 0].to_string(index=False)
)

print("\n3. Undefined Payment Types:")
print(
    df[df["payment_type"] == "not_defined"].to_string(index=False)
)

print("\n=== INVESTIGATION COUNTS ===")

print("Zero Payment Values:", (df["payment_value"] == 0).sum())
print("Zero Installments:", (df["payment_installments"] == 0).sum())
print("Undefined Payment Types:", (df["payment_type"] == "not_defined").sum())
