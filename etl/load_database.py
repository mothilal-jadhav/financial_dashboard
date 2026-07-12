"""Load cleaned transactions into a SQLite database."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "transactions_clean.csv"
DATABASE_PATH = PROJECT_ROOT / "database" / "finance.db"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"
VIEWS_PATH = PROJECT_ROOT / "sql" / "views.sql"


def execute_sql_file(connection: sqlite3.Connection, sql_path: Path) -> None:
    """Execute a SQL script file."""
    connection.executescript(sql_path.read_text(encoding="utf-8"))


def load_transactions() -> None:
    """Create the SQLite schema and load the cleaned CSV."""
    if not CLEAN_INPUT_PATH.exists():
        raise FileNotFoundError(
            "Cleaned dataset not found. Run etl/clean_data.py before loading SQLite."
        )

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(CLEAN_INPUT_PATH)

    with sqlite3.connect(DATABASE_PATH) as connection:
        execute_sql_file(connection, SCHEMA_PATH)
        df.to_sql("transactions", connection, if_exists="append", index=False)
        execute_sql_file(connection, VIEWS_PATH)

        row_count = connection.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
        duplicate_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT Transaction_ID
                FROM transactions
                GROUP BY Transaction_ID
                HAVING COUNT(*) > 1
            )
            """
        ).fetchone()[0]

    if row_count != len(df):
        raise ValueError("Loaded row count does not match cleaned CSV row count.")
    if duplicate_count:
        raise ValueError("Duplicate Transaction_ID values found in SQLite table.")

    print("=" * 50)
    print("Database load complete")
    print("=" * 50)
    print(f"Rows loaded: {row_count:,}")
    print(f"Database: {DATABASE_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    load_transactions()
