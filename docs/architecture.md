# Architecture

## Pipeline Summary

The project follows a simple analytics engineering flow:

1. Generate raw synthetic finance transactions.
2. Clean and validate data with Pandas.
3. Store curated data in SQLite.
4. Analyze with SQL and Python.
5. Document Power BI dashboard design and DAX measures.

## Data Flow

```text
etl/generate_dataset.py
        |
        v
data/raw/transactions_raw.csv
        |
        v
etl/clean_data.py
        |
        v
data/processed/transactions_clean.csv
        |
        v
etl/load_database.py
        |
        v
database/finance.db
```

## Design Choices

- SQLite keeps the project easy to run on any laptop.
- Pandas handles cleaning because the raw data contains mixed formats and missing values.
- SQL views provide reusable monthly, category, merchant, and payment method summaries.
- The Power BI layer is documented rather than stored as a binary `.pbix`, keeping the repository reviewable on GitHub.

## Data Quality Controls

- Required columns are checked before cleaning.
- Dates are parsed using known source formats.
- Duplicate `Transaction_ID` values are removed.
- Negative expense values are converted to positive values.
- Clean output is validated for unique IDs, valid dates, and non-negative amounts.
- SQLite load validates row counts and duplicate IDs.
