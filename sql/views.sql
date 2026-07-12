DROP VIEW IF EXISTS vw_monthly_summary;
DROP VIEW IF EXISTS vw_category_spending;
DROP VIEW IF EXISTS vw_payment_method_summary;
DROP VIEW IF EXISTS vw_merchant_summary;

CREATE VIEW vw_monthly_summary AS
SELECT
    Year,
    Month,
    Month_Name,
    printf('%04d-%02d', Year, Month) AS Year_Month,
    ROUND(SUM(CASE WHEN Income_Expense = 'Income' THEN Amount ELSE 0 END), 2) AS Total_Income,
    ROUND(SUM(CASE WHEN Income_Expense = 'Expense' THEN Amount ELSE 0 END), 2) AS Total_Expense,
    ROUND(
        SUM(CASE WHEN Income_Expense = 'Income' THEN Amount ELSE 0 END)
        - SUM(CASE WHEN Income_Expense = 'Expense' THEN Amount ELSE 0 END),
        2
    ) AS Net_Savings,
    COUNT(*) AS Transaction_Count
FROM transactions
GROUP BY Year, Month, Month_Name;

CREATE VIEW vw_category_spending AS
SELECT
    Category,
    ROUND(SUM(Amount), 2) AS Total_Spent,
    ROUND(AVG(Amount), 2) AS Avg_Transaction,
    COUNT(*) AS Transaction_Count
FROM transactions
WHERE Income_Expense = 'Expense'
GROUP BY Category;

CREATE VIEW vw_payment_method_summary AS
SELECT
    Payment_Method,
    Income_Expense,
    ROUND(SUM(Amount), 2) AS Total_Amount,
    COUNT(*) AS Transaction_Count,
    ROUND(AVG(Amount), 2) AS Avg_Amount
FROM transactions
GROUP BY Payment_Method, Income_Expense;

CREATE VIEW vw_merchant_summary AS
SELECT
    Merchant,
    Category,
    Income_Expense,
    ROUND(SUM(Amount), 2) AS Total_Amount,
    COUNT(*) AS Transaction_Count,
    ROUND(AVG(Amount), 2) AS Avg_Amount
FROM transactions
GROUP BY Merchant, Category, Income_Expense;
