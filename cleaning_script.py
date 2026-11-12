"""Reproducible cleaning script for the SWYNEX retail sales project."""
import pandas as pd

raw = pd.read_csv('retail_store_sales.csv')
for column in ['Transaction ID', 'Customer ID', 'Category', 'Item', 'Payment Method', 'Location']:
    raw[column] = raw[column].apply(lambda value: value.strip() if isinstance(value, str) else value)
raw['Item'] = raw['Item'].fillna('Unknown')
raw['Discount Applied'] = raw['Discount Applied'].fillna('Unknown')
price_mask = (
    raw['Price Per Unit'].isna()
    & raw['Quantity'].notna()
    & raw['Total Spent'].notna()
    & (raw['Quantity'] > 0)
)
raw.loc[price_mask, 'Price Per Unit'] = (
    raw.loc[price_mask, 'Total Spent'] / raw.loc[price_mask, 'Quantity']
).round(2)
raw['Transaction Date'] = pd.to_datetime(raw['Transaction Date'], errors='coerce').dt.strftime('%Y-%m-%d')
raw.to_csv('SWYNEX-cleaned-retail-sales.csv', index=False)
print(f'Rows retained: {len(raw):,}')
print(f'Unit prices inferred: {int(price_mask.sum()):,}')
print(f'Remaining missing quantity: {int(raw["Quantity"].isna().sum()):,}')
print(f'Remaining missing total spent: {int(raw["Total Spent"].isna().sum()):,}')
