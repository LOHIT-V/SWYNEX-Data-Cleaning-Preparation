
"""SWYNEX Data Cleaning and Preparation Project"""

import pandas as pd
import numpy as np

# 1. Load original dataset
raw = pd.read_csv("retail_store_sales.csv")

print("Original rows:", len(raw))

# 2. Remove leading/trailing spaces from text columns
text_columns = raw.select_dtypes(include="object").columns

for column in text_columns:
    raw[column] = raw[column].apply(
        lambda value: value.strip() if isinstance(value, str) else value
    )

# 3. Check duplicates (report only; do not delete records)
full_duplicates = int(raw.duplicated().sum())
duplicate_transactions = int(
    raw["Transaction ID"].duplicated().sum()
)

# 4. Handle missing categorical values
raw["Item"] = raw["Item"].fillna("Unknown")
raw["Discount Applied"] = raw["Discount Applied"].fillna("Unknown")

# 5. Calculate missing unit prices where possible
price_mask = (
    raw["Price Per Unit"].isna()
    & raw["Quantity"].notna()
    & raw["Total Spent"].notna()
    & (raw["Quantity"] > 0)
)

raw.loc[price_mask, "Price Per Unit"] = (
    raw.loc[price_mask, "Total Spent"]
    / raw.loc[price_mask, "Quantity"]
).round(2)

# 6. Validate Total Spent = Price Per Unit x Quantity
valid_rows = raw[
    ["Price Per Unit", "Quantity", "Total Spent"]
].notna().all(axis=1)

expected_total = (
    raw.loc[valid_rows, "Price Per Unit"]
    * raw.loc[valid_rows, "Quantity"]
)

actual_total = raw.loc[valid_rows, "Total Spent"]

mismatch_count = int(
    (~np.isclose(actual_total, expected_total, atol=0.01)).sum()
)

# 7. Standardise transaction dates
dates = pd.to_datetime(raw["Transaction Date"], errors="coerce")
invalid_dates = int(dates.isna().sum())

raw["Transaction Date"] = dates.dt.strftime("%Y-%m-%d")

# 8. Save cleaned dataset
raw.to_csv("SWYNEX-cleaned-retail-sales.csv", index=False)

# 9. Display validation results
print("\n--- SWYNEX CLEANING REPORT ---")
print("Rows retained:", len(raw))
print("Full-row duplicates:", full_duplicates)
print("Duplicate transaction IDs:", duplicate_transactions)
print("Item values replaced:", int(
    (raw["Item"] == "Unknown").sum()
))
print("Unit prices calculated:", int(price_mask.sum()))
print("Invalid transaction dates:", invalid_dates)
print("Numeric mismatches:", mismatch_count)
print("Missing Quantity:", int(raw["Quantity"].isna().sum()))
print("Missing Total Spent:", int(raw["Total Spent"].isna().sum()))
print("\nCleaning completed successfully!")
