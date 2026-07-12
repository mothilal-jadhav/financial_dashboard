# Finance Dashboard

Personal finance analytics project built with Python, Pandas, SQLite, SQL, Plotly, Matplotlib, and Power BI documentation. The repository is designed as an interview-ready portfolio project for Data Analyst, Business Analyst, and Data Analytics roles.

## Project Overview

This project simulates two years of student personal finance transactions, cleans intentionally dirty raw data, loads the curated dataset into SQLite, and provides SQL, EDA, reporting, and Power BI dashboard documentation.

## Architecture

1. `etl/generate_dataset.py` creates synthetic raw transactions with realistic dirty data.
2. `etl/clean_data.py` standardizes the raw file and creates analytical date columns.
3. `etl/load_database.py` creates `database/finance.db`, loads the clean table, and creates SQL views.
4. SQL analysis, notebook EDA, dashboard specs, and written insights use the same clean dataset.

## Folder Structure

```text
finance-dashboard/
  data/raw/                  Raw generated CSV
  data/processed/            Clean analytical CSV
  database/                  SQLite database
  dashboard/                 Power BI design and DAX documentation
  docs/                      Architecture and data dictionary
  etl/                       Python ETL scripts
  notebooks/                 Python EDA notebook
  reports/                   Business insights report
  screenshots/               Space for exported dashboard screenshots
  sql/                       Schema, views, and analysis queries
```

## Dataset Description

The dataset covers `2023-01-01` to `2024-12-31` and includes income, expenses, merchants, payment methods, locations, and account balance after each transaction. The raw file includes duplicate IDs, missing values, mixed date formats, inconsistent category labels, extra whitespace, mixed casing, and negative expense values.

## ETL Pipeline

The cleaning script parses mixed dates, removes duplicate `Transaction_ID` values, trims whitespace, normalizes merchants and categories, fills missing values, converts negative expenses to positive values, and creates `Year`, `Month`, `Month_Name`, `Quarter`, `Day_Of_Week`, and `Is_Weekend`.

## Database and SQL

SQLite is used for portability. `sql/schema.sql` defines the transaction table and indexes. `sql/views.sql` adds reusable summary views. `sql/analysis_queries.sql` contains 28 interview-quality SQL queries covering CTEs, window functions, rankings, running totals, monthly savings, category analysis, merchant analysis, payment method analysis, and weekend analysis.

## Python EDA

`notebooks/eda.ipynb` includes analysis code for monthly spending trends, income vs expense, category distribution, merchant analysis, payment method analysis, correlation heatmap, and monthly savings.

## Power BI

The `dashboard/` folder documents KPI cards, visuals, slicers, layout, color theme, and DAX measures that can be recreated in Power BI from `transactions_clean.csv` or `finance.db`.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## How to Run

```bash
python3 etl/generate_dataset.py
python3 etl/clean_data.py
python3 etl/load_database.py
```

Open the notebook:

```bash
jupyter notebook notebooks/eda.ipynb
```

Run SQL queries against SQLite:

```bash
sqlite3 database/finance.db < sql/analysis_queries.sql
```

## Screenshots

Export Power BI dashboard screenshots into `screenshots/` after building the dashboard from the documented design.

## Business Insights

See `reports/business_insights.md` for summarized findings and analyst recommendations.

## Future Improvements

- Add automated data quality tests with pytest.
- Add a small Streamlit dashboard for quick browser-based exploration.
- Add export scripts for Excel summary reports.
- Track budgets and compare actual spending against planned limits.
