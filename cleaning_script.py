
"""SWYNEX Data Cleaning and Preparation Project"""

import pandas as pd
import numpy as np

# 1. Load original dataset
raw = pd.read_csv("retail_store_sales.csv")

print("Original rows:", len(raw))

# 2. Clean text columns
text_columns = raw.select_dtypes(include="object").columns

for column in text_columns:
    raw[column] = raw[column].apply(
        lambda value: value.strip() if isinstance(value, str) else value
    )

# 3. Remove exact duplicate records
full_duplicates = int(raw.duplicated().sum())
raw = raw.drop_duplicates().copy()

# Check duplicate transaction IDs separately
duplicate_transactions = int(
    raw["Transaction ID"].duplicated().sum()
)

# 4. Convert numeric columns to correct data types
numeric_columns = [
    "Price Per Unit",
    "Quantity",
    "Total Spent"
]

numeric_errors = {}

for column in numeric_columns:
    converted = pd.to_numeric(raw[column], errors="coerce")
    numeric_errors[column] = int(
        (raw[column].notna() & converted.isna()).sum()
    )
    raw[column] = converted

# 5. Handle missing categorical values
missing_items = int(raw["Item"].isna().sum())
missing_discounts = int(raw["Discount Applied"].isna().sum())

raw["Item"] = raw["Item"].fillna("Unknown")
raw["Discount Applied"] = raw["Discount Applied"].fillna("Unknown")

# 6. Calculate missing unit prices where possible
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

# 7. Validate Total Spent = Price Per Unit x Quantity
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

# 8. Standardise transaction dates
dates = pd.to_datetime(
    raw["Transaction Date"],
    errors="coerce",
    dayfirst=False
)

invalid_dates = int(
    (raw["Transaction Date"].notna() & dates.isna()).sum()
)

raw["Transaction Date"] = dates.dt.strftime("%Y-%m-%d")

# 9. Save cleaned dataset
raw.to_csv("SWYNEX-cleaned-retail-sales.csv", index=False)

# 10. Display cleaning report
print("\n--- SWYNEX CLEANING REPORT ---")
print("Rows retained:", len(raw))
print("Exact duplicate rows removed:", full_duplicates)
print("Duplicate transaction IDs:", duplicate_transactions)
print("Missing Item values replaced:", missing_items)
print("Missing Discount values replaced:", missing_discounts)
print("Unit prices calculated:", int(price_mask.sum()))
print("Invalid transaction dates:", invalid_dates)
print("Numeric conversion errors:", numeric_errors)
print("Numeric mismatches:", mismatch_count)
print("\nRemaining missing values:")
print(raw.isna().sum())
print("\nCleaning completed successfully!")
