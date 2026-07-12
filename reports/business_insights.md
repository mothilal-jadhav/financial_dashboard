# Business Insights

## Executive Summary

The project shows how a student can convert transaction-level finance data into decision-ready insights. The most useful views are monthly savings, high-spend categories, top merchants, and payment method behavior.

## Key Insights to Discuss in Interviews

- Monthly savings rate is the strongest high-level KPI because it combines income and expense behavior.
- Category analysis identifies whether spending is concentrated in discretionary areas such as shopping, entertainment, and travel.
- Merchant ranking highlights repeat spend patterns and possible subscription or habit-driven expenses.
- Payment method analysis helps explain behavior: UPI and cards often dominate daily expenses, while net banking is more common for income and larger transfers.
- Weekend analysis can reveal whether discretionary spending increases on Saturdays and Sundays.

## Recommended Actions

- Set monthly limits for the top three discretionary categories.
- Track recurring merchants separately to identify subscriptions or repeated small purchases.
- Review travel and shopping months for seasonal spikes.
- Monitor savings rate rather than only total savings, because income varies across months.
- Build a Power BI monthly review page for quick personal finance check-ins.

## Interview Talking Points

- The raw data intentionally contains real-world quality issues.
- The ETL pipeline validates uniqueness, missing values, date parsing, and negative amounts.
- SQLite makes the project fully reproducible without a cloud database.
- SQL queries demonstrate practical business analytics patterns, not only syntax.
