"""Clean raw personal finance transactions and create date features."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "transactions_raw.csv"
PROCESSED_OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "transactions_clean.csv"

CATEGORY_MAP = {
    "food": "Food & Dining",
    "dining": "Food & Dining",
    "food & dining": "Food & Dining",
    "transport": "Transportation",
    "transportation": "Transportation",
    "commute": "Transportation",
    "shopping": "Shopping",
    "movies": "Entertainment",
    "fun": "Entertainment",
    "entertainment": "Entertainment",
    "utilities": "Bills",
    "utility bills": "Bills",
    "misc": "Miscellaneous",
    "others": "Miscellaneous",
}

PAYMENT_METHOD_MAP = {
    "upi": "UPI",
    "credit card": "Credit Card",
    "debit card": "Debit Card",
    "cash": "Cash",
    "net banking": "Net Banking",
}

MERCHANT_MAP = {
    "1Mg": "Tata 1mg",
    "Bigbasket": "BigBasket",
    "Bookmyshow": "BookMyShow",
    "Bses": "BSES",
    "Domino'S": "Domino's",
    "Dmart": "DMart",
    "Hdfc Bank": "HDFC Bank",
    "Indigo": "IndiGo",
    "Irctc": "IRCTC",
    "Iit Delhi": "IIT Delhi",
    "Jio": "Jio",
    "Leetcode": "LeetCode",
    "Makemytrip": "MakeMyTrip",
    "Mcdonald'S": "McDonald's",
    "Nps": "NPS",
    "Oyo": "OYO",
    "Pvr Cinemas": "PVR Cinemas",
    "Tata 1Mg": "Tata 1mg",
}


def parse_mixed_dates(date_series: pd.Series) -> pd.Series:
    """Parse the known date formats injected in the raw dataset."""
    parsed = pd.Series(pd.NaT, index=date_series.index, dtype="datetime64[ns]")
    for date_format in ("%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y"):
        remaining = parsed.isna()
        parsed.loc[remaining] = pd.to_datetime(
            date_series.loc[remaining],
            format=date_format,
            errors="coerce",
        )
    return parsed


def normalize_text(series: pd.Series) -> pd.Series:
    """Trim spaces and convert string placeholders back to missing values."""
    cleaned = series.astype("string").str.strip()
    missing_mask = cleaned.str.lower().isin({"", "nan", "none", "<na>"})
    return cleaned.mask(missing_mask, pd.NA)


def clean_transactions(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Return a validated cleaned transaction dataframe."""
    df = raw_df.copy()

    required_columns = {
        "Transaction_ID",
        "Date",
        "Merchant",
        "Category",
        "Amount",
        "Payment_Method",
        "Location",
        "Income_Expense",
        "Account_Balance",
    }
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    df["Date"] = parse_mixed_dates(df["Date"].astype("string").str.strip())
    df = df.dropna(subset=["Date"])

    for column in ["Merchant", "Category", "Payment_Method", "Location", "Income_Expense"]:
        df[column] = normalize_text(df[column])

    df["Transaction_ID"] = pd.to_numeric(df["Transaction_ID"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["Account_Balance"] = pd.to_numeric(df["Account_Balance"], errors="coerce")
    df = df.dropna(subset=["Transaction_ID", "Amount", "Account_Balance"])
    df["Transaction_ID"] = df["Transaction_ID"].astype("int64")

    df["Category"] = (
        df["Category"].str.lower().map(CATEGORY_MAP).fillna(df["Category"].str.title())
    )
    df["Payment_Method"] = (
        df["Payment_Method"]
        .str.lower()
        .map(PAYMENT_METHOD_MAP)
        .fillna(df["Payment_Method"])
    )
    df["Income_Expense"] = df["Income_Expense"].str.title()
    df["Merchant"] = df["Merchant"].str.title().replace(MERCHANT_MAP)
    df["Location"] = df["Location"].str.title().replace({"Nan": pd.NA})

    df["Merchant"] = df["Merchant"].fillna("Unknown Merchant")
    df["Payment_Method"] = df["Payment_Method"].fillna(df["Payment_Method"].mode()[0])
    df["Location"] = df["Location"].fillna("Unknown")

    expense_mask = (df["Income_Expense"] == "Expense") & (df["Amount"] < 0)
    df.loc[expense_mask, "Amount"] = df.loc[expense_mask, "Amount"].abs()

    df = df.sort_values(["Transaction_ID", "Date"]).drop_duplicates(
        subset=["Transaction_ID"],
        keep="first",
    )

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%B")
    df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)
    df["Day_Of_Week"] = df["Date"].dt.day_name()
    df["Is_Weekend"] = np.where(df["Day_Of_Week"].isin(["Saturday", "Sunday"]), 1, 0)

    df = df.sort_values(["Date", "Transaction_ID"]).reset_index(drop=True)

    if not df["Transaction_ID"].is_unique:
        raise ValueError("Transaction_ID values are not unique after cleaning.")
    if df["Date"].isna().any():
        raise ValueError("Date parsing failed for one or more records.")
    if (df["Amount"] < 0).any():
        raise ValueError("Negative amounts remain after cleaning.")

    return df


def main() -> None:
    """Read raw CSV, clean it, and write the processed CSV."""
    if not RAW_INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at {RAW_INPUT_PATH}. Run etl/generate_dataset.py first."
        )

    PROCESSED_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw_df = pd.read_csv(RAW_INPUT_PATH)
    clean_df = clean_transactions(raw_df)
    clean_df.to_csv(PROCESSED_OUTPUT_PATH, index=False)

    print("=" * 50)
    print("Cleaning complete")
    print("=" * 50)
    print(f"Input rows: {len(raw_df):,}")
    print(f"Output rows: {len(clean_df):,}")
    print(f"Columns: {len(clean_df.columns)}")
    print(f"Saved to: {PROCESSED_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
