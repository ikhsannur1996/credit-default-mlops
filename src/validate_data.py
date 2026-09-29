import pandas as pd

df = pd.read_csv("data/raw/credit_default.csv")

required = [
    "customer_id", "age", "income", "employment_years",
    "loan_amount", "loan_term", "interest_rate",
    "credit_score", "existing_loan", "monthly_installment",
    "debt_to_income", "credit_utilization",
    "number_of_accounts", "late_payment_count", "default"
]

assert set(required).issubset(df.columns)
assert df.customer_id.is_unique
assert df.income.gt(0).all()
assert df.loan_amount.gt(0).all()
assert df.credit_score.between(300, 850).all()
assert df.default.isin([0, 1]).all()

print("VALIDATION PASSED")
