# SWYNEX – Data Cleaning & Preparation

## Project overview
This project cleans and prepares a public retail store sales dataset for further analysis. The work focuses on identifying missing values, checking duplicates, standardising fields, validating numeric relationships and documenting all changes.

## Dataset
- Source file: `retail_store_sales.csv` (original public dataset supplied for this project)
- Cleaned file: `SWYNEX-cleaned-retail-sales.csv`
- Records: 12,575
- Fields: transaction ID, customer ID, category, item, price per unit, quantity, total spent, payment method, location, transaction date and discount applied.

## Tools used
- Microsoft Excel for initial inspection
- Python and pandas for reproducible data checks and cleaning

## Cleaning steps
1. Inspected column names, data types and missing values.
2. Checked full-row duplicates and duplicate transaction IDs.
3. Trimmed leading and trailing spaces in text fields.
4. Replaced missing `Item` and `Discount Applied` values with `Unknown` so missing information is explicit rather than guessed.
5. Calculated missing `Price Per Unit` only when both `Quantity` and `Total Spent` were available and quantity was positive.
6. Kept rows with missing `Quantity` and `Total Spent` because the source did not contain enough information to infer them safely.
7. Parsed transaction dates and saved them in `YYYY-MM-DD` format.
8. Checked `Total Spent = Price Per Unit × Quantity` wherever all three values were available.

## Important data-quality decisions
- No duplicate rows or duplicate transaction IDs were found, so no transactions were deleted.
- Missing values were not replaced with arbitrary averages or fabricated values.
- Some numeric values remain blank because they cannot be reliably reconstructed from the available fields. These limitations are documented in `CLEANING-SUMMARY.md`.

## Files in this repository
- `SWYNEX-cleaned-retail-sales.csv` – cleaned dataset
- `CLEANING-SUMMARY.md` – counts, validation and cleaning decisions
- `README.md` – project documentation

## Conclusion
The dataset has been inspected and prepared with transparent, reproducible cleaning decisions. Unknown values and unresolved numeric gaps are clearly identified, while all original transaction records are retained.
