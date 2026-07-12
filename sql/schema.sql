DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    Transaction_ID INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    Merchant TEXT NOT NULL,
    Category TEXT NOT NULL,
    Amount REAL NOT NULL CHECK (Amount >= 0),
    Payment_Method TEXT NOT NULL,
    Location TEXT NOT NULL,
    Income_Expense TEXT NOT NULL CHECK (Income_Expense IN ('Income', 'Expense')),
    Account_Balance REAL NOT NULL,
    Year INTEGER NOT NULL,
    Month INTEGER NOT NULL CHECK (Month BETWEEN 1 AND 12),
    Month_Name TEXT NOT NULL,
    Quarter TEXT NOT NULL,
    Day_Of_Week TEXT NOT NULL,
    Is_Weekend INTEGER NOT NULL CHECK (Is_Weekend IN (0, 1))
);

CREATE INDEX idx_transactions_date ON transactions (Date);
CREATE INDEX idx_transactions_category ON transactions (Category);
CREATE INDEX idx_transactions_income_expense ON transactions (Income_Expense);
CREATE INDEX idx_transactions_payment_method ON transactions (Payment_Method);
CREATE INDEX idx_transactions_merchant ON transactions (Merchant);
