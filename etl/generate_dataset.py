import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# -----------------------------
# Reproducibility
# -----------------------------
random.seed(42)
np.random.seed(42)

# -----------------------------
# Date Range
# -----------------------------
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

# -----------------------------
# Payment Methods
# -----------------------------
PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
    "Net Banking"
]

# -----------------------------
# Locations
# -----------------------------
LOCATIONS = [
    "New Delhi",
    "Noida",
    "Gurugram",
    "Online",
    "Hyderabad",
    "Mumbai"
]

# -----------------------------
# Income Categories
# -----------------------------
INCOME = {
    "Salary/Stipend": (7000, 9000),
    "Family Support": (9000, 15000),
    "Freelance": (3000, 12000),
    "Interest": (20, 500),
    "Cashback": (20, 300),
    "Refund": (100, 2000)
}

# -----------------------------
# Expense Categories
# -----------------------------
EXPENSE = {
    "Rent": (4500, 6000),
    "Food & Dining": (100, 500),
    "Groceries": (250, 1500),
    "Transportation": (50, 600),
    "Shopping": (400, 5000),
    "Entertainment": (150, 1200),
    "Health": (200, 3000),
    "Education": (500, 4000),
    "Bills": (199, 1500),
    "Travel": (1500, 12000),
    "Investment": (500, 4000),
    "Miscellaneous": (100, 1500)
}

# -----------------------------
# Merchants
# -----------------------------
MERCHANTS = {
    "Food & Dining": [
        "Swiggy",
        "Zomato",
        "Domino's",
        "McDonald's",
        "Burger King",
        "Campus Canteen"
    ],

    "Groceries": [
        "DMart",
        "Reliance Fresh",
        "BigBasket",
        "Blinkit"
    ],

    "Transportation": [
        "Uber",
        "Ola",
        "Delhi Metro"
    ],

    "Shopping": [
        "Amazon",
        "Flipkart",
        "Myntra",
        "Ajio"
    ],

    "Entertainment": [
        "Netflix",
        "Spotify",
        "PVR Cinemas",
        "BookMyShow"
    ],

    "Bills": [
        "Airtel",
        "Jio",
        "BSES"
    ],

    "Travel": [
        "IRCTC",
        "IndiGo",
        "Air India",
        "OYO"
    ],

    "Investment": [
        "Groww",
        "Zerodha"
    ],

    "Education": [
        "Coursera",
        "Udemy",
        "LeetCode"
    ],

    "Health": [
        "Apollo Pharmacy",
        "1mg"
    ],

    "Rent": [
        "Hostel Fee"
    ],

    "Miscellaneous": [
        "Stationery",
        "Gift Shop",
        "Printing Shop"
    ]
}

# -----------------------------
# Helper Functions
# -----------------------------
def random_date():
    """Return a random date between START_DATE and END_DATE."""
    days = (END_DATE - START_DATE).days
    return START_DATE + timedelta(days=random.randint(0, days))


def random_amount(category, income=True):
    """Generate amount based on category."""
    if income:
        low, high = INCOME[category]
    else:
        low, high = EXPENSE[category]

    return round(random.uniform(low, high), 2)


def random_payment():
    return random.choice(PAYMENT_METHODS)


def random_location():
    return random.choice(LOCATIONS)


def merchant(category):
    return random.choice(MERCHANTS[category])

# -----------------------------
# Generate Transactions
# -----------------------------

transactions = []
balance = 20000.0
txn_id = 100001

current = START_DATE

while current <= END_DATE:

    # -------------------------
    # Monthly Income
    # -------------------------

    stipend = random_amount("Salary/Stipend", True)

    balance += stipend

    transactions.append({
        "Transaction_ID": txn_id,
        "Date": current,
        "Merchant": "IIT Delhi",
        "Category": "Salary/Stipend",
        "Amount": stipend,
        "Payment_Method": "Net Banking",
        "Location": "New Delhi",
        "Income_Expense": "Income",
        "Account_Balance": round(balance,2)
    })

    txn_id += 1

    family = random_amount("Family Support", True)

    balance += family

    transactions.append({
        "Transaction_ID": txn_id,
        "Date": current + timedelta(days=1),
        "Merchant": "Parents",
        "Category": "Family Support",
        "Amount": family,
        "Payment_Method": "Net Banking",
        "Location": "Hyderabad",
        "Income_Expense": "Income",
        "Account_Balance": round(balance,2)
    })

    txn_id += 1

    # Freelance income (25% chance)

    if random.random() < 0.25:

        freelance = random_amount("Freelance", True)

        balance += freelance

        transactions.append({
            "Transaction_ID": txn_id,
            "Date": current + timedelta(days=random.randint(2,25)),
            "Merchant": "Client Payment",
            "Category": "Freelance",
            "Amount": freelance,
            "Payment_Method": "Net Banking",
            "Location": "Online",
            "Income_Expense": "Income",
            "Account_Balance": round(balance,2)
        })

        txn_id += 1

    # -------------------------
    # Monthly Rent
    # -------------------------

    rent = random_amount("Rent", False)

    balance -= rent

    transactions.append({
        "Transaction_ID": txn_id,
        "Date": current + timedelta(days=3),
        "Merchant": "Hostel Fee",
        "Category": "Rent",
        "Amount": rent,
        "Payment_Method": "UPI",
        "Location": "New Delhi",
        "Income_Expense": "Expense",
        "Account_Balance": round(balance,2)
    })

    txn_id += 1

    # -------------------------
    # Daily Transactions
    # -------------------------

    for _ in range(random.randint(70,110)):

        category = random.choice(list(EXPENSE.keys()))

        amount = random_amount(category, False)

        merchant_name = merchant(category)

        date = current + timedelta(days=random.randint(0,27))

        # Seasonal travel spike

        if category == "Travel" and date.month in [5,6,10,12]:
            amount *= random.uniform(1.4,2.2)

        # Festival shopping

        if category == "Shopping" and date.month in [10,11]:
            amount *= random.uniform(1.3,1.8)

        amount = round(amount,2)

        balance -= amount

        transactions.append({

            "Transaction_ID": txn_id,

            "Date": date,

            "Merchant": merchant_name,

            "Category": category,

            "Amount": amount,

            "Payment_Method": random_payment(),

            "Location": random_location(),

            "Income_Expense": "Expense",

            "Account_Balance": round(balance,2)

        })

        txn_id += 1

    # next month

    if current.month == 12:
        current = datetime(current.year + 1,1,1)
    else:
        current = datetime(current.year,current.month + 1,1)


