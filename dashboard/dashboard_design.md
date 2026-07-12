# Power BI Dashboard Design

## Objective

Create a one-page personal finance dashboard that helps a student understand spending behavior, savings trends, high-cost categories, and payment method usage.

## KPIs

- Total Income
- Total Expense
- Net Savings
- Savings Rate
- Average Monthly Expense
- Current Account Balance

## Page Layout

Top row:
- KPI cards for income, expense, savings, savings rate, and account balance.

Middle row:
- Line and clustered column chart: monthly income, expense, and net savings.
- Donut chart: expense share by category.

Bottom row:
- Bar chart: top 10 merchants by spend.
- Stacked bar chart: payment method spend by income/expense type.
- Matrix: category by month spending.

## Filters

- Year
- Quarter
- Month Name
- Category
- Payment Method
- Location
- Income/Expense

## Visuals

- KPI cards for executive summary.
- Monthly trend chart for seasonality and savings movement.
- Category distribution chart for expense prioritization.
- Merchant ranking chart for repeat spending behavior.
- Payment method chart for transaction channel analysis.
- Weekend vs weekday chart for behavioral comparison.

## Color Theme

- Income: `#2E7D32`
- Expense: `#C62828`
- Savings: `#1565C0`
- Neutral text: `#263238`
- Background: `#F7F9FB`
- Accent: `#F9A825`

## Data Model

Use a single fact table named `transactions`. For a more advanced model, create a calendar table in Power BI and relate it to `transactions[Date]`.
