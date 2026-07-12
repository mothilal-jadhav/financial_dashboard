# Data Dictionary

| Column | Type | Description |
| --- | --- | --- |
| Transaction_ID | Integer | Unique transaction identifier after cleaning. |
| Date | Date | Transaction date between 2023-01-01 and 2024-12-31. |
| Merchant | Text | Merchant or income source name. |
| Category | Text | Standardized transaction category. |
| Amount | Float | Positive transaction amount in INR. |
| Payment_Method | Text | UPI, Credit Card, Debit Card, Cash, or Net Banking. |
| Location | Text | Transaction location or Online. |
| Income_Expense | Text | Indicates whether the row is Income or Expense. |
| Account_Balance | Float | Account balance after the transaction in chronological order. |
| Year | Integer | Calendar year extracted from Date. |
| Month | Integer | Calendar month number from 1 to 12. |
| Month_Name | Text | Full month name. |
| Quarter | Text | Calendar quarter such as Q1 or Q4. |
| Day_Of_Week | Text | Day name such as Monday or Saturday. |
| Is_Weekend | Integer | 1 for Saturday/Sunday, otherwise 0. |

## Category Values

Income categories:
- Salary/Stipend
- Family Support
- Freelance
- Interest
- Cashback
- Refund

Expense categories:
- Rent
- Food & Dining
- Groceries
- Transportation
- Shopping
- Entertainment
- Health
- Education
- Bills
- Travel
- Investment
- Miscellaneous