# ----------------------------------
# Create DataFrame
# ----------------------------------

df = pd.DataFrame(transactions)

# ----------------------------------
# Shuffle rows
# ----------------------------------

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# ----------------------------------
# Inject Missing Merchant
# ----------------------------------

missing_merchants = np.random.choice(
    df.index,
    size=int(len(df) * 0.03),
    replace=False
)

df.loc[missing_merchants, "Merchant"] = np.nan

# ----------------------------------
# Inject Missing Payment Method
# ----------------------------------

missing_payment = np.random.choice(
    df.index,
    size=int(len(df) * 0.02),
    replace=False
)

df.loc[missing_payment, "Payment_Method"] = np.nan

# ----------------------------------
# Inject Missing Location
# ----------------------------------

missing_location = np.random.choice(
    df.index,
    size=int(len(df) * 0.01),
    replace=False
)

df.loc[missing_location, "Location"] = np.nan

# ----------------------------------
# Duplicate Rows
# ----------------------------------

duplicates = df.sample(
    frac=0.02,
    random_state=42
)

df = pd.concat([df, duplicates], ignore_index=True)

# ----------------------------------
# Negative Expense Amounts
# ----------------------------------

expense_rows = df[df["Income_Expense"] == "Expense"].sample(
    frac=0.01,
    random_state=42
).index

df.loc[expense_rows, "Amount"] *= -1

# ----------------------------------
# Category Inconsistencies
# ----------------------------------

replace_categories = {

    "Food & Dining": [
        "Food",
        "Dining",
        "food & dining",
        "FOOD"
    ],

    "Transportation": [
        "Transport",
        "transportation"
    ],

    "Shopping": [
        "shopping",
        "SHOPPING"
    ],

    "Entertainment": [
        "Movies",
        "Fun",
        "entertainment"
    ]

}

for original, alternatives in replace_categories.items():

    idx = df[df["Category"] == original].sample(
        frac=0.25,
        random_state=42
    ).index

    df.loc[idx, "Category"] = np.random.choice(
        alternatives,
        size=len(idx)
    )

# ----------------------------------
# Extra Spaces
# ----------------------------------

merchant_idx = df.sample(
    frac=0.02,
    random_state=12
).index

df.loc[merchant_idx, "Merchant"] = (
    df.loc[merchant_idx, "Merchant"]
    .astype(str)
    .apply(lambda x: "  " + x + " ")
)

# ----------------------------------
# Mixed Case
# ----------------------------------

merchant_idx2 = df.sample(
    frac=0.02,
    random_state=15
).index

df.loc[merchant_idx2, "Merchant"] = (
    df.loc[merchant_idx2, "Merchant"]
    .astype(str)
    .str.upper()
)

# ----------------------------------
# Mixed Date Formats
# ----------------------------------

formats = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%b-%Y"
]

formatted_dates = []

for d in df["Date"]:

    fmt = random.choice(formats)

    formatted_dates.append(d.strftime(fmt))

df["Date"] = formatted_dates

# ----------------------------------
# Sort by Transaction ID
# ----------------------------------

df = df.sort_values("Transaction_ID").reset_index(drop=True)


# ----------------------------------
# Save Dataset
# ----------------------------------

output_path = "data/raw/transactions_raw.csv"

df.to_csv(
    output_path,
    index=False
)

print("=" * 50)
print("Dataset Generated Successfully")
print("=" * 50)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print()

print(df.head())

print()

print("Data Quality Issues Injected")

print(
    "Missing Merchant:",
    df["Merchant"].isna().sum()
)

print(
    "Missing Payment Method:",
    df["Payment_Method"].isna().sum()
)

print(
    "Missing Location:",
    df["Location"].isna().sum()
)

print(
    "Duplicate Rows:",
    len(df) - len(df.drop_duplicates())
)

print(
    "Negative Amounts:",
    (df["Amount"] < 0).sum()
)

print()

print(
    "Dataset saved to:",
    output_path
)

