-- 01. Overall portfolio KPIs
SELECT
    COUNT(*) AS total_transactions,
    ROUND(SUM(CASE WHEN Income_Expense = 'Income' THEN Amount ELSE 0 END), 2) AS total_income,
    ROUND(SUM(CASE WHEN Income_Expense = 'Expense' THEN Amount ELSE 0 END), 2) AS total_expense,
    ROUND(SUM(CASE WHEN Income_Expense = 'Income' THEN Amount ELSE -Amount END), 2) AS net_savings,
    ROUND(AVG(Account_Balance), 2) AS avg_account_balance
FROM transactions;

-- 02. Monthly income, expense, and savings
SELECT *
FROM vw_monthly_summary
ORDER BY Year, Month;

-- 03. Monthly savings rate
SELECT
    Year_Month,
    Total_Income,
    Total_Expense,
    Net_Savings,
    ROUND(Net_Savings * 100.0 / NULLIF(Total_Income, 0), 2) AS Savings_Rate_Percent
FROM vw_monthly_summary
ORDER BY Year_Month;

-- 04. Months with expenses above 100,000
SELECT
    Year_Month,
    Total_Expense
FROM vw_monthly_summary
WHERE Total_Expense > 100000
ORDER BY Total_Expense DESC;

-- 05. Category-wise expense contribution
SELECT
    Category,
    Total_Spent,
    ROUND(
        Total_Spent * 100.0 / SUM(Total_Spent) OVER (),
        2
    ) AS Expense_Share_Percent,
    Transaction_Count
FROM vw_category_spending
ORDER BY Total_Spent DESC;

-- 06. Categories with average transaction value above 2,000
SELECT
    Category,
    ROUND(AVG(Amount), 2) AS Avg_Transaction,
    COUNT(*) AS Transaction_Count
FROM transactions
WHERE Income_Expense = 'Expense'
GROUP BY Category
HAVING AVG(Amount) > 2000
ORDER BY Avg_Transaction DESC;

-- 07. Top 10 merchants by expense amount
SELECT
    Merchant,
    ROUND(SUM(Amount), 2) AS Total_Spent,
    COUNT(*) AS Transaction_Count
FROM transactions
WHERE Income_Expense = 'Expense'
GROUP BY Merchant
ORDER BY Total_Spent DESC
LIMIT 10;

-- 08. Top merchant within each expense category
WITH merchant_category AS (
    SELECT
        Category,
        Merchant,
        ROUND(SUM(Amount), 2) AS Total_Spent,
        RANK() OVER (PARTITION BY Category ORDER BY SUM(Amount) DESC) AS Merchant_Rank
    FROM transactions
    WHERE Income_Expense = 'Expense'
    GROUP BY Category, Merchant
)
SELECT Category, Merchant, Total_Spent
FROM merchant_category
WHERE Merchant_Rank = 1
ORDER BY Total_Spent DESC;

-- 09. Payment method usage and amount split
SELECT
    Payment_Method,
    COUNT(*) AS Transaction_Count,
    ROUND(SUM(Amount), 2) AS Total_Amount,
    ROUND(AVG(Amount), 2) AS Avg_Amount
FROM transactions
GROUP BY Payment_Method
ORDER BY Total_Amount DESC;

-- 10. Expense share by payment method
SELECT
    Payment_Method,
    ROUND(SUM(Amount), 2) AS Expense_Amount,
    ROUND(SUM(Amount) * 100.0 / SUM(SUM(Amount)) OVER (), 2) AS Expense_Share_Percent
FROM transactions
WHERE Income_Expense = 'Expense'
GROUP BY Payment_Method
ORDER BY Expense_Amount DESC;

-- 11. Weekend vs weekday spending
SELECT
    CASE WHEN Is_Weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS Day_Type,
    COUNT(*) AS Transaction_Count,
    ROUND(SUM(Amount), 2) AS Total_Spent,
    ROUND(AVG(Amount), 2) AS Avg_Transaction
FROM transactions
WHERE Income_Expense = 'Expense'
GROUP BY Is_Weekend;

-- 12. Day-of-week spending pattern
SELECT
    Day_Of_Week,
    COUNT(*) AS Transaction_Count,
    ROUND(SUM(Amount), 2) AS Total_Spent,
    ROUND(AVG(Amount), 2) AS Avg_Transaction
FROM transactions
WHERE Income_Expense = 'Expense'
GROUP BY Day_Of_Week
ORDER BY Total_Spent DESC;

-- 13. Running account balance by transaction date
SELECT
    Transaction_ID,
    Date,
    Merchant,
    Category,
    Income_Expense,
    Amount,
    Account_Balance
FROM transactions
ORDER BY Date, Transaction_ID;

-- 14. Running total income and expense
SELECT
    Date,
    Transaction_ID,
    Income_Expense,
    Amount,
    ROUND(
        SUM(CASE WHEN Income_Expense = 'Income' THEN Amount ELSE 0 END)
        OVER (ORDER BY Date, Transaction_ID),
        2
    ) AS Running_Income,
    ROUND(
        SUM(CASE WHEN Income_Expense = 'Expense' THEN Amount ELSE 0 END)
        OVER (ORDER BY Date, Transaction_ID),
        2
    ) AS Running_Expense
