from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 10_000

df = pd.DataFrame({
    "customer_id": [f"C{i:05d}" for i in range(1, n + 1)],
    "age": rng.integers(21, 70, n),
    "income": rng.lognormal(np.log(8_000_000), 0.45, n),
    "employment_years": rng.uniform(0, 30, n),
    "loan_amount": rng.lognormal(np.log(75_000_000), 0.55, n),
    "loan_term": rng.choice([12, 24, 36, 48, 60], n),
    "interest_rate": rng.uniform(7, 20, n),
    "credit_score": np.clip(rng.normal(680, 70, n), 300, 850).round(),
    "existing_loan": rng.poisson(1.2, n),
    "credit_utilization": rng.beta(2, 5, n),
    "number_of_accounts": rng.integers(1, 10, n),
    "late_payment_count": rng.poisson(0.8, n),
})

df["monthly_installment"] = (
    df["loan_amount"] / df["loan_term"]
    * (1 + df["interest_rate"] / 100)
)

df["debt_to_income"] = np.clip(
    df["monthly_installment"]
    * (1 + df["existing_loan"] * 0.15)
    / (df["income"] / 12),
    0,
    2,
)

risk = (
    -0.006 * (df["credit_score"] - 650)
    + 2.2 * df["debt_to_income"]
    + 2.0 * df["credit_utilization"]
    + 0.30 * df["late_payment_count"]
    + 0.08 * df["existing_loan"]
)

prob = 1 / (1 + np.exp(-(risk - 1.5)))
df["default"] = rng.binomial(1, prob)

Path("data/raw").mkdir(parents=True, exist_ok=True)
df.to_csv("data/raw/credit_default.csv", index=False)

print(df.shape)
print(df["default"].value_counts(normalize=True))
