# DAX Measures

```DAX
Total Income =
CALCULATE(
    SUM(transactions[Amount]),
    transactions[Income_Expense] = "Income"
)
```

```DAX
Total Expense =
CALCULATE(
    SUM(transactions[Amount]),
    transactions[Income_Expense] = "Expense"
)
```

```DAX
Net Savings =
[Total Income] - [Total Expense]
```

```DAX
Savings Rate % =
DIVIDE([Net Savings], [Total Income], 0)
```

```DAX
Transaction Count =
COUNTROWS(transactions)
```

```DAX
Average Transaction Amount =
AVERAGE(transactions[Amount])
```

```DAX
Average Monthly Expense =
AVERAGEX(
    VALUES(transactions[Month_Name]),
    [Total Expense]
)
```

```DAX
Current Account Balance =
VAR LatestDate = MAX(transactions[Date])
RETURN
CALCULATE(
    MAX(transactions[Account_Balance]),
    transactions[Date] = LatestDate
)
```

```DAX
Weekend Expense =
CALCULATE(
    [Total Expense],
    transactions[Is_Weekend] = 1
)
```

```DAX
Weekday Expense =
CALCULATE(
    [Total Expense],
    transactions[Is_Weekend] = 0
)
```

```DAX
Expense MoM Change =
[Total Expense]
    - CALCULATE(
        [Total Expense],
        DATEADD(transactions[Date], -1, MONTH)
    )
```