FROM transactions
ORDER BY Date, Transaction_ID;

-- 15. Month-over-month expense change
WITH monthly AS (
    SELECT Year_Month, Total_Expense
    FROM vw_monthly_summary
)
SELECT
    Year_Month,
    Total_Expense,
    LAG(Total_Expense) OVER (ORDER BY Year_Month) AS Previous_Month_Expense,
    ROUND(
        Total_Expense - LAG(Total_Expense) OVER (ORDER BY Year_Month),
        2
    ) AS Expense_Change
FROM monthly;

-- 16. Rank months by highest savings
SELECT
    Year_Month,
    Total_Income,
    Total_Expense,
    Net_Savings,
    RANK() OVER (ORDER BY Net_Savings DESC) AS Savings_Rank
FROM vw_monthly_summary
ORDER BY Savings_Rank;

-- 17. Quarterly expense summary
SELECT
    Year,
    Quarter,
    ROUND(SUM(Amount), 2) AS Total_Expense,
    COUNT(*) AS Transaction_Count
FROM transactions
WHERE Income_Expense = 'Expense'
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

-- 18. Income source analysis
SELECT
    Category AS Income_Source,
    ROUND(SUM(Amount), 2) AS Total_Income,
    COUNT(*) AS Transaction_Count,
    ROUND(AVG(Amount), 2) AS Avg_Income
FROM transactions
WHERE Income_Expense = 'Income'
GROUP BY Category
ORDER BY Total_Income DESC;

-- 19. High-value expense transactions
SELECT
    Transaction_ID,
    Date,
    Merchant,
    Category,
    Amount,
    Payment_Method,
    Location
FROM transactions
WHERE Income_Expense = 'Expense'
  AND Amount >= 8000
ORDER BY Amount DESC;

-- 20. Location-wise spending
SELECT
    Location,
    ROUND(SUM(Amount), 2) AS Total_Spent,
    COUNT(*) AS Transaction_Count,
    ROUND(AVG(Amount), 2) AS Avg_Transaction
FROM transactions
WHERE Income_Expense = 'Expense'
GROUP BY Location
ORDER BY Total_Spent DESC;

-- 21. Monthly category spending matrix
SELECT
    printf('%04d-%02d', Year, Month) AS Year_Month,
    Category,
    ROUND(SUM(Amount), 2) AS Total_Spent
FROM transactions
WHERE Income_Expense = 'Expense'
GROUP BY Year, Month, Category
ORDER BY Year_Month, Total_Spent DESC;

-- 22. Categories growing versus previous month
WITH category_monthly AS (
    SELECT
        printf('%04d-%02d', Year, Month) AS Year_Month,
        Category,
        SUM(Amount) AS Total_Spent
    FROM transactions
    WHERE Income_Expense = 'Expense'
    GROUP BY Year, Month, Category
)
SELECT
    Year_Month,
    Category,
    ROUND(Total_Spent, 2) AS Total_Spent,
    ROUND(
        Total_Spent - LAG(Total_Spent) OVER (PARTITION BY Category ORDER BY Year_Month),
        2
    ) AS Monthly_Change
FROM category_monthly
ORDER BY Category, Year_Month;

-- 23. Average transaction size by income/expense type
SELECT
    Income_Expense,
    COUNT(*) AS Transaction_Count,
    ROUND(MIN(Amount), 2) AS Min_Amount,
    ROUND(AVG(Amount), 2) AS Avg_Amount,
    ROUND(MAX(Amount), 2) AS Max_Amount
FROM transactions
GROUP BY Income_Expense;

-- 24. Merchant repeat behavior
SELECT
    Merchant,
    COUNT(*) AS Transaction_Count,
    ROUND(SUM(Amount), 2) AS Total_Amount,
    ROUND(AVG(Amount), 2) AS Avg_Amount
FROM transactions
GROUP BY Merchant
HAVING COUNT(*) >= 20
ORDER BY Transaction_Count DESC, Total_Amount DESC;

-- 25. Categorize expense transactions by ticket size
SELECT
    CASE
        WHEN Amount < 500 THEN 'Small'
        WHEN Amount < 2000 THEN 'Medium'
        WHEN Amount < 8000 THEN 'Large'
        ELSE 'Very Large'
    END AS Ticket_Size,
    COUNT(*) AS Transaction_Count,
    ROUND(SUM(Amount), 2) AS Total_Spent
FROM transactions
WHERE Income_Expense = 'Expense'
GROUP BY Ticket_Size
ORDER BY Total_Spent DESC;

-- 26. Identify negative savings months
SELECT
    Year_Month,
    Total_Income,
    Total_Expense,
    Net_Savings
FROM vw_monthly_summary
WHERE Net_Savings < 0
ORDER BY Net_Savings;

-- 27. Rolling 3-month average expense
SELECT
    Year_Month,
    Total_Expense,
    ROUND(
        AVG(Total_Expense) OVER (
            ORDER BY Year_Month
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ),
        2
    ) AS Rolling_3M_Avg_Expense
FROM vw_monthly_summary
ORDER BY Year_Month;

-- 28. Final account balance check
SELECT
    Date,
    Transaction_ID,
    Account_Balance
FROM transactions
ORDER BY Date DESC, Transaction_ID DESC
LIMIT 1;
