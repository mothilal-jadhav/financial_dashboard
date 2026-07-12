"""Generate a realistic synthetic personal finance dataset.

The dataset models an IIT Delhi student's transactions from 2023-01-01 to
2024-12-31 and intentionally injects data quality issues for the ETL pipeline.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_SEED = 42
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "transactions_raw.csv"

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
LOCATIONS = ["New Delhi", "Noida", "Gurugram", "Online", "Hyderabad", "Mumbai"]

INCOME_RANGES = {
    "Salary/Stipend": (12000, 18000),
    "Family Support": (25000, 45000),
    "Freelance": (3000, 12000),
    "Interest": (20, 500),
    "Cashback": (20, 300),
    "Refund": (100, 2000),
}

EXPENSE_RANGES = {
    "Rent": (4500, 6000),
    "Food & Dining": (80, 350),
    "Groceries": (150, 900),
    "Transportation": (20, 250),
    "Shopping": (250, 2500),
    "Entertainment": (100, 800),
    "Health": (100, 1800),
    "Education": (300, 2500),
    "Bills": (100, 1200),
    "Travel": (700, 8000),
    "Investment": (500, 3000),
    "Miscellaneous": (50, 800),
}

EXPENSE_CATEGORY_WEIGHTS = {
    "Food & Dining": 0.26,
    "Transportation": 0.18,
    "Groceries": 0.13,
    "Bills": 0.08,
    "Miscellaneous": 0.08,
    "Entertainment": 0.07,
    "Shopping": 0.07,
    "Education": 0.04,
    "Health": 0.03,
    "Investment": 0.03,
    "Travel": 0.02,
    "Rent": 0.01,
}

MERCHANTS = {
    "Salary/Stipend": ["IIT Delhi"],
    "Family Support": ["Parents"],
    "Freelance": ["Client Payment", "Upwork Client", "Campus Project"],
    "Interest": ["HDFC Bank", "SBI Savings"],
    "Cashback": ["Google Pay Rewards", "PhonePe Rewards", "Amazon Pay"],
    "Refund": ["Amazon Refund", "IRCTC Refund", "Myntra Refund"],
    "Rent": ["Hostel Fee"],
    "Food & Dining": [
        "Swiggy",
        "Zomato",
        "Domino's",
        "McDonald's",
        "Burger King",
        "Campus Canteen",
        "Chaayos",
    ],
    "Groceries": ["DMart", "Reliance Fresh", "BigBasket", "Blinkit"],
    "Transportation": ["Uber", "Ola", "Delhi Metro", "Rapido"],
    "Shopping": ["Amazon", "Flipkart", "Myntra", "Ajio"],
    "Entertainment": ["Netflix", "Spotify", "PVR Cinemas", "BookMyShow"],
    "Health": ["Apollo Pharmacy", "Tata 1mg", "Practo"],
    "Education": ["Coursera", "Udemy", "LeetCode", "Gate Academy"],
    "Bills": ["Airtel", "Jio", "BSES", "Hostel Laundry"],
    "Travel": ["IRCTC", "IndiGo", "Air India", "OYO", "MakeMyTrip"],
    "Investment": ["Groww", "Zerodha", "NPS"],
    "Miscellaneous": ["Stationery", "Gift Shop", "Printing Shop"],
}

INCONSISTENT_CATEGORIES = {
    "Food & Dining": ["Food", "Dining", "food & dining", "FOOD"],
    "Transportation": ["Transport", "transportation", "Commute"],
    "Shopping": ["shopping", "SHOPPING"],
    "Entertainment": ["Movies", "Fun", "entertainment"],
    "Bills": ["utilities", "Utility Bills"],
    "Miscellaneous": ["misc", "Others"],
}


def random_amount(category: str, transaction_type: str) -> float:
    """Return a category-aware transaction amount."""
    ranges = INCOME_RANGES if transaction_type == "Income" else EXPENSE_RANGES
    low, high = ranges[category]
    return round(random.uniform(low, high), 2)


def add_transaction(
    transactions: list[dict[str, object]],
    transaction_id: int,
    date: datetime,
    merchant: str,
    category: str,
    amount: float,
    payment_method: str,
    location: str,
    income_expense: str,
    balance: float,
) -> None:
    """Append one transaction row with consistent column names."""
    transactions.append(
        {
            "Transaction_ID": transaction_id,
            "Date": date,
            "Merchant": merchant,
            "Category": category,
            "Amount": round(amount, 2),
            "Payment_Method": payment_method,
            "Location": location,
            "Income_Expense": income_expense,
            "Account_Balance": round(balance, 2),
        }
    )


def generate_clean_base_transactions() -> pd.DataFrame:
    """Generate clean transactions before intentional quality issues are added."""
    transactions: list[dict[str, object]] = []
    balance = 20000.0
    transaction_id = 100001
    current_month = START_DATE

    while current_month <= END_DATE:
        for category, day_offset in [
            ("Salary/Stipend", 0),
            ("Family Support", 1),
        ]:
            amount = random_amount(category, "Income")
            balance += amount
            add_transaction(
                transactions,
                transaction_id,
                current_month + timedelta(days=day_offset),
                random.choice(MERCHANTS[category]),
                category,
                amount,
                "Net Banking",
                "New Delhi" if category == "Salary/Stipend" else "Hyderabad",
                "Income",
                balance,
            )
            transaction_id += 1

        optional_income_categories = ["Freelance", "Interest", "Cashback", "Refund"]
        for category in optional_income_categories:
            if random.random() < 0.35:
                amount = random_amount(category, "Income")
                balance += amount
                add_transaction(
                    transactions,
                    transaction_id,
                    current_month + timedelta(days=random.randint(2, 27)),
                    random.choice(MERCHANTS[category]),
                    category,
                    amount,
                    "Net Banking" if category in {"Freelance", "Interest"} else "UPI",
                    random.choice(["Online", "New Delhi", "Hyderabad"]),
                    "Income",
                    balance,
                )
                transaction_id += 1

        rent = random_amount("Rent", "Expense")
        balance -= rent
        add_transaction(
            transactions,
            transaction_id,
            current_month + timedelta(days=3),
            "Hostel Fee",
            "Rent",
            rent,
            "UPI",
            "New Delhi",
            "Expense",
            balance,
        )
        transaction_id += 1

        for _ in range(random.randint(86, 112)):
            category = random.choices(
                population=list(EXPENSE_CATEGORY_WEIGHTS),
                weights=list(EXPENSE_CATEGORY_WEIGHTS.values()),
                k=1,
            )[0]
            amount = random_amount(category, "Expense")
            date = current_month + timedelta(days=random.randint(0, 27))

            if category == "Travel" and date.month in {5, 6, 10, 12}:
                amount *= random.uniform(1.4, 2.2)
            if category == "Shopping" and date.month in {10, 11}:
                amount *= random.uniform(1.3, 1.8)

            amount = round(amount, 2)
            balance -= amount
            add_transaction(
                transactions,
                transaction_id,
                date,
                random.choice(MERCHANTS[category]),
                category,
                amount,
                random.choice(PAYMENT_METHODS),
                random.choice(LOCATIONS),
                "Expense",
                balance,
            )
            transaction_id += 1

        if current_month.month == 12:
            current_month = datetime(current_month.year + 1, 1, 1)
        else:
            current_month = datetime(current_month.year, current_month.month + 1, 1)

    df = pd.DataFrame(transactions).sort_values(["Date", "Transaction_ID"]).reset_index(
        drop=True
    )
    df["Transaction_ID"] = range(100001, 100001 + len(df))

    balance = 20000.0
    balances = []
    for _, row in df.iterrows():
        if row["Income_Expense"] == "Income":
            balance += row["Amount"]
        else:
            balance -= row["Amount"]
        balances.append(round(balance, 2))
    df["Account_Balance"] = balances

    return df


def inject_dirty_data(df: pd.DataFrame) -> pd.DataFrame:
    """Inject realistic data quality problems for cleaning practice."""
    dirty = df.copy()

    dirty.loc[
        np.random.choice(dirty.index, size=int(len(dirty) * 0.03), replace=False),
        "Merchant",
    ] = np.nan
    dirty.loc[
        np.random.choice(dirty.index, size=int(len(dirty) * 0.02), replace=False),
        "Payment_Method",
    ] = np.nan
    dirty.loc[
        np.random.choice(dirty.index, size=int(len(dirty) * 0.01), replace=False),
        "Location",
    ] = np.nan

    duplicate_rows = dirty.sample(frac=0.02, random_state=RANDOM_SEED)
    dirty = pd.concat([dirty, duplicate_rows], ignore_index=True)

    expense_sample = dirty[dirty["Income_Expense"] == "Expense"].sample(
        frac=0.01,
        random_state=RANDOM_SEED,
    )
    dirty.loc[expense_sample.index, "Amount"] *= -1

    for original, alternatives in INCONSISTENT_CATEGORIES.items():
        category_rows = dirty[dirty["Category"] == original]
        if category_rows.empty:
            continue
        indexes = category_rows.sample(frac=0.25, random_state=RANDOM_SEED).index
        dirty.loc[indexes, "Category"] = np.random.choice(alternatives, size=len(indexes))

    for column in ["Merchant", "Category", "Payment_Method", "Location"]:
        indexes = dirty.sample(frac=0.02, random_state=len(column)).index
        dirty.loc[indexes, column] = dirty.loc[indexes, column].astype(str).apply(
            lambda value: f"  {value} "
        )

    merchant_indexes = dirty.sample(frac=0.02, random_state=15).index
    dirty.loc[merchant_indexes, "Merchant"] = (
        dirty.loc[merchant_indexes, "Merchant"].astype(str).str.upper()
    )

    date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y"]
    dirty["Date"] = [
        date_value.strftime(random.choice(date_formats)) for date_value in dirty["Date"]
    ]

    return dirty.sort_values("Transaction_ID").reset_index(drop=True)


def main() -> None:
    """Generate the raw CSV file."""
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    RAW_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    base_df = generate_clean_base_transactions()
    raw_df = inject_dirty_data(base_df)
    raw_df.to_csv(RAW_OUTPUT_PATH, index=False)

    print("=" * 50)
    print("Dataset generated successfully")
    print("=" * 50)
    print(f"Rows: {len(raw_df):,}")
    print(f"Columns: {len(raw_df.columns)}")
    print(f"Duplicate Transaction_IDs: {raw_df['Transaction_ID'].duplicated().sum()}")
    print(f"Missing Merchant: {raw_df['Merchant'].isna().sum()}")
    print(f"Missing Payment Method: {raw_df['Payment_Method'].isna().sum()}")
    print(f"Missing Location: {raw_df['Location'].isna().sum()}")
    print(f"Negative Amounts: {(raw_df['Amount'] < 0).sum()}")
    print(f"Dataset saved to: {RAW_OUTPUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
