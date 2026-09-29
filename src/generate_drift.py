import numpy as np
import pandas as pd

rng = np.random.default_rng(123)
df = pd.read_csv("data/processed/test.csv")

df["credit_score"] = np.clip(
    df["credit_score"] - rng.normal(60, 15, len(df)), 300, 850
)
df["credit_utilization"] = np.clip(
    df["credit_utilization"] + rng.normal(0.20, 0.08, len(df)), 0, 1
)
df["debt_to_income"] = np.clip(
    df["debt_to_income"] + rng.normal(0.15, 0.05, len(df)), 0, 2
)

df.to_csv("data/production_batch.csv", index=False)
print("drift batch created")
