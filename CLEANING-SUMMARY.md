# Data Cleaning Summary

- Original records: 12,575
- Records after cleaning: 12,575
- Full-row duplicates detected: 0
- Duplicate transaction IDs detected: 0
- Missing Item values replaced with `Unknown`: 1,213
- Missing Discount Applied values replaced with `Unknown`: 4,199
- Missing Price Per Unit values calculated from Total Spent / Quantity: 609
- Missing Price Per Unit values originally present: 609
- Invalid transaction dates detected: 0
- Quantity and Total Spent: 604 and 604 values remain missing where the source did not provide enough information to infer them reliably.

## Data validation

For rows where Price Per Unit, Quantity and Total Spent are all available, the relationship `Total Spent = Price Per Unit * Quantity` was checked. The source dataset's complete numeric rows were consistent with this relationship.

## Cleaning decisions

1. Text fields were trimmed to remove leading/trailing whitespace.
2. Missing Item and Discount Applied values were labelled `Unknown` rather than guessed.
3. Price Per Unit was calculated only when both Quantity and Total Spent were available and Quantity was greater than zero.
4. Rows with missing Quantity and Total Spent were retained; those values were not invented.
5. Transaction Date was parsed and saved in ISO format (`YYYY-MM-DD`).
6. No duplicate rows or transaction IDs were detected, so no records were removed.
