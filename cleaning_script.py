import pandas as pd

INPUT_FILE = "retail_store_sales.csv"
OUTPUT_FILE = "SWYNEX-cleaned-retail-sales.csv"

df = pd.read_csv(INPUT_FILE)
original_rows = len(df)

# Clean whitespace in text columns.
for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].astype("string").str.strip()
    df[column] = df[column].replace("", pd.NA)

# Remove exact duplicate rows.
exact_duplicates = int(df.duplicated().sum())
df = df.drop_duplicates().copy()
duplicate_transaction_ids = int(df["Transaction ID"].duplicated().sum())

# Convert numeric columns safely.
numeric_columns = ["Price Per Unit", "Quantity", "Total Spent"]
conversion_errors = {}
for column in numeric_columns:
    before = df[column].notna()
    converted = pd.to_numeric(df[column], errors="coerce")
    conversion_errors[column] = int((before & converted.isna()).sum())
    df[column] = converted

# Replace missing category labels with an explicit value.
missing_item_filled = int(df["Item"].isna().sum())
df["Item"] = df["Item"].fillna("Unknown")

missing_discount_filled = int(df["Discount Applied"].isna().sum())
df["Discount Applied"] = df["Discount Applied"].fillna("Unknown")

# Infer unit price only when total and a positive quantity are available.
price_missing_before = int(df["Price Per Unit"].isna().sum())
price_fill_mask = (
    df["Price Per Unit"].isna()
    & df["Total Spent"].notna()
    & df["Quantity"].notna()
    & (df["Quantity"] > 0)
)
df.loc[price_fill_mask, "Price Per Unit"] = (
    df.loc[price_fill_mask, "Total Spent"] / df.loc[price_fill_mask, "Quantity"]
)
prices_calculated = int(price_fill_mask.sum())

# Standardize transaction dates.
parsed_dates = pd.to_datetime(df["Transaction Date"], errors="coerce")
invalid_dates = int((df["Transaction Date"].notna() & parsed_dates.isna()).sum())
df["Transaction Date"] = parsed_dates.dt.strftime("%Y-%m-%d")

# Check the total against unit price multiplied by quantity where all values exist.
complete_amount_rows = df[["Price Per Unit", "Quantity", "Total Spent"]].notna().all(axis=1)
valid_amount_rows = complete_amount_rows & (df["Quantity"] > 0)
mismatch_count = int(
    (
        (df.loc[valid_amount_rows, "Price Per Unit"] * df.loc[valid_amount_rows, "Quantity"]
         - df.loc[valid_amount_rows, "Total Spent"]).abs() > 0.01
    ).sum()
)

df.to_csv(OUTPUT_FILE, index=False)

print("CLEANING REPORT")
print(f"Original rows: {original_rows}")
print(f"Cleaned rows: {len(df)}")
print(f"Exact duplicate rows removed: {exact_duplicates}")
print(f"Duplicate Transaction IDs: {duplicate_transaction_ids}")
print(f"Missing Item values filled: {missing_item_filled}")
print(f"Missing Discount Applied values filled: {missing_discount_filled}")
print(f"Price Per Unit values calculated: {prices_calculated}")
print(f"Invalid transaction dates: {invalid_dates}")
print(f"Numeric conversion errors: {sum(conversion_errors.values())}")
print(f"Amount mismatches (complete rows): {mismatch_count}")
print(f"Rows with Quantity still missing: {int(df['Quantity'].isna().sum())}")
print(f"Rows with Total Spent still missing: {int(df['Total Spent'].isna().sum())}")
