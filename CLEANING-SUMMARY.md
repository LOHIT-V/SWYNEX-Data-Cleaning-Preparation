# Cleaning Summary

## Dataset
- Input file: `retail_store_sales.csv`
- Original rows: 12,575
- Cleaned rows: 12,575
- Columns: 11

## Results
- Original rows: 12575
- Cleaned rows: 12575
- Exact duplicate rows removed: 0
- Duplicate Transaction IDs: 0
- Missing Item values filled: 1213
- Missing Discount Applied values filled: 4199
- Price Per Unit values calculated: 609
- Invalid transaction dates: 0
- Numeric conversion errors: 0
- Amount mismatches (complete rows): 0
- Rows with Quantity still missing: 604
- Rows with Total Spent still missing: 604

## Notes
- No rows were removed because the dataset contained no exact duplicate rows.
- No duplicate transaction IDs were found.
- Missing `Item` and `Discount Applied` values were labeled `Unknown`.
- 609 missing `Price Per Unit` values were calculated using `Total Spent / Quantity` where both values were available and quantity was positive.
- Missing `Quantity` and `Total Spent` values were retained because the available data did not support safely inferring them.
- No invalid dates, numeric conversion errors, or amount mismatches were detected by the checks in the script.
